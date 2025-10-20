Residual Diffusion Modeling for Km-scale Atmospheric Downscaling

Morteza Mardani

Nvidia

Noah Brenowitz

Nvidia

Yair Cohen

Nvidia Research

Jaideep Pathak

Nvidia

Chieh-Yu Chen

Nvidia

Cheng-Chin Liu

Central Weather Agency

Arash Vahdat

Nvidia Corporation

Karthik Kashinath

Nvidia

Jan Kautz NVIDIA

Mike Pritchard

Nvidia, University of California Irvine

Article

Keywords:

Posted Date: January 4th, 2024

DOI: https://doi.org/10.21203/rs.3.rs-3673869/v1

License:   This work is licensed under a Creative Commons Attribution 4.0 International License. Read Full License

Additional Declarations: There is NO Competing Interest.

Version of Record: A version of this preprint was published at Communications Earth & Environment on

February 24th, 2025. See the published version at https://doi.org/10.1038/s43247-025-02042-5.

Residual Diﬀusion Modeling for Km-scale Atmospheric Downscaling

Morteza Mardani1,*,a, Noah Brenowitz1,*, Yair Cohen1,*, Jaideep Pathak1, Chieh-Yu Chen1, Cheng-Chin Liu2, Arash Vahdat1, Karthik Kashinath1, Jan Kautz1, and Mike Pritchard1

1NVIDIA, Santa Clara, CA. 95050, USA 2Central Weather Administration, 64, Gongyuan Road, Taipei 100006, Taiwan *These authors contributed equally aCorresponding author: mmardani@nvidia.com

November 22, 2023

Abstract

Predictions of weather hazard require expensive km-scale simulations driven by coarser global inputs. Here, a cost-eﬀective stochastic downscaling model is trained from a high-resolution 2-km weather model over Taiwan conditioned on 25-km ERA5 reanalysis. To address the multi-scale machine learning challenges of weather data, we employ a two-step approach Corrector Diﬀusion (CorrDiﬀ ), where a UNet prediction of the mean is corrected by a diﬀusion step. Akin to Reynolds decomposition in ﬂuid dynamics, this isolates generative learning to the stochastic scales. CorrDiﬀ exhibits skillful RMSE and CRPS and faithfully recovers spectra and distributions even for extremes. Case studies of coherent weather phenomena reveal appropriate multivariate relationships reminiscent of learnt physics: the collocation of intense rainfall and sharp gradients in fronts and extreme winds and rainfall bands near the eyewall of typhoons. Downscaling global forecasts successfully retains many of these beneﬁts, foreshadowing the potential of end-to-end, global-to- km-scales machine learning weather predictions.

1

Introduction

Coarse-resolution 25-km global weather prediction is undergoing a machine learning renaissance thanks to autoregressive machine learning models trained on global reanalysis [6, 39, 11, 7, 29, 14, 32]. However, many applications of weather and climate data require kilometer-scale forecasts: e.g., risk assessment and capturing local eﬀects of topography and human land use [21]. Globally, applying ML at km-scale resolution poses signiﬁcant challenges since training costs are superlinear with respect to the resolution of training data. Moreover, predictions from global km-scale physical simulators are not yet well tuned, so available training data can have worse systematic biases than coarse-resolution or established regional simulations [56, 26], and current data tends to cover short periods of time. Such datasets are also massive, diﬃcult to transfer between data centers and frequently not produced on machines attached to signiﬁcant AI computing resources like GPUs.

In contrast, for regional simulation, scaling ML to km-scales is attractive. High-quality training data is abundant as many national weather agencies couple km-scale numerical weather models in a limited domain to coarser resolution global models [16] – a process called dynamical downscaling. Since these predictions are augmented by data assimilation from ground-based precipitation radar and other sensors, good estimates of regional km-scale atmospheric states exists [13]. Such dynamical downscaling is computationally expensive, which limits the number of ensemble members used to quantify uncertainties [38]. A common inexpensive alternative is to learn a statistical downscaling from these dynamical downscaling simulations and observations [60].

In this context, ML downscaling enters as an advanced (non linear) form of statistical downscaling with potential to emulate the ﬁdelity of dynamical downscaling. Several ML methods have been previously used

1

for downscaling [9, 50, 18, 57, 38, 59, 2]. Convolutional Neural Networks, which reduce the input dimensions, have shown promise in globally downscaling climate (100km) data to weather scales (25km) [35, 47, 3, 45]. However, such deterministic ML approaches require interventions to produce useful probabilistic results, such as ensemble inference [47] or predicting the parameters of an assumed distribution [3]).

The stochastic nature of atmospheric physics at km-scale [51] makes the downscaling inherently probabilis- tic, making it natural to apply generative models at these scales. Generative Adversarial Networks (GANs) have been tested, including for forecasting precipitation at km-scale in various regions [31, 43, 22, 46, 20, 59]; see the latter for a good review. Training GANs, however, poses several practical challenges including mode collapse, training instabilities, and diﬃculties in capturing long tails of distributions [61, 28, 48].

Alternatively, diﬀusion models oﬀer sample diversity and training stability [25, 15] alongside demonstrable skill in probabilistically generating km-scales. [1] used a diﬀusion model for predicting rain density in the UK from vorticity as an input, thus demonstrating potential for channel synthesis. [23] used a diﬀusion model for downscaling solar irradiance in Hawaii with a 1 day lead time, demonstrating the ability to simultaneously forecast. Moreover, diﬀusion models have been used directly for probabilistic weather forecasting and nowcasting [30, 33, 36]. See table S1 in 1 for more details.

Building from this work, we turn to our challenge of interest – stochastically downscaling multiple variables simultaneously while also transferring input information to predict a new ﬁeld (i.e. channel synthesis). If successful, this paves the way towards end-to-end ML downscaling systems that predicts regional high- resolution weather as a postprocessing of global predictions. As a proof of concept we will demonstrate such a ML model trained for the region surrounding Taiwan and show its downscaling abilities from both a global reanalysis and a global forecast model.

Details follow. The key contributions of this paper are:

1. A physics-inspired, two-step approach (CorrDiﬀ) to learn mappings between low- and high-resolution weather data with high ﬁdelity.

2. CorrDiﬀ provides realistic measures of stochasticity and uncertainty, in terms of Continuous Rank Probability Score (CRPS) and by comparing spectra and distributions.

3. CorrDiﬀ reproduces the physics of coherent weather phenomena remarkably well, correcting frontal systems and typhoons.

4. CorrDiﬀ is sample-eﬃcient, learning eﬀectively from just 4 years of data.

5. CorrDiﬀ on a single GPU is at least 22 times faster and 1,300 times more energy eﬃcient than the numerical model used to produce its high resolution training data, which is run on 928 CPU cores.

2 Generative downscaling: Corrector diﬀusion model

❘cin×m×n is a Consider a speciﬁc region on Earth, mapped onto a two-dimensional grid. Our input y low-resolution meteorological forecast taken from a 25-km global weather forecasting model (e.g., FourCastNet [39, 29, 7], or the Global Forecast System (GFS) [37]) . Here, cin represents the number of input channels ❘cout×p×q come from and m,n represent the dimensions of a 2D subset of the globe. Our targets x corresponding data aligned in time cout but having higher resolution, i.e. p > m and q > n.

∈

∈

In our proof of concept we use the ERA5 reanalysis as input, over a subregion surrounding Taiwan, with m = n = 36, cin = 20 and cout = 4. See Table S2 for details about the inputs and outputs. The target data are 12.5 times higher resolution (p = q = 448) and were produced using a radar-assimilating Weather Research and Forecasting (WRF) physical simulator [41] provided by the Central Weather Administration of Taiwan (CWA) [13] (i.e. CWA-WRF). Though imperfect, WRF is a SOTA model for km-scale weather simulations and is used operationally by several national weather agencies.

The goal of probabilistic downscaling is to mimic the conditional probability density p(x y). To learn y) we employ a diﬀusion model. Such models learn generative SDEs through the concept of score p(x matching [25, 53, 27, 52, 5], with a forward and a backward processes working in tandem. In the forward process, noise is gradually added to the target data until the signal becomes indistinguishable from noise. The backward process then involves denoising the samples using a dedicated neural network to eliminate the

|

|

2

y

4 Res Blocks

4 Res Blocks + Self attention

Conv Block

Down/up sample block

Concatenate

Concatenate

Concatenate

Figure 1: The workﬂow for training and sampling CorrDiﬀ for generative downscaling. Top: Coarse-resolution global weather data at 25 km scale is used to ﬁrst predict the mean µ using a regression model, which is then stochastically corrected using EDM diﬀusion r, together producing the probabilistic high-resolution 2 km-scale regional forecast. Bottom right: diﬀusion model is conditioned with the coarse-resolution input to generate the residual r after a few denoising steps. Bottom left: the score function for diﬀusion is learned based on the UNet architecture.

noise. Through this sequential denoising process, the model iteratively reﬁnes the samples, bringing them closer to the target data distribution. The denoising neural network plays a critical role in this convergence, providing the necessary guidance to steer the samples towards accurate representations of the original data. The motivation for CorrDiﬀ is that naively applying conditional diﬀusion models to directly learn p(x y) was unsuccessful. The large uncertainty of variables such as radar reﬂectivity at these scales requires substantial noise levels during the forward process demands a large number of steps in backward process. This impedes learning and leads to poor sample ﬁdelity [54].

To sidestep these challenges, we decompose the generation into two steps (Fig. 1). The ﬁrst step predicts the conditional mean using (UNet) regression (see also 2 and S1 for details), and the second step learns a correction using a diﬀusion model as follows:

x =

❊[x

y]

| :=µ(regression) | {z }

+ (x

−

❊[x

|

y])

:=r(generation) | } {z

,

where y and x are the input and target respectively. This signal decomposition is inspired by Reynolds decomposition in ﬂuid-dynamics [40] and climate data analytics. Assuming the regression learns the conditional mean accurately, i.e., µ 0, and as a result var(r

❊[x

y], the residual is zero mean, namely ❊[r

y]

≈

≈

|

|

y). Accordingly, based on law of total variance [10], one can decompose the variance as

y) = var(x

| var(r) = ❊ (cid:2)

|

❊ (cid:2)

❊[x

❊[r

y]

y)

var(r

y)

= var(x).

y]

var(x

+ var

+ var

|

≤

|

|

|

(cid:0)

(cid:0)

(cid:3)

(cid:3)

(cid:1)

(cid:1)

=0 {z

≥0 {z

|

|

}

}

That is, the residual formulation ensures targets that have signiﬁcantly smaller variance. According to (2), the variance reduction is more pronounced when var(❊[x y]) is large, e.g., in the case of Typhoons. For our speciﬁc target data we ﬁnd that the actual variance reduction is signiﬁcant, especially at large scales; see section 3 and Figure S2. Moreover, the diﬀerence r is very localized and has no signiﬁcant spatial

|

3

|

(1)

(2)

(a)

(d)

) 2 s / 3

m

(

a r t c e p s

y g r e n e

104

103

102

101

target RF Reg Int-ERA5 ERA5 CorrDiff

) F D P ( g o

l

2.5

5.0

7.5

10.0

12.5

c i t e n K

i

100

10 1

10 3

10 2

Zonal wavenumber (1/km)

10 1

15.0

17.5

0

5

15 10 meter windspeed (m/s)

10

20

25

30

)(b) 2 ^ K m

(e)

2.5

(

a r t c e p s

e r u t a r e p m e t

103

102

101

100

) F D P ( g o

l

5.0

7.5

10.0

12.5

15.0

m 2

10 1

17.5

10 3

10 2

Zonal wavenumber (1/km)

10 1

270

290 300 2 meter temperature (K)

280

310

)(c) 2 ^ z b d m

104

(f)

2

(

a r t c e p s

y t i v i t c e l f e r

103

102

101

100

) F D P ( g o

l

0

2

r a d a r

10 1

10 3

10 2

10 1

4

0

1

2

3

4

5

Zonal wavenumber (1/km)

radar reflectivity (dbz)

Figure 2: Power spectra and distributions for the interpolated ERA5 input, CorrDiﬀ, RF, Reg, and WRF. These results reﬂect reductions over space, time and for CorrDiﬀ across 192 diﬀerent samples. Left: Power spectra for kinetic energy (top), 2 meter temperature (middle) and radar reﬂectivity (bottom). Right: distributions of windspeed, (top), 2 meter temperature (middle) and radar reﬂectivity (bottom). Radar reﬂectivity is not included in the ERA5 dataset. We show the log-PDF to highlight the diﬀerences at the tails of the distributions. Here wavenumber is the inverse of a wavelength.

auto-correlation at ranges beyond 30 km. In contrast, x has signiﬁcant auto-correlation even at a 200 km distance. To sum it up, the main idea of CorrDiﬀ is that learning the distribution p(r) can be much easier than learning the distribution p(x). Since modeling multi-scale interactions is a daunting task in many physics domains, we expect this approach could be widely applied. More details are described in Section 5 and the outline is depicted in Fig. 1.

3 Results

The target data (WRF) span four years (2018-2021) and additional ﬁrst four months of 2022, at one hour time resolution. We use the ﬁrst 3 years for training and the rest for testing. The input (course resolution) data is taken from the ERA5 reanalysis for the corresponding dates. See 5 and S2 for details.

CorrDiﬀ downscaling is compared with the input and target data and several baseline models, for deterministic and probabilistic skill scores, distributions and power spectra, and case studies of various coherent atmospheric phenomena.

4

Method

Metric

u10m Radar

v10m t2m

CorrDiﬀ CRPS CorrDiﬀ MAE UNet-regression MAE MAE Random forest regression ERA5 bilinear interpolation MAE

0.29 0.40 0.45 1.15 1.18

0.53 0.74 0.77 3.58 -

0.31 0.43 0.50 1.28 1.28

0.14 0.19 0.24 0.81 0.97

Table 1: Skill scores evaluated from 204 date and time combinations taken randomly from the out-of-sample year (2021). For CorrDiﬀ each evaluation used 192 samples. The table compares CorrDiﬀ, UNet-regression, random forest, and interpolated ERA5 predictions in terms of MAE of the ensemble mean and CRPS for diﬀerent atmospheric variables. For deterministic predictions, MAE and CRPS are equivalent. A separate RF is ﬁt with scikit-learn for each of the 4 output channels with 100 trees and the default hyperparameters. While crude, this RF provides a simple (and easily tuned) baseline for the performance of Reg.

3.1 Skill

Compared with several baselines, CorrDiﬀ shows the highest deterministic skill (MAE) followed by the UNet regression (Reg), the random forest (RF) and the interpolation of ERA5 (1). The diﬀerence between MAE of CorrDiﬀ and that of the UNet reﬂects the correction of the sample mean by the diﬀusion step. The consistent improvement in MAE for all the target variables between the UNet and CorrDiﬀ suggests that the generative CorrDiﬀ model (step 2) can correct some of the remaining biases after the UNet-regression (step 1).

3.2 Spectra and distributions

CorrDiﬀ is able to predict the correct power spectra of kinetic energy (KE), 2-meter temperature and radar reﬂectivity compared with the baselines in Table 1 (Fig. 2 a-c). The beneﬁts of CorrDiﬀ relative to the UNet baseline are stronger for some predicted variables than others. Improvements are most striking for radar reﬂectivity (Fig. 2 c) for which CorrDiﬀ matches the target power spectra while the UNet-regression is signiﬁcantly worse. This is expected as radar reﬂectivity comes from precipitation, which is linked to intrinsically stochastic physics (see [59]), i.e. requires the generation step for skillful prediction. In contrast, for 2-meter temperature (Fig. 2 b) the performance of UNet-regression is comparable to CorrDiﬀ; temperature downscaling is expected to be mostly driven by sub-grid variations in topography that can be learned determinstically from the static grid embeddings.

Good skill is also found when looking at the corresponding probability distributions (Fig. 2 d-f). CorrDiﬀ is able to match the target distribution, including the heavy-tailed structure, which is signiﬁcantly improved from the the prediction based on the UNet alone. These rare extreme values reﬂect most of the risk. For windspeed (Fig. 2 d), the UNet and the baseline models underestimate the probability of winds faster than 20 m/s. For 2-meter temperatures (Fig. 2 e), the baseline models overestimate the probability of warm extremes and underestimate the probability of cold extremes. Radar reﬂectivity proves to be the most challenging distribution to reproduce. CorrDiﬀ outperforms the other models in reproducing the reﬂectivity PDF (Fig. 2f). Although it overestimates the occurrence of reﬂectivity at lower values (i.e. weakly precipitating systems), the match of slopes at high values attests that the power-law relationship regulating the heavy-tail structure of rain extremes is emulated skillfully.

3.3 Case studies: downscaling coherent structures

Operational meteorologists value case study analysis, since aggregate skill scores and spectra can be more easily gamed or mask symptoms of spatial incoherence. We thus turn our attention to speciﬁc weather regimes. Fig. 3 illustrates the variability of the generated radar reﬂectivity ﬁeld at four distinct times. When analyzing 200 samples, the standard deviation of radar reﬂectivity (second column from the left) is roughly 20% of the magnitude of the mean (left column), with the majority of the variance located in and around existing precipitation regions. Such a pattern is anticipated given that the timing and location of precipitation can vary markedly even within a ﬁxed large-scale conﬁguration since convective physics are inherently stochastic.

5

Figure 3: Demonstration of the stochastic prediction of radar reﬂectivity (in dBZ). Top to bottom: 2021-09-12 00:00, 2021-04-02 06:00, 2021-02-02 12:00 and 2022-02-13 20:00. Left to right: sample mean, sample standard deviation, sample number 200 and the target forecast.

The CorrDiﬀ prediction for an individual sample (number 200, third column from the left) reveals a ﬁne-scale structure akin to the target data (right column). The similarity between panels (a) and (d) highlights the role of the mean prediction in forming large-scale coherent structures, such as typhoon Chanthu (2021), top row, and frontal systems, bottom row. Speciﬁcally the typhoon rainbands (spiral bands of clouds that emanate from the typhoon center) are coherent enough to be captured by the mean, but with large variance and smooth structure. The ﬁne-scale structure reﬂecting the stochastic physics is captured well by the diﬀusion model, reﬁning the smooth ﬁelds of the mean prediction as seen in the third column of Fig. 3. Further comparison across samples is presented in an animation in S3 in 4.

3.3.1 Frontal system case study

Frontal systems are an example of organized atmospheric systems. A cold front is a sharp change in temperature and winds associated with a mature cyclonic storm. As the front moves eastward, the cold air pushes the warm air to its east upward. This upward motion leads to cooling, condensation and ultimately rainfall. That is, these physics should manifest as multi-variate relationships with linked ﬁne scale structures of two wind vector components and temperature that should co-locate with radar reﬂectivity.

Fig. 4 shows an example of CorrDiﬀ downscaling a cold front. The position of the front is clearly visible in the southeast portion of the domain, where a strong horizontal surface temperature gradient (top) co-locates with strong across-front wind convergence (middle). The along-front components of the wind vector also change abruptly (middle row), which is consistent with the change in temperature. The super resolved gradients in the temperature and winds are encouragingly sharper than the input. The intense rainfall associated with this convergence line can be seen in the radar reﬂectivity ground truth for the same calendar date (which are shown in bottom row of Fig. 3 above). The generated radar reﬂectivity is appropriately

6

ERA5

CorrDiff from ERA5

WRF

NW-SE cross section

297.0

26

26

26

292.5

e d u t i t a L

24

24

24

288.0

283.5

22

20

22

20

22

20

279.0

274.5

CorrDiff WRF ERA5

270.0

118

120

122

124

118

120

122

124

118

120

122

124

0

1

2

3

13.5

9.0

26

26

26

4.5

e d u t i t a L

24

24

24

0.0

4.5

22

22

22

9.0

13.5

20

20

20

118

120

122

124

118

120

122

124

118

120

122

124

18.0

0

1

2

3

8

6

26

26

26

4

2

e d u t i t a L

24

24

24

0

2

4

22

22

22

6

8

20

20

20

10

118

120 Longitude

122

124

118

120 Longitude

122

124

118

120 Longitude

122

124

0

1

2

3

distance from [122E, 23N]

Figure 4: Examining the downscaling of a cold front on Feb 2, 2022 at 20 UTC. Left to right: prediction of ERA5, CorrDiﬀ and Target for diﬀerent ﬁelds, followed by their averaged cross section from 20 lines parallel to the thin dashed line in the contour ﬁgures. Top to bottom: 2 meter temperature (arrows are true wind vectors), along front wind (arrows are along front wind component) and across front wind (arrows are across front wind component).

concentrated near the frontal boundary. Both the location of the front, and the magnitude of the horizontal wind and temperature gradients (sharpening of the front) associated with it, are captured well by CorrDiﬀ although some mispositioning of the exact front location is inevitable. These are reassuring signs of learnt physics during the generation task.

3.3.2 Tropical Cyclone case study

Downscaling typhoons (i.e. tropical cyclones) is especially complicated. The average radius of maximum winds of a tropical cyclone is less than 100km, and at 25km resolution of the input data tropical cyclones are only partially resolved, resulting in cyclonic structures that are too wide and too weak compared with high resolution models or observations [8]. A useful downscaling model must simultaneously correct their size and intensity in addition to generating appropriate ﬁne-scale structure.

We ﬁnd that CorrDiﬀ is able to correct the structure of tropical cyclones accurately. Fig. 5(a)-(f) shows the structure of typhoon Chanthu (2021) on September 12 at 00:00:000 UTC. Compared to the target data (panel c) the poorly resolved typhoon in the ERA5 (panel a) is too wide and does not include a closed contour annulus of winds above 16 m/s surrounding an overly quiescent eye-wall. CorrDiﬀ downscaling (panel b) is able to recover much of the spatial structure of the windspeed compared with the target. The skill of the CorrDiﬀ downscaling compared to interpolating ERA5 can be more clearly quantiﬁed by calculating the mean axisymmetric structure of the storms as a function of radius from eye-wall center (panel f). Notably, with downscaling the radius of maximum winds decreases from 75km to about 25km while the windspeed

7

299

298

297

296

295

10

5

0

5

10

6

4

2

0

2

4

6

8

] K [

e r u t a r e p m e t

m 2

] s / m

d n w

i

t n o r f

g n o a

l

] s / m

[

d n w

i

t n o r f

s s o r c

(a)

ERA5

(b)

CorrDiff from ERA5

(c)

WRF

28

56

48

23°N

23°N

22.5°N

24

48

42

22°N

20

22.5°N

40

22.5°N

36

30

16

22°N

32

22°N

21.5°N

24

12

24

21.5°N

21.5°N

18

21°N

8

16

12

21°N

21°N

20.5°N

4

8

6

0

20.5°N

0

20.5°N

0

120.5°E

121.5°E

122.5°E

123.5°E

120.5°E

121.5°E

122.5°E

123.5°E

120.5°E

121.5°E

122.5°E

123.5°E

(d)

(e)

(f)

0.16

40

WRF CorrDiff from ERA5 ERA5

0.14

0.08

0.12

y t i s n e D y t i l i

b a b o r P

0.10

0.08

0.06

0.06

0.04

] s / m

d e e p s d n w m 0 1

i

30

20

0.04

0.02

10

0.02

0.00

0.00

0

0

10

20

30

10m windspeed [m/s]

40

50

0

10

20

30

10m windspeed [m/s]

40

50

0

25

50

75

100 radius [km]

125

150

175

200

Figure 5: A comparison of the 10m windspeed maps (m/s), distributions and the axisymmetric cross section from typhoon Chanthu (2021) on 2021/09/11:12:00:00UTC. Panels (a),(b),(c) show the 10m windspeed from ERA5, CorrDiﬀ downscaling of ERA5 and the target (WRF), respectively. The CorrDiﬀ panels show the ﬁrst ensemble member. The solid black contour indicates the Taiwan coastline. Storm center of the ERA5, CorrDiﬀ and WRF are shown in red ‘+‘, orange diamond, and the black dot, respectively. Panels (d) and (e) show the distribution shift (normalized PDFs) for the entire CWA domain and for the typhoon selected region in the top panels. Panel (f) shows the axisymmteric structure of the typhoon about its center. For the CorrDiﬀ curves, line is the ensemble mean and the shading shows one standard deviation around the mean.

increases from 20 m/s to 50 m/s – both favorable improvements.

Probabilities of damaging typhoon winds shown in in panels (d) and (e) in Fig. 5 are signiﬁcantly improved. In ERA5 (red), occurrence of weak wind speeds is over-estimated and the damaging extreme hurricane winds (above 25m/s) are missing. CorrDiﬀ better predicts the chances of the strong winds most likely to impact society and infrastructure. Further analysis 5 expands beyond this case study to examine generated wind statistics for several hundred typhoons that crossed the domain during 1980 to 2020. Although no target data is available, when comparing the maximum windspeed and radius of maximum windspeed from CorrDiﬀ predictions to a reference from the Japan Meteorological Agency best track dataset [4] CorrDiﬀ is found to correct at least 75% of the error in intensity for windspeed below 50m/s but only 50% of the error for higher windspeeds S4.

3.4 Downscaling a forecast from a global model

An attractive use case for CorrDiﬀ is to directly downscale forecasts from global models. During the writing of this paper, typhoon Koinu (2023) approached Taiwan. Together with CWA we compared the live forecasts of Koinu from GFS, CorrDiﬀ downscaling applied to GFS (here we use the same input channel as before) and WRF (target) data, see Figure 6. Expectation of good results should be tempered by the fact that this exposes CorrDiﬀ to out of sample inputs, by using GFS in place of ERA5. Even without retraining to include the leadtime forecast bias of GFS, we ﬁnd some encouraging results. An expected enhancement in windspeed intensity is conﬁrmed and it most accurate up to a leadtime of 6 hours (third row) after which is decreases. The radar reﬂectivity shows some caveats. While the domain averaged reﬂectivity is corrected well by CorrDiﬀ, the coherent rainband that is exhibited in the target data at lead times larger than 3h is absent in CorrDiﬀ. This rainband is also absent in the input (GFS), and CorrDiﬀ seem to struggle to generate it.

8

This suggests that CorrDiﬀ could be used for downscaling from a global model at short lead times (12h, for which baseline was provided).

4 Discussion

This study presents a generative diﬀusion model (CorrDiﬀ) for downscaling coarse-resolution (25-km) global weather state to higher resolution (2km) over a subset of the globe. CorrDiﬀ consists of two steps: regression and generation. The regression step approximates the mean, while the generation step further corrects the mean but also generates the distribution, producing ﬁne-scale details stochastically. This approach is akin to the decomposition of physical variables into their mean and perturbations, common practice in ﬂuid dynamics, e.g. [40].

Through extensive testing in the region of Taiwan, the model is shown to skillfully correct kinetic energy spectra, generate realistic probabilities and downscale coherent structures accurately(with minor caveats such as inaccuracies in the 2-meter temperature on the warm sector of a frontal system (Fig. 4) and over-correction of typhoon sizes in some out-of-sample cases for which we do not have the target (WRF) data, see 5). It is possible that the model’s accuracy could be further improved with a larger training dataset that contains more diverse examples of such rare coherent structures.

The two step approach in CorrDiﬀ also oﬀers the possibility to trade oﬀ between the fast inference of the mean using the UNet-regression, and the accurate and probabilistic inference of the CorrDiﬀ. This is particularly useful given that some variables – like the 2 meter temperature – are well predicted by the UNet-regression while others like radar reﬂectivity depend on the diﬀusion step for their skill (see Figure 2). Moreover, it could be possible to apply the diﬀusion step to a mean prediction obtained in a diﬀerent way (e.g. a numerical model if available) to generate a plausible distribution from a single prediction.

With the current hardware (see 6) and with an unoptimized code (no GPU parallelization or batching utilized), CorrDiﬀ inference is about 22 (40) times faster, and 1,130 (1,800) times more energy eﬃcient than running CWA-WRF on CPU with ﬂoat32 (mixed) precision.

This paper focused on generation quality, and not on optimal inference speed, for which gains could be easily anticipated. Our prototype of CorrDiﬀ is using a dozen iterations thanks to the initial regression step. However, for future work, we will push to reduce the number of iterations to only a few by using distillation methods [49, 61, 62] and pursuing other performance optimization techniques [34, 58].

Several potential extensions of the proposed method are worth considering:

1. Downscaling Coarse-Resolution Medium-Range Forecasts: This requires addressing lead time- dependent forecast errors, enabling a comprehensive evaluation of simultaneous bias correction and downscaling.

2. Downscaling at Diﬀerent Geographic Locations: The primary obstacle here is the scarcity of reliable kilometer-scale weather data. Additionally, addressing the computational scalability of CorrDiﬀ for regions signiﬁcantly larger than Taiwan is crucial.

3. Downscaling Future Climate Predictions: This introduces further complexities related to con- ditioning probabilistic predictions on various future anthropogenic emissions scenarios and assessing whether the generated weather envelope appropriately reﬂects climate sensitivity, particularly concerning extreme events.

These extensions have signiﬁcant potential beneﬁts such as accelerated regional forecasts, increased ensemble sizes, improved climate downscaling, and the provision of high-resolution regional forecasts in data-scarce regions, leveraging training data from adjacent areas.

5 Methods

This section elaborates on the proposed CorrDiﬀ methodology for probabilistic downscaling. It begins with a background on diﬀusion models to provide the machinery. It then delves into CorrDiﬀ and its associated components. We further detail our experimental setup including the CWA dataset, network architecture, and training protocols. At the end, we brieﬂy discuss evaluation criteria.

9

8.6

6.8

5.9

9.5

7.0

7.3

11.1

8.3

8.1

12.6

9.2

8.8

13.0

9.5

8.4

Figure 6: A comparison of a live km-scale forecast made by linking GFS predictions to CorrDiﬀ donwscaling, validated against WRF-CWA operational predictions made prior to the typhoon Loinu landfall. Forecast is initialized on 20231004-12:00 UTC, top to bottom show lead time 0, 3, 6, 9, 12 hours. Left to right: forecast from the GFS; CorrDiﬀ downscaling of GFS and the target (WRF-CWA). The fourth column compares the axisymmetric windspeed proﬁle of the typhoon (shading for GFS+CorrDiﬀ shows one standard deviation). The domain mean of the 1-hr maximum radar reﬂectivity is indicated at the top left of each of the reﬂectivity maps.

10

5.1 Background on diﬀusion models

Consider the data distribution represented by pdata(x). This distribution has an associated standard deviation, denoted by σdata. The forward diﬀusion process seeks to adjust this distribution, yielding modiﬁed distributions denoted by pdata(x;σ). This transformation is achieved by incorporating i.i.d. Gaussian noise with a standard deviation of σ into the data. When σ surpasses σdata by a considerable margin, the resulting distribution approximates pure Gaussian noise.

Conversely, the backward diﬀusion process operates by initially sampling noise, represented as x0, from maxI). The process then focuses on the denoising of this image into a series, xi, that the distribution is characterized by a descending order of noise levels: σ0 = σmax > σ1 > ... > σN = 0. Each noise level corresponds to a speciﬁc distribution of the form xi pdata(xi;σi). The terminal image of the backward process, xN, is expected to approach the original data distribution. SDE formulation. To present the forward and backward processes rigorously, they can be captured via stochastic diﬀerential equations (SDEs). Such SDEs ensure that the sample, x, aligns with the designated data distribution, p, over its progression through time [55, 27]. A numerical SDE solver can be used here, where a critical component is the noise schedule, σ(t), which prescribes the noise level at a speciﬁc time, t. A typical noise scheduler is σ(t)

(0,σ2

N

∼

∝

√t. Based on [27], the forward SDE is given as

dx =

2˙σ(t)σ(t)dωωω(t),

while the backward SDE is

p

dx =

x logp(x;σ(t))dt +

2˙σ(t)σ(t)d¯ωωω(t).

2˙σ(t)σ(t)

∇

−

p

The term ˙σ(t) refers to the time derivative of σ(t). The forward SDE is a Wiener process, while the backward SDE comprises two terms: a deterministic component representing the probability ﬂow ODE with noise degradation, and noise injection via the Wiener process. Denoising score matching. An examination of the SDE in Eq. (4) indicates the necessity of the score x logp(x;σ), for sampling from diﬀusion models. Intriguingly, this score function remains unaﬀected function, by the normalization constant of the base distribution, regardless of its computational complexity. Given its x)/σ2, a denoising independence, it can be deduced using a denoising method. If neural network, namely Dθ(x;σ), can be trained for the denoising task using

∇

x logp(x;σ) = (Dθ(x;σ)

∇

−

❊x∼pdata❊σ∼pσ❊n∼N(0,σ2I)

2

x

min θ

.

Dθ(x + n;σ)

−

(cid:2)∥

∥

(cid:3)

Note, the noise variance is also modeled as a random variable that simulates diﬀerent noise levels in the forward process e.g., based on log-normal distribution; see [27].

5.2 Proposed approach

As discussed in section 2, the high resolution state x in (1) can be written as the sum of the mean µ and the diﬀerence r, where the latter will be nearly zero mean and exhibits a small distribution shift, which facilities training diﬀusion models for correcting the mean prediction. It is worth noting that this two-step method has further implications for learning physics. The UNet-regression step can anticipate many of the physics of downscaling, some of which are deterministic. These include high-resolution topography (which to ﬁrst order controls the 2-meter temperature variation due to the lapse-rate eﬀect), and the large-scale horizontal wind which combine leading balances in the free atmosphere with the eﬀect of surface friction and topography. Stochastic phenomena such as convective storms that also change temperatures and winds are easier to model as deviations from the mean. Also, cloud resolving models are explicitly formulated using deviations from a larger scale balanced state [42]. In the next section, we discuss the regression and generation step in details.

5.2.1 Regression on the mean

In order to predict the conditional mean µµµ = ❊[x y], we resort to UNet-regression. A UNet network is N n=1 to learn the regression. We adopt a UNet architecture that is supervised with training data } commonly used in denoising diﬀusion models. This particular UNet [53] incorporates attention layers and residual layers, allowing it to eﬀectively capture both short and long-range dependencies in the data see section 2 and S1. Mean-Squared-Error (MSE) loss is optimized for training.

|

(xn,yn)

{

11

(3)

(4)

(5)

5.2.2 Denoising diﬀusion corrector

Once equipped with the UNet-regression network, we can begin by predicting the conditional mean ˆµµµ, which serves as an approximation of ❊[x y]. Subsequently, we proceed to train the diﬀusion model directly on the diﬀerence: r = x ˆµµµ. Notably, the diﬀerence exhibits a small departure from the target data, allowing for the utilization of smaller noise levels during the training of the diﬀusion process.

|

−

In our approach, we adopt the Elucidated diﬀusion model (EDM), a continuous-time diﬀusion model that adheres to the principles of SDEs (in Eq. (3)-(4)) [27] to design the diﬀusion process and architecture. As a result it has an intuitive and physics driven hyperparameter tuning, which makes it work across diﬀerent y) following domains. In our case, we want to generate r by sampling from the conditional distribution p(r the SDEs in Eq. (3)-(4). To condition the diﬀusion model, we concatenate the input coarse-resolution data y y) using the score matching with the noise over diﬀerent channels. We also learn the score function loss in Eq. (5) where the denoiser is now Dθ(r + n;σ;y) with the conditioning input y. For the denoiser we again follow the design principles in EDM to use a UNet architecture with skip connections weighted by the noise variance. Architecture details are discussed in Section 5.3.2.

|

r logp(r

∇

|

y), we employ the second-order EDM stochastic sampler [27] [Algorithm 2] to solve for the reverse SDE in Eq. (4). Upon sampling r, we augment it with the predicted conditional mean ˆµµµ from regression, to generate the sample ˆµµµ+r. This entire workﬂow is illustrated in Fig. 1, providing a visual representation of the steps involved in our proposed method.

To generate samples from the distribution p(r

|

5.3 Experimental setup

5.3.1 Dataset

The input (conditioning) dataset is taken from ERA5 reanalysis [24], a global dataset at spatial resolution of about 25km and a temporal resolution of 1h, the latter matches the target data listed below. To facilitate training, we interpolate the input data onto the curvirectangular grid of CWA with bilinear interpolation 36 pixels over the region of Taiwan. Each sample in the input (with a rate of 4x), which results in 36 dataset consists of 20 channels of information see ??. This includes four pressure levels (500 hPa, 700 hPa, 850 hPa, and 925 hPa) with four corresponding variables: temperature, eastward and northward components horizontal wind vector, and Geopotential Height. Additionally, the dataset includes single level variables such as 2 meter Temperature, 10 meter wind vector, total column water vapor.

×

The target dataset used in this study is a subset of the proprietary RWRF model data (Radar Data Assimilation with WRFDA 1). The RWRF model is one of the operational regional Numerical Weather Prediction (NWP) models developed by CWA [13], which focuses on radar Data Assimilation (DA) in the vicinity of Taiwan. Assimilating radar data is a common strategy used in regional weather prediction, which helps constrain especially stochastic convective processes such as mesoscale convective systems and short-lived thunderstorms. The WRF - CWA system uses a nested 2km domain in a 10km that is driven by a global model (GFS) as boundary conditions [13]. By incorporating radar data [12], RWRF improves the short-term prediction of high-impact weather events. The radar observations possess high spatial resolution of approximately 1km and temporal resolutions of 5-10 minutes at a convective scale. These observations provide wind information (radial velocity) as well as hydrometers (radar reﬂectivity) usefully, with a particular emphasis on the lower atmosphere. The radar data assimilation relies on the availability of reliable and precise observations, which contributes signiﬁcantly to enhance the accuracy and performance of the applied deep learning algorithms in the context of NWP applications.

The target dataset covers a duration of 52 months, speciﬁcally from January 2018 to April 2022. It has a temporal frequency of one hour and a spatial resolution of 2km. We use only the inner (nested) 2km domain, which has 448 448 pixels, projected using the Lambert conformal conical projection method around Taiwan. The geographical extent of the dataset spans from approximately 116.371°E to 125.568°E in longitude and 19.5483°N to 27.8446°N in latitude. We sub-selected 4 channels (variables) as the target variables, that are most relevant for practical forecasting: temperature at 2 meter above the surface, the horizontal winds at 10 meter above the surface and the 1h maximum radar reﬂectivity - a surrogate of expect precipitation. Notably, the radar reﬂectivity channel is not present in the input data and needs to be predicted based on the other channels, making its prediction strictly generative. The radar reﬂectivity data also exhibits a

×

1https://www.mmm.ucar.edu/models/wrfda

12

distinct distribution compared to the other output channels, with positive values and a prominent zero-mode consistent with typical non-raining conditions.

Initially, the target data is provided in the NetCDF format, which is the output of the WRFDA assimilation process. Subsequently, vertical interpolated from sigma levels to isobaric levels then save as a custom CWA DMS format. As part of the preprocessing steps, the data is converted to the Hadoop Distributed File System (HDFS) format. Additionally, any missing or corrupted data points represented by "inf" or "nan" values are eliminated from the dataset. This leads to a reduction in the number of samples from 37,944 to 33,813.

To avoid over-ﬁtting we divide the data into training and testing sets. Three years of data 2018-2020 are used for training (2,4154 samples total). For testing we use the full fourth year, 2021, as well as the ﬁrst four months (January to April) of 2022.

5.3.2 Network architecture and training

The CorrDiﬀ method has two step learning approach. To ensure compatibility and consistency, we employ the same UNet architecture used in EDM (Elucidated Diﬀusion Models) for both the regression and diﬀusion networks(see S1). This architecture is based on the UNet model proposed in [53]. We enhance the UNet by increasing its size to include 6 encoder layers and 6 decoder layers. The base embedding size is set to 128, and it is multiplied over channels according to the pattern [1,2,2,2,2]. The attention resolution is deﬁned as 28. For time embedding in the diﬀusion process, we utilize Fourier-based position embedding. However, in the regression network, time embedding is disabled. No data augmentation techniques are employed during training. Overall, the UNet architecture comprises 80 million parameters. Additionally, we introduce 4 channels for sinusoidal positional embedding.

10−4, β1 = 0.9, and β2 = 0.99. Exponential moving averages (EMA) with a rate of η = 0.5 are applied, and dropout with a rate of 0.13 is utilized. The regression network solely receives the input conditioning channels. On the other hand, the diﬀusion training incorporates the 20 input conditioning channels from the coarse-resolution ERA5 data, which are concatenated with 4 noise channels to generate the output for each denoiser. For diﬀusion training, we adopt the Elucidated Diﬀusion Model (EDM), a continuous-time diﬀusion model. During training, EDM (0,1.22) and aims to denoise the samples per randomly selects the noise variance such that ln(σ(t)) mini-batch. EDM is trained for 100 million steps, while the regression network is trained for 30 million steps. The training process is distributed across 16 DGX nodes, each equipped with 8 A100 GPUs, utilizing data parallelism and a total batch size of 512. The total training time for regression and diﬀusion models was 7 days that amounts to approximately 21,504 GPU-hours.

During the training phase, we use the Adam optimizer with a learning rate of 2

×

∼ N

For sampling purposes, we employ the second-order stochastic sampler provided by EDM. This sampler performs 18 steps, starting from a maximum noise variance of σmax = 800 and gradually decreasing it to a minimum noise variance of σmin = 0.002. We adopt the rest of hyperparamaters from EDM as listed in [27].

5.4 Evaluation criterion

Probabilistic predictions aim to maximize sharpness subject to calibration [44]. Qualitatively, calibration means that the likelihood of observing the true value is the same as observing a member drawn from the ensemble. A necessary condition for calibration is that the spread-error relationship be 1-to-1 when averaged over suﬃcient samples [17]. Calibration also manifests as a ﬂat rank-histogram. A simple metric used below is the root-mean-squared error of the sample mean. In the large sample limit, the sample mean becomes deterministic. So we expect this error to be comparable for generative and deterministic models.

Instead of considering both calibration and spread separately, it can be easier to use proper scoring rules like the continuous-ranked-probability score (CRPS) [19]. Let x be a scalar observation and F be the cumulative distribution of the probabilistic forecast (e.g., the empirical CDF of generated samples). Then, CRPS is deﬁned as

∞

CRPS(F,x) =

Z

−∞

(F(y)

−

✶{y≥x})2 dy.

The F which minimizes CRPS is the true cumulative distribution of x. For a deterministic forecast, F(y) = ✶{y>=x0} where x0 is the forecast value, CRPS is equivalent to the mean absolute deviation.

13

6 Acknowledgements

We extend our profound appreciation to the Central Weather Administration (CWA) of Taiwan2, a premier government meteorological research and forecasting institution, for granting us access to the invaluable operational Numerical Weather Prediction (NWP) model dataset and for their expert guidance on data consultation. Our gratitude also extends to the AI-Algo team at NVIDIA, especially Kamyar Azizzadenesheli, Anima Anandkumar, Nikola Kovachki, Jean Kossaiﬁ, and Boris Bonev for their insightful discussions. Additionally, we are indebted to David Matthew Hall, Dale Durran, Chris Bretherton for thier constructive feedback on the manuscript.

References

[1] Henry Addison, Elizabeth Kendon, Suman Ravuri, Laurence Aitchison, and Peter AG Watson. Machine

learning emulation of a local-scale uk climate model. arXiv preprint arXiv:2211.16116, 2022.

[2] Rilwan A Adewoyin, Peter Dueben, Peter Watson, Yulan He, and Ritabrata Dutta. Tru-net: a deep learning approach to high resolution prediction of rainfall. Machine Learning, 110:2035–2062, 2021.

[3] Jorge Baño-Medina, Rodrigo Manzanas, and José Manuel Gutiérrez. Conﬁguration and intercomparison of deep learning neural models for statistical downscaling. Geoscientiﬁc Model Development, 13(4):2109– 2124, 2020.

[4] Monika Barcikowska, Frauke Feser, and Hans Von Storch. Usability of best track data in climate statistics

in the western north paciﬁc. Monthly Weather Review, 140(9):2818–2830, 2012.

[5] G. Batzolis, J. Stanczuk, C.-B. Schönlieb, and C. Etmann. Conditional image generation with score-based

diﬀusion models. arXiv preprint arXiv:2111.13606, 2021.

[6] Zied Ben-Bouallegue, Mariana C A Clare, Linus Magnusson, Estibaliz Gascon, Michael Maier-Gerber, Martin Janousek, Mark Rodwell, Florian Pinault, Jesper S Dramsch, Simon T K Lang, Baudouin Raoult, Florence Rabier, Matthieu Chevallier, Irina Sandu, Peter Dueben, Matthew Chantry, and Florian Pappenberger. The rise of data-driven weather forecasting, 2023.

[7] Kaifeng Bi, Lingxi Xie, Hengheng Zhang, Xin Chen, Xiaotao Gu, and Qi Tian. Accurate medium-range

global weather forecasting with 3d neural networks. Nature, pages 1–6, 2023.

[8] Gu-Feng Bian, Gao-Zhen Nie, and Xin Qiu. How well is outer tropical cyclone size represented in the

era5 reanalysis dataset? Atmospheric Research, 249:105339, 2021.

[9] Tobias Bischoﬀ and Katherine Deck. Unpaired downscaling of ﬂuid ﬂows with diﬀusion bridges. arXiv

preprint arXiv:2305.01822, 2023.

[10] Joseph K Blitzstein and Jessica Hwang. Introduction to probability. Crc Press, 2019.

[11] Boris Bonev, Thorsten Kurth, Christian Hundt, Jaideep Pathak, Maximilian Baust, Karthik Kashinath, and Anima Anandkumar. Spherical fourier neural operators: Learning stable dynamics on the sphere. arXiv preprint arXiv:2306.03838, 2023.

[12] Pao-Liang Chang, Jian Zhang, Yu-Shuang Tang, Lin Tang, Pin-Fang Lin, Carrie Langston, Brian Kaney, Chia-Rong Chen, and Kenneth Howard. An operational multi-radar multi-sensor qpe system in taiwan. Bulletin of the American Meteorological Society, 102(3):E555–E577, 2021.

[13] I-Han Chen, Jing-Shan Hong, Ya-Ting Tsai, and Chin-Tzu Fong. Improving afternoon thunderstorm prediction over taiwan through 3dvar-based radar and surface data assimilation. Weather and Forecasting, 35(6):2603–2620, 2020.

2https://www.cwa.gov.tw/eng/

14

[14] Florinel-Alin Croitoru, Vlad Hondru, Radu Tudor Ionescu, and Mubarak Shah. Diﬀusion models in

vision: A survey. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2023.

[15] P. Dhariwal and A. Nichol. Diﬀusion models beat gans on image synthesis. In Proceedings of NeurIPS,

volume 34, pages 8780–8794, 2021.

[16] Devajyoti Dutta, Ashish Routray, D Preveen Kumar, and John P George. Regional data assimilation with the ncmrwf uniﬁed model (ncum): impact of doppler weather radar radial wind. Pure and Applied Geophysics, 176:4575–4597, 2019.

[17] V Fortin, M Abaza, F Anctil, and R Turcotte. Why should ensemble spread match the RMSE of the

ensemble mean? J. Hydrometeorol., 15(4):1708–1713, August 2014.

[18] Andrew Geiss and Joseph C Hardin. Radar super resolution using a deep convolutional neural network.

Journal of Atmospheric and Oceanic Technology, 37(12):2197–2207, 2020.

[19] Tilmann Gneiting and Adrian E Raftery. Strictly proper scoring rules, prediction, and estimation. J.

Am. Stat. Assoc., 102(477):359–378, March 2007.

[20] Aofan Gong, Ruidong Li, Baoxiang Pan, Haonan Chen, Guangheng Ni, and Mingxuan Chen. Enhancing spatial variability representation of radar nowcasting with generative adversarial networks. Remote Sensing, 15(13):3306, 2023.

[21] William J Gutowski, Paul Aaron Ullrich, Alex Hall, L Ruby Leung, Travis Allen O’Brien, Christina M Patricola, RW Arritt, MS Bukovsky, Katherine V Calvin, Zhe Feng, et al. The ongoing need for high-resolution regional climate models: Process understanding and stakeholder information. Bulletin of the American Meteorological Society, 101(5):E664–E683, 2020.

[22] Lucy Harris, Andrew TT McRae, Matthew Chantry, Peter D Dueben, and Tim N Palmer. A generative deep learning approach to stochastic downscaling of precipitation forecasts. Journal of Advances in Modeling Earth Systems, 14(10):e2022MS003120, 2022.

[23] Yusuke Hatanaka, Yannik Glaser, Geoﬀ Galgon, Giuseppe Torri, and Peter Sadowski. Diﬀusion models

for high-resolution solar forecasts. arXiv preprint arXiv:2302.00170, 2023.

[24] Hans Hersbach, Bill Bell, Paul Berrisford, Shoji Hirahara, András Horányi, Joaquín Muñoz-Sabater, Julien Nicolas, Carole Peubey, Raluca Radu, Dinand Schepers, et al. The era5 global reanalysis. Quarterly Journal of the Royal Meteorological Society, 146(730):1999–2049, 2020.

[25] J. Ho, A. Jain, and P. Abbeel. Denoising diﬀusion probabilistic models. In Proceedings of NeurIPS,

volume 33, pages 6840–6851, 2020.

[26] Cathy Hohenegger, Peter Korn, Leonidas Linardakis, René Redler, Reiner Schnur, Panagiotis Adamidis, Jiawei Bao, Swantje Bastin, Milad Behravesh, Martin Bergemann, et al. Icon-sapphire: simulating the components of the earth system and their interactions at kilometer and subkilometer scales. Geoscientiﬁc Model Development, 16(2):779–811, 2023.

[27] Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diﬀusion-based

generative models. arXiv preprint arXiv:2206.00364, 2022.

[28] Naveen Kodali, Jacob Abernethy, James Hays, and Zsolt Kira. On convergence and stability of gans.

arXiv preprint arXiv:1705.07215, 2017.

[29] Remi Lam, Alvaro Sanchez-Gonzalez, Matthew Willson, Peter Wirnsberger, Meire Fortunato, Ferran Alet, Suman Ravuri, Timo Ewalds, Zach Eaton-Rosen, Weihua Hu, Alexander Merose, Stephan Hoyer, George Holland, Oriol Vinyals, Jacklynn Stott, Alexander Pritzel, Shakir Mohamed, and Peter Battaglia. Learning skillful medium-range global weather forecasting. Science, 0(0):eadi2336, 2023.

15

[30] Jussi Leinonen, Ulrich Hamann, Daniele Nerini, Urs Germann, and Gabriele Franch. Latent diﬀusion models for generative precipitation nowcasting with accurate uncertainty quantiﬁcation. arXiv preprint arXiv:2304.12891, 2023.

[31] Jussi Leinonen, Daniele Nerini, and Alexis Berne. Stochastic super-resolution for downscaling time- evolving atmospheric ﬁelds with a generative adversarial network. IEEE Transactions on Geoscience and Remote Sensing, 59(9):7211–7223, 2020.

[32] Hao Li, Lei Chen, Xiaohui Zhong, Feng Zhang, Yuan Cheng, Yinghui Xu, and Yuan Qi. Fuxi: A cascade

machine learning forecasting system for 15-day global weather forecast. 2023.

[33] Lizao Li, Rob Carver, Ignacio Lopez-Gomez, Fei Sha, and John Anderson. Seeds: Emulation of weather

forecast ensembles with diﬀusion models. arXiv preprint arXiv:2306.14066, 2023.

[34] Chenlin Meng, Robin Rombach, Ruiqi Gao, Diederik Kingma, Stefano Ermon, Jonathan Ho, and Tim Salimans. On distillation of guided diﬀusion models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14297–14306, 2023.

[35] Bin Mu, Bo Qin, Shijin Yuan, and Xiaoyun Qin. A climate downscaling deep learning model considering the multiscale spatial correlations and chaos of meteorological events. Mathematical Problems in Engineering, 2020:1–17, 2020.

[36] Pritthijit Nath, Pancham Shukla, and César Quilodrán-Casas. Forecasting tropical cyclones with cascaded

diﬀusion models. arXiv preprint arXiv:2310.01690, 2023.

[37] National Centers for Environmental Prediction, National Weather Service, NOAA, U.S. Department of

Commerce. Ncep gfs 0.25 degree global forecast grids historical archive, 2015.

[38] Nidhi Nishant, Sanaa Hobeichi, Steven C Sherwood, Gab Abramowitz, Yawen Shao, Craig Bishop, and Andy J Pitman. Comparison of a novel machine learning approach with dynamical downscaling for australian precipitation. Environmental Research Letters, 2023.

[39] Jaideep Pathak, Shashank Subramanian, Peter Harrington, Sanjeev Raja, Ashesh Chattopadhyay, Morteza Mardani, Thorsten Kurth, David Hall, Zongyi Li, Kamyar Azizzadenesheli, et al. Fourcastnet: A global data-driven high-resolution weather model using adaptive fourier neural operators. arXiv preprint arXiv:2202.11214, 2022.

[40] Stephen B Pope. Turbulent ﬂows. Cambridge university press, 2000.

[41] Jordan G Powers, Joseph B Klemp, William C Skamarock, Christopher A Davis, Jimy Dudhia, David O Gill, Janice L Coen, David J Gochis, Ravan Ahmadov, Steven E Peckham, et al. The weather research and forecasting model: Overview, system eﬀorts, and future directions. Bulletin of the American Meteorological Society, 98(8):1717–1737, 2017.

[42] Kyle G Pressel, Colleen M Kaul, Tapio Schneider, Zhihong Tan, and Siddhartha Mishra. Large-eddy simulation in an anelastic framework with closed water and entropy balances. Journal of Advances in Modeling Earth Systems, 7(3):1425–1456, 2015.

[43] Ilan Price and Stephan Rasp. Increasing the accuracy and resolution of precipitation forecasts using deep generative models. In International conference on artiﬁcial intelligence and statistics, pages 10555–10571. PMLR, 2022.

[44] Adrian E Raftery, Tilmann Gneiting, Fadoua Balabdaoui, and Michael Polakowski. Using bayesian model averaging to calibrate forecast ensembles. Mon. Weather Rev., 133(5):1155–1174, May 2005.

[45] Neelesh Rampal, Peter B Gibson, Abha Sood, Stephen Stuart, Nicolas C Fauchereau, Chris Brandolino, Ben Noll, and Tristan Meyers. High-resolution downscaling with interpretable deep learning: Rainfall extremes over new zealand. Weather and Climate Extremes, 38:100525, 2022.

16

[46] Suman Ravuri, Karel Lenc, Matthew Willson, Dmitry Kangin, Remi Lam, Piotr Mirowski, Megan Fitzsimons, Maria Athanassiadou, Sheleem Kashem, Sam Madge, et al. Skilful precipitation nowcasting using deep generative models of radar. Nature, 597(7878):672–677, 2021.

[47] Eduardo R. Rodrigues, Igor Oliveira, Renato L. F. Cunha, and Marco A. S. Netto. Deepdownscale: a deep learning strategy for high-resolution weather forecast. arXiv preprint arXiv:1808.05264, 2018.

[48] Tim Salimans, Ian Goodfellow, Wojciech Zaremba, Vicki Cheung, Alec Radford, and Xi Chen. Improved

techniques for training gans. Advances in neural information processing systems, 29, 2016.

[49] Tim Salimans and Jonathan Ho. Progressive distillation for fast sampling of diﬀusion models.

International Conference on Learning Representations, 2021.

[50] Badr-eddine Sebbar, Saïd Khabba, Olivier Merlin, Vincent Simonneaux, Chouaib El Hachimi, Mo- hamed Hakim Kharrou, and Abdelghani Chehbouni. Machine-learning-based downscaling of hourly era5-land air temperature over mountainous regions. Atmosphere, 14(4):610, 2023.

[51] Tobias Selz and George C Craig. Upscale error growth in a high-resolution simulation of a summertime

weather event over europe. Monthly Weather Review, 143(3):813–827, 2015.

[52] Jiefeng Song, Chaoyue Meng, and Stefano Ermon. Denoising diﬀusion implicit models. In Proceedings of

the International Conference on Learning Representations (ICLR), 2021.

[53] Yang Song and Stefano Ermon. Generative modeling by estimating gradients of the data distribution.

In Advances in Neural Information Processing Systems (NeurIPS), 2019.

[54] Yang Song and Stefano Ermon. Improved techniques for training score-based generative models. Advances

in neural information processing systems, 33:12438–12448, 2020.

[55] Yang Song, Jascha Sohl-Dickstein, Diederik P. Kingma, Ashish Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic diﬀerential equations. In Proceedings of the International Conference on Learning Representations (ICLR), 2021.

[56] Bjorn Stevens, Masaki Satoh, Ludovic Auger, Joachim Biercamp, Christopher S Bretherton, Xi Chen, Peter Düben, Falko Judt, Marat Khairoutdinov, Daniel Klocke, et al. Dyamond: the dynamics of the atmospheric general circulation modeled on non-hydrostatic domains. Progress in Earth and Planetary Science, 6(1):1–17, 2019.

[57] B Teufel, F Carmo, L Sushama, L Sun, MN Khaliq, S Bélair, A Shamseldin, D Nagesh Kumar, and J Vaze. Physics-informed deep learning framework to model intense precipitation events at super resolution. Geoscience Letters, 10(1):19, 2023.

[58] Arash Vahdat, Karsten Kreis, and Jan Kautz. Score-based generative modeling in latent space. Advances

in Neural Information Processing Systems, 34:11287–11302, 2021.

[59] Emily Vosper, Peter Watson, Lucy Harris, Andrew McRae, Raul Santos-Rodriguez, Laurence Aitchison, and Dann Mitchell. Deep learning for downscaling tropical cyclone rainfall to hazard-relevant spatial scales. Journal of Geophysical Research: Atmospheres, page e2022JD038163, 2023.

[60] Robert L Wilby, TML Wigley, D Conway, PD Jones, BC Hewitson, J Main, and DS Wilks. Statistical downscaling of general circulation model output: A comparison of methods. Water resources research, 34(11):2995–3008, 1998.

[61] Zhisheng Xiao, Karsten Kreis, and Arash Vahdat. Tackling the generative learning trilemma with denoising diﬀusion GANs. In Internatiodnal Conference on Learning Representations (ICLR), 2022.

[62] Hongkai Zheng, Weili Nie, Arash Vahdat, Kamyar Azizzadenesheli, and Anima Anandkumar. Fast sampling of diﬀusion models via operator learning. In International Conference on Machine Learning, pages 42390–42402. PMLR, 2023.

17

In

Citation

Architecture Resolutions

Pixels Variables

Addison et al., (2022) [1]

Diﬀusion

input: 60km target: 8.8km

642

precipitation

Harris et al., (2022) [22]

GANs + ensemble forecast

input: 10km target: 1km

9402

precipitation

Hatanaka et al., (2023) [23] Cascaded diﬀusion

input: 30km target: 1km

1282

day-ahead solar-irradiance

Leinonen et al., (2020) [31] GANs

input 8km target: 1km

1282

precipitation

Leinonen et al., (2020) [31] GANs

input 16km target: 2km

1282

cloud optical-thickness

Price and Rasp, (2022) [43] Corrector

GAN

input 32km target 4km

1282

precipitation

Vosper et al., (2023) [59] WGAN

input 100km target 10km

1002

precipitation from tropical-cyclones

Current work

CorrDiﬀ

input 25km target 2km

4482

10 meter winds 2 meter temperature radar-reﬂectivity

Table S1: Downscaling models presented in the most relevant works we could ﬁnd with respect to the current study. We highlight the resolution ratios, the pixel size of the high resolution prediction, predicted variables and architecture.

Supplementary Information

1 Our position with respect to existing works

To highlight the novel component of our work we expend our review. Table S1 above present a shortlist of the most relevant works that preform weather downscaling. Some of the successes of previous downscaling works are by preforming state vector inﬂation as [1], on a relatively larger domain [22], with a large resolution ratio, e.g. [23, 1] and downscaling precipitation from tropical cyclones [59]. However, most of these related works focus on a single variables per model (note that [31] provided two model each per variable and is thus listed twice in the table). The variables of interest in all these works are related to properties of cloud and precipitation. While [59] showed a successful super resolution (recovering 10km from data coarsened to 100km) of tropical cyclone precipitation. To the best of our knowledge ML downscaling of tropical cyclones, which requires accounting for diﬀerent physics, across many channels and channel synthesis was not shown before.

The combined prediction of selected dynamical, thermodynamical and microphysical (cloud related) variables in concert marks a new capability of such models. It utility is demonstrated here by examining coherent structures and how all variables jointly downscaled in a physically consistent manner.

2 Descriptions of the architecture and the channels

Table S2 lists the input and output channels for the CorrDiﬀ model. Note that the two diﬀer both by pixel side and by the channels themselves. For single level variables, the input includes total column water vapor but lacks the maximum radar reﬂectivity which is present in the output, and vice versa. The input also includes pressure level variables at the 925, 850, 700 and 500 (hpa) levels.

18

Pixel side Single level channels

Input 36 x 36 Total column water vapor Temperature at 2 meter Eastward wind at 10 meter Northward wind at 10 meter Northward wind at 10 meter

Output 448 x 448 Maximum radar reﬂectivity Temperature at 2 meter Eastward wind at 10 meter

Pressure level channels Temperature Geopotential Eastward wind Northward wind

Table S2: A list of the input and output resolutions and channel for the CorrDiﬀ downscaling model. Input channels include the both single level variables and pressure level variables, the latter are used at 925, 850, 700 and 500 (hpa) levels.

Figure S1 shows the architecture of the Unet in CorrDiﬀ.

3 Localization by two-step formulation

Figure S2 (left) demonstrates the role of the two steps associated with CorrDiﬀ as a function of spatial scales. From the target data (blue), it is seen that the regression step learns mostly large spatial scales, leaving the small scales almost completely for the diﬀusion step. In addition, from Fig S2 (right), it is observed that the residual is quite localized. It seems that to fully resolve the residual at each spatial location, only 40km radius around that is needed, while for the target data there is long-range correlations up to 200km. This has important implications for training and sampling eﬃciency of diﬀusion models since one can deploy diﬀusion models with smaller UNet desnoing architectures to aggregate the local information. We leave further study of this for future research.

4 Examining sample diversity of CorrDiﬀ

In order to examine the realism of individual samples from CorrDiﬀ and their quality compared with the target data ﬁgure shows an animation of the target data (left) Reg (middle) and 20 generated samples of the CorrDiﬀ prediction of maximum radar reﬂectivity.

5 Comparison of simulated Typhoons with historical records

Although our out-of-sample data is limited to 2021, we can compare CorrDiﬀ simulated typhoons in the CWA region with historical records. The Japan Meteorological Agency best track data (JMA tracks) [4] includes the maximum windspeed (intensity) and radius of maximum windspeed (size) of typhoons in west paciﬁc for several decades. During the years 1980 to 2020 for (which we have ERA5 data available) and within the CWA domain, we identiﬁed 648 instances of typhoons with intensities of 30 m/s or greater in this time period. Panels (a) and (b) of ﬁgure S4 display the storm size and intensity, respectively, revealing the expected correction for ERA5 typhoons achieved through the application of CorrDiﬀ. One imperfection of CorrDiﬀ is that it shrinks all storms, including those with the correct size or those that were too small in the ERA5 input data (panel a). The main beneﬁt is an improvement in the windspeeds, removing most of the error between the ERA5 and the observed records for windspeeds up to 50 m/s (panel b); stronger storms have room for improvement. CorrDiﬀ generates a ﬁve-fold increase in the probability of hurricane-force winds exceeding 33 m/s (panel c). To the extent that JMA tracks can serve as ground truth, such distribution shift has signiﬁcant societal implications as these low-probability, high-impact events represent a substantial portion of the overall risk, underscoring the importance of accurate modeling and forecasting.

19

4 Res Blocks

Self attention

Conv Block

Down/up sample block

Concatenate

Concatenate

Concatenate

t

Figure S1: A sketch of the hierarchical UNet architecture adopted in both the regression model and the denoising diﬀusion model. Note, in the regression stage, time embedding is not used.

20

Spatial autocorrelation

Figure S2: Left column: power spectra, right column: spatial auto-correlation. Top to bottom: maximum radar reﬂectivity, 10m eastward wind, 10m northward wind and 2m temperature. This ﬁgure compares the original target x and the diﬀerence r = x y]. The diﬀerence has greatly reduced variance at large-scales and equivalently removes the long-range auto-correlations.

❊[x

−

|

21

Figure S3: Comparison of many samples of maximum radar reﬂectivity (right) with the prediction from the regression (Reg) and the truth (WRF) for several cloud regimes.

(a)

(b)

(c)

Figure S4: Comparison between ERA5, CorrDiﬀ (from ERA5) and observed records for all typhoons found in the domain with windspeed of 30 m/s or more in the years 1980-2020. Panel (a): abscissa: mean (dot) and one standard deviation (bars) of predicted radius of maximum winds for the ERA5 (red) and CorrDiﬀ (orange) storms, grouped by their observed values; ordinate: corresponding observed values. Panel (b) same as (a) but the maximum windspeed. Panel (c): The PDFs of all instances with typhoon of windspeed 30 m/s or greater in the years 1980-2020 in the CWA domain.

22

6 Energy eﬃciency and latency of CorrDiﬀ donwscaling inference

compared to WRF simulations

Comparing the performance of a statistical downscaling like CorrDiﬀ with a dynamical downscaling like the WRF-CWA is not straightforward. The former produces maps of a subset of channels at time t + 1 from a low resolution global forecast at t + 1, while the latter produces maps of the full state vector at time t + 1 from a low resolution global forecast at t using a numerical time-stepper where each time step is of the order of seconds.

Nonetheless, given that a global model like GFS is available, we can compare the compute time and energy required to obtain high resolution 1 hourly maps in Taiwan from the two approaches. Doing so, we compare the speed of CorrDiﬀ against the operational WRF run by CWA on their respective hardware. The CWA-WRF is run on Fujitsu FX-100 system, where each node is equipped with 32 SPARC64 Xifx CPU cores. A 13 hour deterministic CWA-WRF forecast (excluding data assimilation) is run on 928 CPU cores (across 29 nodes with a maximum system memory of 6.9GB per node) and takes about 20 minutes. CorrDiﬀ inference is run on a single NVIDIA RTX 6000 Ada Generation GPU, which takes 4.1 sec per downscaling sample. Given a global model 1 hour leadtime forecast, the CorrDiﬀ statistical downscaling on a single GPU is about 22 times faster than the dynamic downscaling that runs CWA-WRF on 928 CPUs. Moreover, CorrDiﬀ it is about 1130 times more energy eﬃcient. We note that our current implementation of CorrDiﬀ is far from optimized and does not utilize GPU parallelization and batching for generating many samples independently. A simple change to mixed-precision (ﬂoat 16) gains almost another factor 2 speedup, without any degradation energy eﬃciency compared with WRF-CWA. of the results, leading to about 38 Furthermore, given global model data (which both systems need) CorrDiﬀ can be run for the 13h on 13 GPUs obtaining about a 13x speedup for the 13h forecast used, over the above results (but with the same energy eﬃciency). We believe that GPU parallelization and batched inference will likely lead to even more signiﬁcant speed-up and energy improvements.

speed up and about 1,800

×

×

Hardware

Latency (sec/FH) Power (J/sec) Energy (kJ/FH)

WRF-CWA CorrDiﬀ, ﬂoat32 CorrDiﬀ, ﬂoat16

928 CPUs 1 GPU 1 GPU

91.38 4.1 2.4

15.15 300 300

1285.46 1.23 0.72

Table S3: A comparison of running the WRF model on the CWA system with CorrDiﬀ inference on a single NVIDIA RTX 6000 Ada Generation GPU. Latency is given per Forecast Hour (FH) and Power is given in Joule/sec (W) per a single hardware unit (a CPU or a GPU), while Energy is for the entire forecast system (928 CPU for WRF-CWA) per FH.

23

Supplementary Files

This is a list of supplementary  les associated with this preprint. Click to download.

SupplementaryInformation.pdf