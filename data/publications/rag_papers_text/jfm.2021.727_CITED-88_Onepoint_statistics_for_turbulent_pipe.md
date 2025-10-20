s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

J. Fluid Mech. (2021), vol. 926, A28, doi:10.1017/jfm.2021.727

One-point statistics for turbulent pipe ﬂow up to Reτ ≈ 6000

Sergio Pirozzoli1,†, Joshua Romero2, Massimiliano Fatica2, Roberto Verzicco3,4 and Paolo Orlandi1 1Dipartimento di Ingegneria Meccanica e Aerospaziale, Sapienza Università di Roma, Via Eudossiana 18, 00184 Roma, Italy 2NVIDIA Corporation, 2701 San Tomas Expressway, Santa Clara, CA 95050, USA 3Dipartimento di Ingegneria Industriale, Università di Roma TorVergata, Via del Politecnico 1, 00133 Roma, Italy 4Physics of Fluid Group, University of Twente, PO Box 217, 7500 AE Enschede, The Netherlands

(Received 23 March 2021; revised 5 August 2021; accepted 12 August 2021)

We study turbulent ﬂows in a smooth straight pipe of circular cross-section up to friction Reynolds number (Reτ) ≈ 6000 using direct numerical simulation (DNS) of the Navier–Stokes equations. The DNS results highlight systematic deviations from Prandtl friction law, amounting to approximately 2%, which would extrapolate to approximately 4% at extreme Reynolds numbers. Data ﬁtting of the DNS friction coefﬁcient yields an estimated von Kármán constant k ≈ 0.387, which nicely ﬁts the mean velocity proﬁle, and which supports universality of canonical wall-bounded ﬂows. The same constant also applies to the pipe centreline velocity, thus providing support for the claim that the asymptotic state of pipe ﬂow at extreme Reynolds numbers should be plug ﬂow. At the Reynolds numbers under scrutiny, no evidence for saturation of the logarithmic growth of the inner peak of the axial velocity variance is found. Although no outer peak of the velocity variance directly emerges in our DNS, we provide strong evidence that it should appear at Reτ (cid:2) 104, as a result of turbulence production exceeding dissipation over a large part of the outer wall layer, thus invalidating the classical equilibrium hypothesis.

Key words: pipe ﬂow, turbulence simulation, turbulence theory

1. Introduction Turbulent ﬂow in circular pipes has always attracted the interest of scientists, owing to its prominent importance in the engineering practice and because of the beautiful simplicity of the set-up. In this respect, the pioneering ﬂow visualizations of Reynolds †Email address for correspondence: sergio.pirozzoli@uniroma1.it

© The Author(s), 2021. Published by Cambridge University Press. This is an Open Access article, distributed under the terms of the Creative Commons Attribution licence (https://creativecommons. org/licenses/by/4.0/), which permits unrestricted re-use, distribution, and reproduction in any medium, provided the original work is properly cited.

926 A28-1

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

(1883) may be regarded as a milestone for the understanding of turbulent and transitional ﬂows. The most extensive experimental measurements of high-Reynolds-number pipe ﬂows have been carried out in modern times in the Princeton SuperPipe pressurized facility (Zagarola & Smits 1998; McKeon, Zagarola & Smits 2005; Hultmark, Bailey & Smits 2010). Those investigations have allowed scientists to measure the main ﬂow features such as friction and mean velocity proﬁles with high precision, and they currently constitute the most comprehensive database for the study of pipe turbulence. However, even the use of specialized microfabricated hot-wire probes could not provide fully reliable information about the viscous and buffer layers at high Reynolds numbers (Hultmark et al. 2012). Additional experimental studies of pipe turbulence have been carried out in the high-Reynolds-number actual ﬂow facility (Hi-Reff), a water tunnel with relatively large diameter, which allows for accurate estimation of friction (Furuichi et al. 2015, 2018). Recently, the Center for International Cooperation in Long Pipe Experiments (CICLoPE) facility of the University of Bologna (Fiorini 2017; Willert et al. 2017) has been set up, whose large diameter (approximately 1 m) offers a well-established turbulent ﬂow with relatively large viscous scales, thus granting higher spatial resolution. Flows in different facilities seem to have sensibly different properties in terms of friction and mean velocity proﬁles, which we will comment on.

Numerical simulation of pipe turbulence ﬂow has received less interest than other canonical ﬂows, the plane channel in particular, because of additional difﬁculties involved with the discrete solution of the Navier–Stokes equations in cylindrical coordinates, with special reference to the treatment of the geometrical singularity at the pipe axis. Early numerical simulations of turbulent pipe ﬂow were carried out by Eggels et al. (1994), at friction Reynolds number Reτ = 180 (Reτ = uτR/ν, with uτ = (τw/ρ)1/2 the friction velocity, R the pipe radius and ν the ﬂuid kinematic viscosity). Effects of drag reduction associated with pipe rotation were later studied by Orlandi & Fatica (1997). Higher Reynolds numbers (up to Reτ ≈ 1140) were reached by Wu & Moin (2008), which ﬁrst allowed one to observe a near logarithmic layer in the mean velocity proﬁle. Flow visualizations and two-point correlation statistics pointed to the existence of high-speed wavy structures in the pipe core region which are elongated in the axial direction, and whose streamwise and azimuthal dimensions do not change substantially with the Reynolds number, when normalized in outer units. Further follow-up direct numerical simulation (DNS) studies have been carried out by El Khoury et al. (2013), Chin et al. (2014) and Ahn et al. (2013). At present, the highest Reynolds number in pipe ﬂow (Reτ ≈ 3000) has been reached in the study of Ahn et al. (2015). Although no sizeable logarithmic layer is present yet at those conditions, some effects associated with signiﬁcant scale separation between inner- and outer-scale turbulence were observed, as the presence of a k−1 (k being the wavenumber in any wall-parallel direction) power-law ranges in the velocity spectra.

Despite inherent limitations in the Reynolds numbers which can be attained, DNS has the advantage over experiments of yielding immediate access to the near-wall region, and of allowing scientists to measure some ﬂow properties, e.g. the turbulence dissipation rate, which can hardly be measured in experiments. Hence, it is generally claimed that DNS data at increasing Reynolds numbers are needed to prove or disprove theoretical claims related to departure (or not) of the statistical properties of wall-bounded turbulence from the universal wall scaling (Cantwell 2019; Chen & Sreenivasan 2021; Monkewitz 2021). In this paper we thus present DNS data of turbulent ﬂow in a smooth circular pipe at Reτ ≈ 6000, which is two times higher than the previous state of the art. Relying on the DNS data, we revisit current theoretical inferences and discuss implications about possible trends in the extreme Reynolds number regime.

926 A28-2

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

2. The numerical dataset The code used for DNS is the spin-off of an existing solver previously used to study Rayleigh–Bénard convection in cylindrical containers at extreme Rayleigh numbers (Stevens et al. 2013). That code is in turn the evolution of the solver originally developed by Verzicco & Orlandi (1996), and used for DNS of pipe ﬂow by Orlandi & Fatica (1997). A second-order ﬁnite-difference discretization of the incompressible Navier–Stokes equations in cylindrical coordinates is used, based on the classical marker-and-cell method (Harlow & Welch 1965), with staggered arrangement of the ﬂow variables to remove odd–even decoupling phenomena and guarantee discrete conservation of the total kinetic energy in the inviscid ﬂow limit. Uniform volumetric forcing is applied to the axial momentum equation to maintain constant mass ﬂow rate in time. The Poisson equation resulting from enforcement of the divergence-free condition is efﬁciently solved by double trigonometric expansion in the periodic axial and azimuthal directions, and inversion of tridiagonal matrices in the radial direction (Kim & Moin 1985). An extensive series of previous studies about wall-bounded ﬂows from this group proved that second-order ﬁnite-difference discretization yields in practical cases of wall-bounded turbulence results which are by no means inferior in quality to those of pseudospectral methods (e.g. Moin & Verzicco 2016; Pirozzoli, Bernardini & Orlandi 2016). A crucial issue is the proper treatment of the polar singularity at the pipe axis. A detailed description of the subject is reported in Verzicco & Orlandi (1996), but basically, the radial velocity ur in the governing equations is replaced by qr = rur (r is the radial space coordinate), which by construction vanishes at the axis. The governing equations are advanced in time by means of a hybrid third-order low-storage Runge–Kutta algorithm, whereby the diffusive terms are handled implicitly, and convective terms in the axial and radial direction are handled explicitly. An important issue in this respect is the convective time step limitation in the azimuthal direction, due to intrinsic shrinking of the cells’ size toward the pipe axis. To alleviate this limitation we rely on implicit treatment of the convective terms in the azimuthal direction (Akselvoll & Moin 1996; Wu & Moin 2008), which enables marching in time with similar time step as in planar domains ﬂow in practical computations. In order to minimize numerical errors associated with implicit time stepping, in the present code explicit and explicit discretizations of the azimuthal convective terms are linearly blended with the radial coordinate, in such a way that near the pipe wall the treatment is fully explicit, and near the pipe axis it is fully implicit. The code was adapted to run on clusters of graphic accelerators (GPUs), using a combination of CUDA Fortran and OpenACC directives, and relying on the CUFFT libraries for efﬁcient execution of fast Fourier transforms (FFTs) (Ruetsch & Fatica 2014). The DNS were carried out on the Marconi-100 machine based at CINECA (Italy), relying on NVIDIA Volta V100 graphic cards. Speciﬁcally, 1024 GPUs were used for DNS-F. Numerical simulations are carried out with periodic boundary conditions in the axial (z) and azimuthal (θ) directions. The velocity ﬁeld is then controlled by two parameters, namely the bulk Reynolds number (Reb = 2Rub/ν, with R the pipe radius, ub the ﬂuid bulk velocity and ν its kinematic viscosity), and the relative pipe length, Lz/R. A list of the main simulations that we have carried out is given in table 1. The mesh resolution is designed based on well-established criteria in the wall turbulence community. In particular, the collocation points are distributed in the wall-normal direction so that approximately 30 points are placed within y+ ≤ 40 (y = R − r is the wall distance, and the + superscript is used to denote normalization with respect to uτ and ν), with the ﬁrst grid point at y+ ≈ 0.05. The mesh is progressively stretched in the outer wall layer in such a way that the mesh spacing is proportional to the local Kolmogorov length

926 A28-3

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

Dataset

Lz/R Mesh (Nθ × Nr × Nz)

Reb

λ

Reτ

T/τt

Line style

DNS-A DNS-B DNS-C DNS-C-SH DNS-C-LO DNS-C-FT DNS-C-FR DNS-C-FZ DNS-D DNS-E DNS-F

15 15 15 7.5 30 15 15 15 15 15 15

256 × 67 × 256 768 × 140 × 768 1792 × 270 × 1792 1792 × 270 × 986 1792 × 270 × 3944 3944 × 270 × 1792 1792 × 540 × 1792 1792 × 270 × 3944 3072 × 399 × 3072 4608 × 540 × 4608 9216 × 910 × 9216

5300 17000 44000 44000 44000 44000 44000 44000 82500 133000 285000

0.03700 0.02716 0.02136 0.02164 0.02128 0.02114 0.02132 0.02132 0.01836 0.01659 0.01428

180.3 495.3 1136.6 1144.2 1134.6 1131.0 1135.7 1135.7 1976.0 3028.1 6019.4

204.0 87.4 25.9 31.1 24.5 31.3 28.6 15.5 22.4 16.6 8.32

NA NA NA NA NA

Table 1. Flow parameters for DNS of pipe ﬂow. Here R is the pipe radius; Lz is the pipe axial length; Nθ, Nr and Nz are the number of grid points in the azimuthal, radial and axial directions, respectively; Reb = 2Rub/ν is the bulk Reynolds number; λ = 8τw/(ρu2 ) is the friction factor; Reτ = uτR/ν is the friction Reynolds number; b T is the time interval used to collect the ﬂow statistics; and τt = R/uτ is the eddy turnover time.

scale, which there varies as η+ ≈ 0.8y+1/4 (Jiménez 2018), and the radial spacing at the pipe axis is Δy+ ≈ 8.8. Additional details are provided in a speciﬁcally focused publication (Pirozzoli & Orlandi 2021). Regarding the axial and azimuthal directions, ﬁnite-difference simulations of wall-bounded ﬂows yield grid-independent results as long as Δx+ ≈ 10, R+Δθ ≈ 4.5 (Pirozzoli et al. 2016), hence the associated number of grid points scales as Nz ≈ Lz/R × Reτ/10, Nθ ∼ 2π × Reτ/4.5. All DNS have been carried out at Courant–Friedrichs–Lewy (CFL) number close to unity, based on the radial convective time step limitation. The CFL number along the axial direction is typically smaller by a τ) ranges from Δt+ = 0.55 in DNS-A factor two. The time step expressed in wall units (ν/u2 to Δt+ = 0.15 in DNS-F. According to the established practice (Hoyas & Jiménez 2006; Ahn et al. 2015; Lee & Moser 2015), the time intervals used to collect the ﬂow statistics are reported in terms of eddy-turnover times, τt = R/uτ. For reference, the time window used to collect the ﬂow statistics in DNS-F amounts to approximately 13.1 ﬂow-through times (Lz/ub time units).

The sampling errors for some key properties discussed in this paper have been estimated using the method of Russo & Luchini (2017), based on an extension of the classical batch means approach. The results of the uncertainty estimation analysis are listed in table 2, where we provide expected values and associated standard deviation for the friction factor (f), mean centreline velocity (UCL), peak axial velocity variance and its position (cid:3) (cid:2) (( IP and yIP, respectively), and the dissipation rate of axial velocity variance ((cid:7)11w). Here and elsewhere, capital letters are used to denote ﬂow properties averaged in the homogeneous spatial directions and in time, brackets denote the averaging operator, and lower-case letters to denote ﬂuctuations from the mean. We ﬁnd that the sampling error is generally quite limited, being larger in the largest DNS, which have been run for shorter times. In particular, in DNS-F the expected sampling error in friction, centreline velocity and peak velocity variance is approximately 0.5%, whereas it is approximately 1% for the wall dissipation. Additional tests aimed at establishing the effect of axial domain length and grid size have been carried out for the DNS-C ﬂow case, whose results are also reported in table 2. We ﬁnd that doubling the pipe length yields a change in the basic ﬂow properties of approximately 0.2%–0.3%, whereas halving it yields changes of approximately 1% in friction and peak velocity variance, and up to 10% in the wall

u2 z

926 A28-4

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

(cid:6)+ IP

+ y IP

+ CL

(cid:5)u2 z 0.03700 ± 0.15% 19.30 ± 0.087% 7.129 ± 0.26% 14.95 ± 0.24% 0.1168 ± 0.47% DNS-A 0.02716 ± 0.074% 21.81 ± 0.17% 7.352 ± 0.17% 14.28 ± 0.010% 0.1506 ± 0.21% DNS-B 0.02136 ± 0.13% 24.07 ± 0.18% 7.995 ± 0.29% 14.66 ± 0.073% 0.1697 ± 0.37% DNS-C DNS-C-SH 0.02164 ± 0.14% 24.09 ± 0.20% 8.071 ± 0.44% 14.37 ± 0.11% 0.1952 ± 0.54% DNS-C-LO 0.02128 ± 0.16% 24.17 ± 0.11% 7.965 ± 0.29% 14.62 ± 0.058% 0.1704 ± 0.40% DNS-C-FT 0.02114 ± 0.12% 24.28 ± 0.14% 7.948 ± 0.27% 14.66 ± 0.078% 0.1691 ± 0.34% DNS-C-FR 0.02132 ± 0.25% 24.10 ± 0.12% 7.886 ± 0.31% 14.41 ± 0.096% 0.1741 ± 0.60% DNS-C-FZ 0.02132 ± 0.21% 24.07 ± 0.26% 8.168 ± 0.38% 14.89 ± 0.14% 0.1727 ± 0.44% 0.01839 ± 0.25% 25.56 ± 0.34% 8.397 ± 0.43% 14.79 ± 0.098% 0.1822 ± 0.57% DNS-D 0.01658 ± 0.26% 26.47 ± 0.27% 8.681 ± 0.69% 14.87 ± 0.13% 0.1903 ± 0.93% DNS-E 0.01428 ± 0.36% 28.05 ± 0.35% 9.108 ± 0.72% 15.14 ± 0.20% 0.1993 ± 1.10% DNS-F

λ

Dataset

U

(cid:7)+ 11w

Table 2. Uncertainty estimation study: mean values of representative quantities and standard deviation of their (cid:6)+ estimates. Here λ is the friction factor; U IP is the peak axial velocity (cid:6) at the wall. variance and y

+ CL is the mean pipe centreline velocity; (cid:5)u2 z 11w is the dissipation rate of (cid:5)u2 z

IP is its distance from the wall; and (cid:7)+

+

dissipation. Hence, consistent with previous studies (Chin et al. 2010), we believe that the selected pipe length (Lz/R = 15) is representative of an inﬁnitely long pipe, at least for the purposes of the present study. In order to quantify uncertainties associated with numerical discretization, additional simulations have been carried out by doubling the grid points in the azimuthal, radial and axial directions. Based on the data reported in the table, after discarding the short pipe case, we can thus quantify the uncertainty due to numerical discretization and limited pipe length to be approximately 0.3% for the friction coefﬁcient and pipe centreline velocity, 0.6% for the peak velocity variance and 0.9% for the wall dissipation.

3. Results Qualitative information about the structure of the ﬂow ﬁeld is provided by instantaneous perspective views of the axial velocity ﬁeld, provided in ﬁgure 1. Although ﬁner-scale details are visible at the higher Re, the ﬂow in the cross-stream planes is always characterized by a limited number of bulges distributed along the azimuthal direction, which closely recall the proper orthogonal decomposition (POD) modes identiﬁed by Hellström & Smits (2014), and which correspond to alternating intrusions of high-speed ﬂuid from the pipe core and ejections of low-speed ﬂuid from the wall. Streaks are visible in the near-wall cylindrical shells, whose organization has clear association with the cross-stream pattern. Speciﬁcally, regardless of the Reynolds number, R-sized low-streaks are observed in association with large-scale ejections, whereas R-sized high-speed streaks occur in the presence of large-scale inrush from the core ﬂow. At the same time, smaller streaks scaling in wall units appear, corresponding to buffer-layer ejections/sweeps. Hence, organization of the ﬂow on at least two length scales is apparent here, whose separation increases with Reτ. (3.1)

926 A28-5

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

(a)

(b)

(c)

DNS-A Reτ=180

DNS-B Reτ=495

DNS-C Reτ=1137

(d)

(e)

( f )

DNS-D Reτ=1976

DNS-E Reτ=3028

DNS-F Reτ=6019

Figure 1. Instantaneous axial velocity contours (colour scale from blue to red) in turbulent pipe ﬂow as obtained from DNS. Contours are shown on a cross-stream plane and on a near-wall cylindrical shell (y+ ≈ 15).

A correlation generally used for smooth pipes is the Prandtl friction law, 1/λ1/2 = Alog10

(Rebλ1/2) − B,

√

where A = log10/(2k 2), with k being the von Kármán log-law constant. The standard values A = 2.0, B = 0.8, were derived by ﬁtting the experimental data of Nikuradse (1933). Reynolds-number-dependent corrections to the standard friction law were introduced by McKeon et al. (2005) in order to improve the ﬁtting of the SuperPipe data. Figure 2 shows overall agreement of all DNS and experimental data with the Prandtl law. However, closer scrutiny (see the ﬁgure insets) highlights some scatter. Regarding DNS, all datasets overshoot the Prandtl law at low Reynolds number, although to a quite different extent. In fact, the data of Wu & Moin (2008), El Khoury et al. (2013) and Chin et al. (2014) exceed the theoretical values by up to 4%, whereas our data tend to be much more consistent with those of Ahn et al. (2015). We believe that this difference may be related to different grid resolution in the azimuthal direction, which was R+Δθ = 7–8 in those previous studies, and 4–5 in our DNS. Our data in fact show minimal overshoot at low Reynolds number, and consistent undershoot from Prandtl law by approximately 2%. Regarding experiments, SuperPipe data typically tend to lie above the theoretical curve by approximately 2%, whereas the CICLoPE and Hi-Reff data tend to fall short of it. Although the range of data overlap is not extensive, it appears that DNS data tend to be more consistent with the CICLoPE and Hi-Reff data than with other datasets. Fitting the current DNS data with a functional relationship as (3.2), yields A ≈ 2.102, B ≈ 1.148, with an inferred value of the von Kármán constant of k = 0.387 ± 0.004, with uncertainty estimates based on 95% conﬁdence bounds from the curve-ﬁtting procedure. This value is extremely close to that suggested by Furuichi et al. (2018), who reported k = 0.386 as an average value over a very wide range of Reynolds numbers, and also very close to values reported in boundary layers (Nagib & Chauhan 2009) and channels (Lee & Moser 2015).

926 A28-6

(3.2)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

(a)

0.040

(b)

0.050

0.035

0.030

1 –

l t d n a r P

0.06

0.04

0.02

0

0.045

0.040

0.035

1 –

l t d n a r P

0.06

0.04

0.02

0

λ

0.025

0.020

λ / λ

–0.02

–0.04

–0.06

0

100000

200000

300000

0.030

0.025

0.020

λ / λ

–0.02

–0.04

–0.06

104

105

106

107

0.015

0.015

0.010

0

100000

200000

300000

104

105

106

107

Reb

Reb

Figure 2. Friction factor as a function of bulk Reynolds number, in linear (a) and in semilogarithmic (b) scale. Circles denote present DNS data, other symbols are deﬁned in table 3. The solid line corresponds to the classical Prandtl friction law as given in (3.2), whereas the dashed grey line corresponds to a ﬁt of the DNS data. Relative deviations with respect to the Prandtl friction law are shown in the insets.

Source

Type

Reτ range

Symbols

Wu & Moin (2008) El Khoury et al. (2013) Chin et al. (2014) Ahn et al. (2013), Ahn et al. (2015) Durst, Jovanovi´c & Sender (1995) Swanson et al. (2002) Fiorini (2017) Willert et al. (2017) Nagib et al. (2017) McKeon et al. (2005) Hultmark et al. (2012) Furuichi et al. (2015), Furuichi et al. (2018) Schultz & Flack (2013) Lee & Moser (2015)

DNS DNS DNS DNS EXP EXP EXP EXP EXP EXP EXP EXP EXP (channel) DNS (channel)

180, 1140 180–1000 180–2000 180-3000 250 170–1500 3000–35000 5400–40000 8000–40000 1800–32900 2000–20000 200–53000 1000–6000 180–5200

Table 3. List of other references for data used in the paper.

If this trend is extrapolated, deviations of approximately 4% from the standard Prandtl law would result at Reb = 107.

The mean velocity proﬁle in turbulent pipes has received extensive attention from theoretical studies, much of the early debate being focused on whether a log law or a power law better ﬁts the experimental results (Barenblatt, Chorin & Prostokishin 1997), mainly carried out in the SuperPipe facility (Zagarola & Smits 1998; McKeon et al. 2005). Recent studies have highlighted the need for corrections to the baseline log law in order to accurately describe the velocity proﬁle throughout the log layer into the core part of the ﬂow (Luchini 2017; Cantwell 2019; Monkewitz 2021). In ﬁgure 3, we show the series of velocity proﬁles computed with the present DNS, compared with previous DNS and experimental data. Overall, good agreement is observed across various sources as far as the inner and the overlap regions are concerned, with data gradually approaching a logarithmic distribution, here identiﬁed by visual ﬁtting as U+ = 1/klogy+ + 4.53, using the value of k = 0.387 determined from friction data. This is quite close to estimates

926 A28-7

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

(a)

30

(b)

60

25

50

20

40

U+

15

2

30

10

5

g o l

0

+ U – + U

–2

–4

20

10

0 100

101

100

102 y+

101

102

103

103

104

104

0 100

101

102 y+

103

Figure 3. Inner-scaled mean velocity proﬁles obtained with our DNS (a), and compared with previous DNS = logy+/0.387 + 4.53, are and experiments (b). Deviations from the assumed logarithmic wall law, U highlighted in the inset of panel (a). For greater clarity, proﬁles in panel (b) are offset in the vertical direction by ﬁve wall units steps. Lines denote present DNS data, with colour code as in table 1, and symbols denote data from other authors, as in table 3.

+ log

based on direct ﬁtting of the mean velocity proﬁle in pipe ﬂow (Marusic et al. 2013), which yielded U+ = 1/0.391logy+ + 4.34. The DNS velocity proﬁles for Reτ ≥ 103 follow this distribution with deviations of no more than 0.1 wall units from y+ ≈ 30 to y/R ≈ 0.15, whence the core region develops. Differences with respect to previous DNSs are concentrated in the core region, which seemingly stronger wake in some datasets, including our own, Wu & Moin (2008) and Ahn et al. (2013), and weaker in others (El Khoury et al. 2013; Chin et al. 2014), reﬂecting previously noted differences in the friction coefﬁcient. Especially satisfactory is the excellent agreement between our DNS-E velocity proﬁle and the data of Ahn et al. (2015) at Reτ ≈ 3000. Comparison of our DNS dataset with experimental data also shows overall good agreement, although some differences are quite clear in the core region, in which SuperPipe experiments consistently yield lower U+, which translates into lower friction.

More reﬁned information on the behaviour of the mean velocity proﬁle can be gained

from inspection of the log-law diagnostic function

Ξ = y

+

dU

+/dy

+,

which is shown in ﬁgure 4, and whose constancy would imply the presence of a genuine logarithmic layer in the mean velocity proﬁle. The ﬁgure supports universality of the inner-scaled axial velocity for Reτ (cid:2) 103, up to y+ ≈ 100, where Ξ attains a minimum, and the presence of an outer maximum at y/R ≈ 0.6. Between these two sites the distribution is roughly linear, as can be better appreciated in ﬁgure 4(b), with nearly constant slope when expressed in outer coordinates. Approximate linear variation of the diagnostic function in channel ﬂow was observed by Jiménez & Moser (2007), who, based on reﬁned overlap arguments expressed by Afzal & Yajnik (1973), proposed the following ﬁt:

β

Ξ = 1 k

+ α y R

+

,

Reτ where α, β are adjustable constants, and k is the von Kármán constant. Here we ﬁnd that the set of constants k = 0.387, α = 2.0, β = 0, yields overall good approximation of the pipe DNS data. The consequence is that a genuine logarithmic layer would only be attained at inﬁnite Reynolds number. In this respect, SuperPipe data seem to suggest the formation

926 A28-8

104

(3.3)

(3.4)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

(a)

6

(b)

6

5

5

+

4

4

y d /

+ U d +

y

3

2

3

2

1

1

0 100

101

102

103

104

0

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

y+

y/R

Figure 4. Log-law diagnostic function as deﬁned in (3.3), expressed as a function of inner-scaled (a) and outer-scaled (b) wall distance. The dashed horizontal line denotes the inverse Kármán constant, 1/0.387, and the dash–dotted lines in panel (b) denote the linear ﬁt (3.4), with k = 0.387, α = 2.0, β = 0. Lines denote present DNS data, with colour code as in table 1, and symbols denote SuperPipe data (McKeon et al. 2005) at Reτ = 1825,3328,6617,10914,19119,32870.

(a)

1.4

(b)

1.4

1.2

1.2

1.0

1.0

U/ub

0.8

0.6

0.8

0.6

0.4

0.4

0.2

0.2

0

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

0

0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

y/R

y/R

Figure 5. Mean velocity proﬁles in outer scaling. Data of ﬂow case DNS-E (a) are compared with SuperPipe data at Reτ = 3328 and Reτ = 3334, and data of ﬂow case DNS-F (b) with SuperPipe data at Reτ = 5411 and Reτ = 6617.

of a plateau at Reτ (cid:2) 104, although the scatter of points is quite signiﬁcant. Hence, DNS at higher Reynolds number would be most welcome to conﬁrm or refute our ﬁndings, and possibly determine more accurate values of the extended log-law constants in (3.4).

Comparison with SuperPipe data is presented in outer units in ﬁgure 5, limited to the higher Reτ cases. Despite differences in the Reynolds number, the velocity proﬁles now agree very well, throughout the outer layer. This observation would suggest problems with correct estimation of the friction velocity which, however, seems unlikely both in DNS, in which we independently evaluate friction velocity by computing the wall derivative of the velocity proﬁle and from momentum balance, and in experiments, as measurements of the pressure drop are regarded to have low uncertainty. Hence, reasons for this discrepancy are not known, and additional experiments as those currently carried out in the large CICLoPE facility would be especially useful and welcome. Unfortunately, velocity proﬁles along the full radial span are not available at the moment for that facility.

The structure of the core region is examined in detail in ﬁgure 6, where the mean velocity proﬁles are shown in defect form. Although full outer-layer similarity is not

926 A28-9

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

(a)

20

(b)

20

15

15

+ U – +

10

10

L C U

5

5

0

0.2

0.4

0.6

0.8

1.0

0 10–3

10–2

10–1

y/R

y/R

Figure 6. Defect velocity proﬁles for DNS and experiments, in linear (a) and semilogarithmic (b) scale. The − U+ = 8.0(1 − y/R)2), and the dashed purple dashed grey line marks a parabolic ﬁt of the DNS data (U line the outer-layer logarithmic ﬁt U

+ CL

+ CL

− U+ = 0.961 − 1/0.387log(y/R).

reached at the conditions of our DNS study (also see the inset of ﬁgure 3a), scatter across the Reynolds number range and with respect to SuperPipe proﬁles for y/R ≥ 0.2 is no larger than 5%. As suggested by Pirozzoli (2014), the core velocity proﬁles can be closely approximated with a simple quadratic function, reﬂecting near constancy of the eddy viscosity. In particular, we ﬁnd that the formula

+ = CO (1 − y/R)2 ,

+ CL

− U

(3.5) ﬁts the DNS data with CO = 8.0 well, and it smoothly connects at y/R ≈ 0.2 with the logarithmic proﬁle expressed in outer form, += − 1 k where again k = 0.387, and data ﬁtting yields B = 0.961. While, of course, better descriptions of the core velocity proﬁles are possible based on more elaborate functional relationships (Luchini 2017), the composite proﬁle matching equations (3.5) and (3.6) yields a reasonable representation of the whole outer-layer mean velocity proﬁle within the scatter of available data.

U

+ CL

−U

log(y/R) + B,

U

Finer evaluation of similarities and differences between DNS and experiments is provided in ﬁgure 7, where we show the mean centreline velocity, UCL, normalized by the friction velocity (ﬁgure 7a), and by the bulk velocity (ﬁgure 7b), as a function of the friction Reynolds number. Consistently with theoretical expectations (e.g. Monkewitz 2021), data suggest logarithmic increase with Reτ according to

U

+ CL

= 1 kCL

logReτ + BCL,

where we ﬁnd kCL = k = 0.387 as for the friction law, and BCL = 5.85. For convenience, the trend of ub/uτ is also presented, having in fact the same logarithmic growth with Reτ. With some previously noted differences, all pipe ﬂow DNSs seem to exhibit a consistent trend in the accessible range. While the trend is very similar at low Reynolds + number, experimental data yield consistently lower values of U CL, especially those from the SuperPipe. At Reynolds numbers higher than approximately Reτ = 104, experiments seem to suggest milder growth rate, although signiﬁcant differences emerge between the

926 A28-10

100

(3.6)

(3.7)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

(a)

36

(b)

1.40

32

1.35

1.30

τ u /

L C U

28

24

20

b

u /

L C U

1.25

1.20

1.15

1.10

16

1.05

1.00

102

103

104

105

102

103

104

105

Reτ

Reτ

Figure 7. Mean pipe centreline velocity (UCL) expressed in inner (a) and in outer (b) units. The dashed grey line corresponds to a ﬁt of the DNS data. The DNS data are shown as circle symbols, and the corresponding logarithmic ﬁts are shown as thick dashed lines. Purple lines and symbols are used for the bulk velocity, ub. For the nomenclature of other symbols, refer to table 3.

SuperPipe and the Hi-Reff datasets. Hence, whether this is the result of a change of behaviour at high Reynolds number, or some form of shortcoming of experiments, is difﬁcult to say. As a result of the observed identity (or very close vicinity) of the von Kármán constant for the centreline and for the bulk velocity, ﬁgure 7(b) highlights that their ratio approaches unity at large Re, supporting the inference that pipe ﬂow asymptotes to plug ﬂow in the inﬁnite-Reynolds-number limit (Pullin, Inoue & Saito 2013). Regarding that study, it is worthwhile noticing that one of the assumptions made in the analysis is that the wall-normal location of the onset of the logarithmic region is either ﬁnite, or increases no faster than Reτ. Interpreting the near-wall minimum of the diagnostic function in ﬁgure 4 as the root of the (near) logarithmic layer, our data support that assumption well. Whereas the curvature of the core velocity proﬁle is not changing substantially when expressed in wall units (see ﬁgure 6), it would become vanishingly small when expressed in outer units. However, as ﬁgure 7(b) suggests, this trend is extremely slow. Interestingly, again despite some scatter, DNS and experiments here seem to indicate a common trend with overall monotonic decrease, perhaps with a ‘bump’ in the range of Reynolds numbers in the low thousands. The DNS data points at the highest Reynolds numbers (DNS-D, DNS-E, DNS-F) now appear to be in good agreement with SuperPipe experiments, which is in line with the previously noted agreement of the outer-scaled mean velocity proﬁles.

The distributions of the velocity variances along the coordinate directions are shown in ﬁgure 8, in inner scaling. As is now well established (Marusic & Monty 2019), the longitudinal (uz) and spanwise (uθ) velocity ﬂuctuations show slow increase with the Reynolds number, with commonly accepted logarithmic growth as after Townsend’s attached eddy model (Townsend 1976). On the other hand, the wall-normal velocity ﬂuctuations seem to level off to a maximum value of approximately 1.30. It is remarkable that the general growth of the longitudinal and spanwise ﬂuctuations is more evident in the outer layer, and in fact it has long been argued about the possible occurrence of a (cid:6), besides the primary buffer-layer peak. Experiments carried out secondary peak of (cid:5)u2 z in the SuperPipe (Hultmark et al. 2012) and CICLoPE (Willert et al. 2017) facilities indeed support the occurrence of such a peak at Reτ (cid:2) 104. Whereas DNS data are not at sufﬁciently high Reτ to show this secondary peak, it appears that in DNS-F the axial velocity variance has attained a nearly horizontal inﬂectional point at y+ ≈ 140. Comparison with the Reτ ≈ 3000 DNS of Ahn et al. (2015) shows overall good agreement

926 A28-11

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

(a)

10

(b)

10

8

8

2

τ u / (cid:3) 2

6

6

i

u (cid:2)

4

4

2

2

0 100

101

102 y+

103

104

0 100

101

102 y+

103

Figure 8. Distribution of velocity variances (a) and comparison of cases DNS-E, DNS-F with reference DNS and experiments (b). In panel (a), the short dashed lines denote the axial velocity variance ((cid:5)u2 (cid:6)), the solid lines z denote the radial velocity variance ((cid:5)u2 (cid:6)), and the long dashed lines denote the azimuthal velocity variance r ((cid:5)u2

θ(cid:6)). For colour codes in DNS data, see table 1, and for nomenclature of symbols, see table 3.

of all turbulence intensities. Comparison with SuperPipe data at Reτ = 3000 is also very good, with the exception of the near-wall peak which is likely to be overestimated in experiments. The DNS-F data seem to be well bracketed by SuperPipe and CICLoPE measurements at nearby Reynolds numbers, and also compare very well with experimental data for plane channel ﬂow (Schultz & Flack 2013).

Distributions of the turbulent shear stress are shown in ﬁgure 9. As is well established (e.g. Lee & Moser 2015), the shear stress proﬁles tend to become ﬂatter at higher Reτ, the peak value rises towards unity, and its position moves farther from the wall, in inner units. In particular, exploiting mean momentum balance and assuming the presence of a logarithmic layer in the mean axial velocity, the following prediction follows for the position of the turbulent shear stress peak (Afzal 1982):

(cid:4)

y

+ m

(cid:9)

Reτ k

,

which is intermediate between inner and outer scaling. This observation has led some authors to argue about the relevance of a ‘mesolayer’ (e.g. Long & Chen 1981; Wei et al. 2005). The asymptotic relationship (3.8) (with k = 0.387) is satisﬁed with good accuracy starting at Reτ ≈ 103, reﬂecting the onset of a near logarithmic layer. Similar results were obtained by Chin et al. (2014), by processing the mean velocity proﬁles obtained in the experiments of Hultmark et al. (2013).

The behaviour of the Reynolds stresses when expressed as a function of the outer-scaled wall distance, which is shown in ﬁgure 10, is also of great theoretical interest. In fact, according to the attached-eddy model (Townsend 1976; Marusic & Monty 2019), the wall-parallel velocity variances are expected to decline logarithmically with the wall distance in the outer layer, hence

(cid:5)

(cid:6)

(cid:5)

(cid:6)

u2 z

= B1 − A1 log(y/R),

u2 θ

= B3 − A3 log(y/R),

where Ai, Bi are universal constants. Regarding the axial stress, Marusic et al. (2013) argued that SuperPipe data at the highest available Reynolds number are best ﬁt with A1 = 1.23, B1 = 1.56, with a sensible logarithmic layer only emerging at Reτ > 104, 926 A28-12

104

(3.8)

(3.9a,b)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

(a)

2

τ u / (cid:3)

r

u

z

u (cid:2)

1.0 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1 0 100

(b)

ym

+

103

102

101

101

102 y+

103

104

102

103

Reτ

104

105

Figure 9. Distributions of turbulent shear stress (a) and its peak position at various Reτ (b). In panel (b) the circles denote the present DNS data, the squares the data of Hultmark et al. (2013), as processed by Chin et al. (2014), and the dashed line the theoretical estimate (3.8). For colour codes in DNS data, see table 1.

(a)

τ2 u / (cid:3) z2 u (cid:2)

10 9 8 7 6 5 4 3 2 1 0 104

103

102 y/R

101

100

(b)

τ2 u / (cid:3) θ2 u (cid:2)

3.0

2.5

2.0

1.5

1.0

0.5

0 104

103

102 y/R

101

100

Figure 10. Axial (a) and azimuthal (b) turbulent stresses as a function of outer-scaled wall distance. In panel (a), symbols denote SuperPipe data (Hultmark et al. 2012) at Reτ = 1985,3334,5411,10480,20250,37690, and the dashed grey line the corresponding ﬁt, (cid:5)u2 (cid:6) = 1.61–1.25log(y/R). In panel (b), the dashed coloured z lines denote DNS data of channel ﬂow (Lee & Moser 2015) at Reτ = 550,1000,2000,5200, and the dashed grey line the ﬁt of the DNS data, (cid:5)u2

θ(cid:6) = 1.0–0.40log(y/R). For colour codes in DNS data, see table 1.

in the range of wall distances 3Re1/2 τ ≤ y+ ≤ 0.15Reτ. The DNS data only show the formation of a near logarithmic layer farther away from the wall, which is not where it is expected from theoretical arguments. Hence, little can be said in this respect. The azimuthal velocity variance, shown in ﬁgure 10(b), has a more benign behaviour, and it features clear logarithmic layers even at modest Reτ. Fitting the DNS data yields A3 = 0.40, B3 = 1.0, which is very close to what is found in channels (Bernardini, Pirozzoli & Orlandi 2014; Lee & Moser 2015). Measurements of pipe ﬂow carried out in the CICLoPE facility (Örlü et al. 2017) yielded A3 = 0.63, B3 = 1.21, hence much larger values than in DNS. Possible overestimation of the wall-normal and azimuthal Reynolds stresses was in fact acknowledged by the authors of that paper.

Quantitative insight into Reynolds number effects is provided by inspection of the amplitude of the inner peak of the axial velocity variance, which we show in ﬁgure 11. The general theoretical expectation is that the peak grows logarithmically with Reτ owing to the increasing inﬂuence of distant, inactive eddies (Marusic & Monty 2019). However, some

926 A28-13

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

(a)

11

(b)

10

w+ 1 1

100

Reτ Reτ

–0.282

–1.07

τ2 u /

P I

(cid:3) z2 u (cid:2)

9

8

7

ε - 4 / 1

,

K+ P

P - 4 / 1

10–1

10–2

10–3

6 101

102

Reτ

103

104

10–4

101

102 Reτ

Figure 11. Magnitude of inner peak of axial velocity variance (a), peak turbulence production (PPK, red) and wall dissipation of axial velocity variance ((cid:7)11w, black) (b). For colour codes in DNS data, see table 1, and for nomenclature of symbols, see table 3. In panel (a) the dashed grey line marks the DNS data ﬁt, (cid:5)u2 = z 0.67logReτ + 3.3, the dashed purple line denotes the defect power law of Chen & Sreenivasan (2021) and the dash–dotted line the logarithmic law of Marusic, Baars & Hutchins (2017), (cid:5)u2 = 0.63logReτ + 3.8. z In panel (b), the dot–dashed and dotted lines denote ﬁts of PPK and (cid:7)11w in their tendency to the respective assumed asymptotic values.

(cid:6)+ IP

recent experimental results (Willert et al. 2017), and theoretical arguments (Chen & Sreenivasan 2021), suggest that such growth should eventually saturate. Although the difference between slow logarithmic growth and the attainment of an asymptotic value is quite subtle in practice, the theoretical interest is high, as in the latter case universality of wall scaling would be eventually restored. Within the investigated range of Reynolds numbers, our DNS data in fact support continuing logarithmic increase. Comparison with channel data (Lee & Moser 2015) shows some difference, which might result from stronger geometrical conﬁnement of distant eddies in the pipe geometry. However, differences tend to becomes smaller at higher Reτ. In quantitative terms, we ﬁnd the slope of logarithmic increase to be approximately 0.67, a bit steeper than found in channel ﬂow DNS (Lee & Moser 2015, approximately 0.64), and then suggested from a collection of DNS and experiments (approximately 0.63 (Marusic et al. 2017)). Experimental data for pipe ﬂow are quite scattered, as SuperPipe experiments yield an unrealistically decreasing trend (Hultmark et al. 2012), particle image velocimetry (known as PIV) measurements taken in the CIPLoPE facility (Willert et al. 2017) suggest saturation of the growth, whereas hot-wire measurements in the same facility support continued logarithmic growth (Fiorini 2017). The theoretical predictions of Chen & Sreenivasan (2021) (see the dashed purple line of ﬁgure 11a) seem to conform well with channel ﬂow DNS data and with the experiments of Willert et al. (2017).

While our DNS data cannot be used to directly evaluate the theoretical predictions owing to limited achievable Reynolds number, they can be used to better scrutinize the foundations of the theoretical arguments. The main argument made by Chen & Sreenivasan (2021), although not thoroughly justiﬁed in our opinion, was that since turbulence kinetic energy production is bounded, the wall dissipation must also stay bounded. Hence, let P = −(cid:5)uzur(cid:6)dU/dr be the turbulence kinetic energy production rate, and (cid:7)11 = ν(cid:5)|∇uz|2(cid:6) be the dissipation rate of the axial velocity variance, those authors ﬁrst argue that the wall limiting value of (cid:7)11 should scale as

(cid:7)11

+ w

= 1/4 − β/Re1/4

τ

,

926 A28-14

103

(cid:6)+ IP

(3.10)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow with β a suitable constant. In ﬁgure 11 we explore deviations of (cid:7)w and of the peak turbulence kinetic energy production, say PPK, from their asymptotic value, namely 1/4. According to analytical constraints (Pope 2000), we ﬁnd that production tends to its asymptotic value quite rapidly, as approximately 1/Reτ. Consistent with (3.10), the wall dissipation also tends to 1/4, more or less at the predicted rate, thus empirically validating the ﬁrst assumption. The next argument advocated by Chen & Sreenivasan (2021) is that wall balance between viscous diffusion and dissipation and Taylor series expansion of the axial velocity variance near the wall yields

(cid:5)u2 z

(cid:6)+ ∼ (cid:7)+

11wy

+2,

(3.11)

+ whence, from assumed invariance of the peak location of (cid:5)u2 (cid:6) (say, y IP), saturation of z growth of the peak velocity variance would follow. Table 2 suggests that this second assumption is in fact violated, as the position of the peak slightly increases with Reτ, with non-negligible effect on the peak variance as it appears in squared form in (3.11). As a consequence, logarithmic growth of the peak velocity variance still holds, at least in the range of Reynolds numbers currently accessible to DNS.

A secondary, outer-layer peak of the axial velocity variance was observed in the SuperPipe experiments of Hultmark et al. (2012), which relied on nanoscale thermal anemometry probes. Later experiments carried out in the CICLoPE facility (Örlü et al. 2017), using custom-made X-wire probes, raised doubts about the existence of a genuine outer peak, and in general prompted further high-quality data to ascertain whether it exists beyond measurement uncertainty. Particle image velocimetry measurements also carried out in the CICLoPE facility (Willert et al. 2017), did show an outer peak that develops and moves away from the inner peak with increasing Reynolds number. Hence, it is clear that this issue is not deﬁnitely settled in experiments. Although no distinct outer peak of the axial velocity variance is found at the Reynolds numbers accessed in the present DNS study, it is nevertheless instructive to explore the scaling of the velocity ﬂuctuations in the range of wall distances where the peak is expected to occur. For that purpose, we consider the outer position where the second logarithmic derivative of the velocity variance vanishes, which in the present DNS ranges from y+ ≈ 115 for DNS-A, to y+ ≈ 140 for DNS-F. Weak dependence of the inner-scaled outer peak position on Reτ, although at much higher Reynolds number, was also noticed by Hultmark et al. (2012). The resulting distribution is shown in ﬁgure 12. All DNS data fall nicely on a logarithmic ﬁt, and they seem to connect smoothly to the experimental results, whose scatter and uncertainty is expected to be much less than for the inner peak. Experiments indicate a change of behaviour to a shallower logarithmic dependence with slope of approximately 0.63 (Pullin et al. 2013; Fiorini 2017), which would be very close to the growth rate of the inner peak (see ﬁgure 11). The ﬁgure suggests that veriﬁcation of this effect would require Reτ of approximately 104.

As pointed out by Hultmark et al. (2012), the formation and growth of an outer peak of the axial velocity variance has important theoretical and practical implications. From the modelling standpoint, no current Reynolds-averaged Navier–Stokes (RANS) model is capable of predicting non-monotonic behaviour of Reynolds stresses outside the buffer layer. From the fundamental physics standpoint, the presence of an outer peak is suggestive of violation of equilibrium between turbulence production and dissipation. The DNS allows us to substantiate this scenario, and for that purpose in ﬁgure 13, we show the relative excess of turbulent kinetic energy production (P) over its total dissipation rate, here deﬁned as D = ν(cid:5)ui∇2ui(cid:6), which lumps together dissipation rate and viscous diffusion. Data conﬁrm the presence of a near-universal region conﬁned to the buffer layer (say,

926 A28-15

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

8

6

τ2 u /

P O

(cid:3) z2 u (cid:2)

4

2

102

103

104

105

Reτ

Figure 12. Magnitude of outer peak of axial velocity variance as a function of Reτ. Lines and symbols as in = 1.33logReτ − 5.61, and the purple line tables 1 and 3. The dashed grey line marks the DNS data ﬁt, (cid:5)u2 z denotes the logarithmic ﬁt given by Pullin et al. (2013).

(cid:6)+ OP

(a)

0.50

(b)

0.50

0.25

0.25

1

0

0

– + D / + P

–0.25

–0.50

–0.25

–0.50

–0.75

–0.75

–1.00

100

101

102 y+

103

104

–1.00

0

0.2

0.4

y/R

0.6

0.8

Figure 13. Excess of turbulence kinetic energy production over dissipation as a function of inner-scaled (a) and outer-scaled (b) wall distance. Lines as in table 1.

8 (cid:3) y+ (cid:3) 35), in which production exceeds dissipation by up to 40%. Data also show the onset, starting from DNS-B, of another region farther from the wall with positive unbalance, whose inner limit is constant in inner units, at y+ = 100, and whose outer limit tends to become constant at high Reτ in outer units, at y/R ≈ 0.4. The peak unbalance at high Reynolds number is approximately 17%, and its position seems to scale more in inner than in outer units. Turbulence kinetic energy production excess in the presence of a (near) logarithmic mean velocity proﬁle can be interpreted by recalling that only part of the axial velocity ﬂuctuations which are generated correlates with wall-normal velocity ﬂuctuations to yield active motions (Townsend 1976), hence the extra production feeds inactive motions, which do not convey contribution to the turbulent shear stress. This ﬁnding clearly indicates that at high enough Reynolds number the outer wall layer becomes a dynamically active part of the ﬂow, having the potential to transfer energy both to the core ﬂow, and towards the wall, in the form of imprinting on the near-wall layer (Marusic & Monty 2019).

926 A28-16

1.0

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

4. Concluding comments Although DNS of wall turbulence is still conﬁned to a moderate range of Reynolds numbers, it is beginning to approach a state in which some typical phenomena of the asymptotically high-Re emerge. Given its ability to resolve the near-wall layer, DNS lends itself to testing theories of wall turbulence and to in-depth scrutiny of experimental data. In this work, DNS of ﬂow in a smooth pipe has been carried out up to Reτ ≈ 6000, which, although still far from what achievable in experimental tests, allows us to uncover a number of interesting issues, in our opinion. First, we have noted that DNS data fall systematically short of the classical Prandtl friction law, by as much as 2%. This evidence is not consistent with data from the SuperPipe facility, although other recent data from the CICLoPE and Hi-Reff facilities seem to yield similar trends. The DNS data ﬁtting suggests that a logarithmic law as (3.2) still holds, however, with a von Kármán constant k ≈ 0.387, which matches extremely well the value quoted by Furuichi et al. (2018), and which would reconcile pipe ﬂow with plane channel and boundary layer ﬂows, thus corroborating claims made by Marusic et al. (2013). A logarithmic proﬁle with k ≈ 0.387 ﬁts the mean axial velocity distributions for 30 ≤ y+ ≤ 0.15Reτ well, although linear deviations are clearly visible, as argued by Afzal & Yajnik (1973) and Luchini (2017), which when taken into account yield an excellent representation of the velocity proﬁles up to y/R ≈ 0.5. It is remarkable that the same value of the von Kármán constant also ﬁts the mean centreline velocity distribution well (see ﬁgure 7), which is found to grow logarithmically throughout the range of Reτ under investigation. This ﬁnding is quite reasonable as it corroborates that the eventual state of turbulent ﬂow in a pipe should be plug ﬂow, as argued by Pullin et al. (2013), hence UCL → ub as Reτ → ∞. This would, however, seemingly contrast with recent measurements made in the CICLoPE facility (Nagib et al. 2017), which rather suggest a different von Kármán constant for the bulk and the centreline velocity. + Experimental data at Reτ (cid:2) 104 in fact suggest deviations of U CL from the logarithmic trend found in DNS, however, this effect requires further conﬁrmation, as data are quite scattered. The core velocity proﬁle is found to be, to a good approximation, parabolic, with curvature which is nearly constant in wall units, and decreasing in outer units. Regarding the velocity ﬂuctuations, we ﬁnd evidence for continuing logarithmic increase of the inner-peak magnitude with Reτ. Some experiments and theoretical arguments would indicate that beyond Reτ ≈ 104 a change of behaviour might occur which, however, is very difﬁcult to quantify. The DNS is probably of little use in this respect, as in order to clearly discern among the various trends, Reτ in excess of 105 are likely to be needed. As predicted by the attached-eddy hypothesis, the wall-parallel velocity variances in the outer layer tend to form logarithmic layers, which are especially evident in the azimuthal velocity. Although we do not ﬁnd direct evidence for the existence of an outer peak of the axial velocity variance, our results highlight the occurrence of an outer site with substantial turbulence production excess over dissipation, thus contradicting the classical equilibrium hypothesis and likely to yield a distinct peak at Reτ ≈ 104. Investigating these and other violations of universality of wall turbulence to extrapolate asymptotic behaviours is a formidable challenge for theoreticians in years to come.

Supplementary movies. Supplementary movies are available at https://doi.org/10.1017/jfm.2021.727.

Acknowledgements. We acknowledge that the results reported in this paper have been achieved using the PRACE Research Infrastructure resource MARCONI based at CINECA, Casalecchio di Reno, Italy, under project PRACE no. 2019204979. Discussions with A.J. Smits are gratefully acknowledged. We would like to thank P. Luchini and M. Quadrio for providing the code used for the data uncertainty analysis.

926 A28-17

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

Funding. This research received no speciﬁc grant from any funding agency, commercial or not-for-proﬁt sectors.

Declaration of interests. The authors report no conﬂict of interest.

Data availability statement. The data that support the ﬁndings of this study are openly available at the web page http://newton.dma.uniroma1.it/database/

Author ORCIDs.

Sergio Pirozzoli https://orcid.org/0000-0002-7160-3023; Roberto Verzicco https://orcid.org/0000-0002-2690-9998; Paolo Orlandi https://orcid.org/0000-0002-0305-5723.

REFERENCES

AFZAL, N. 1982 Fully developed turbulent ﬂow in a pipe: an intermediate layer. Ing. Arch. 52 (6), 355–377. AFZAL, N. & YAJNIK, K. 1973 Analysis of turbulent pipe and channel ﬂows at moderately large Reynolds

number. J. Fluid Mech. 61, 23–31.

AHN, J., LEE, J.H., JANG, S. & SUNG, H.J. 2013 Direct numerical simulations of fully developed turbulent

pipe ﬂows for Reτ = 180,544 and 934. Intl J. Heat Fluid Flow 44, 222–228.

AHN, J., LEE, J.H., LEE, J., KANG, J.-H. & SUNG, H.J. 2015 Direct numerical simulation of a 30R long

turbulent pipe ﬂow at Reτ = 3000. Phys. Fluids 27, 065110.

AKSELVOLL, K. & MOIN, P. 1996 An efﬁcient method for temporal integration of the Navier–Stokes equations

in conﬁned axisymmetric geometries. J. Comput. Phys. 125, 454–463.

BARENBLATT, G.I., CHORIN, A.J. & PROSTOKISHIN, V.M. 1997 Scaling laws for fully developed turbulent

ﬂow in pipes. Appl. Mech. Rev. 50, 413–429.

BERNARDINI, M., PIROZZOLI, S. & ORLANDI, P. 2014 Velocity statistics in turbulent channel ﬂow up to

Reτ = 4000. J. Fluid Mech. 742, 171–191.

CANTWELL, B.J. 2019 A universal velocity proﬁle for smooth wall pipe ﬂow. J. Fluid Mech. 878, 834–874. CHEN, X. & SREENIVASAN, K.R. 2021 Reynolds number scaling of the peak turbulence intensity in wall

ﬂows. J. Fluid Mech. 908, R3.

CHIN, C., OOI, A.S.H., MARUSIC, I. & BLACKBURN, H.M. 2010 The inﬂuence of pipe length on turbulence

statistics computed from direct numerical simulation data. Phys. Fluids 22 (11), 115107.

CHIN, C., PHILIP, J., KLEWICKI, J., OOI, A. & MARUSIC, I. 2014 Reynolds-number-dependent turbulent

inertia and onset of log region in pipe ﬂows. J. Fluid Mech. 757, 747–769.

DURST, F., JOVANOVI ´C, J. & SENDER, J. 1995 LDA measurements in the near-wall region of a turbulent pipe

ﬂow. J. Fluid Mech. 295, 305–335.

EGGELS, J.G.M., UNGER, F., WEISS, M.H., WESTERWEEL, J., ADRIAN, R.J., FRIEDRICH, R. & NIEUWSTADT, F.T.M. 1994 Fully developed turbulent pipe ﬂow: a comparison between direct numerical simulation and experiment. J. Fluid Mech. 268, 175–210.

EL KHOURY, G.K., SCHLATTER, P., NOORANI, A., FISCHER, P.F., BRETHOUWER, G. & JOHANSSON, A.V. 2013 Direct numerical simulation of turbulent pipe ﬂow at moderately high Reynolds numbers. Flow Turbul. Combust. 91, 475–495.

FIORINI, T. 2017 Turbulent pipe ﬂow - high resolution measurements in CICLoPE. PhD thesis, School of

Engineering and Architecture, University of Bologna.

FURUICHI, N., TERAO, Y., WADA, Y. & TSUJI, Y. 2015 Friction factor and mean velocity proﬁle for pipe

ﬂow at high Reynolds numbers. Phys. Fluids 27, 095108.

FURUICHI, N., TERAO, Y., WADA, Y. & TSUJI, Y. 2018 Further experiments for mean velocity proﬁle of

pipe ﬂow at high Reynolds number. Phys. Fluids 29, 055101.

HARLOW, F.H. & WELCH, J.E. 1965 Numerical calculation of time-dependent viscous incompressible ﬂow

of ﬂuid with free surface. Phys. Fluids 8, 2182–2189.

HELLSTRÖM, L.H.O. & SMITS, A.J. 2014 The energetic motions in turbulent pipe ﬂow. Phys. Fluids 26,

125102.

HOYAS, S. & JIMÉNEZ, J. 2006 Scaling of velocity ﬂuctuations in turbulent channels up to Reτ = 2003. Phys.

Fluids 18, 011702.

HULTMARK, M., BAILEY, S.C.C. & SMITS, A.J. 2010 Scaling of near-wall turbulence in pipe ﬂow. J. Fluid

Mech. 649, 103–113.

HULTMARK, M., VALLIKIVI, M., BAILEY, S.C.C. & SMITS, A.J. 2012 Turbulent pipe ﬂow at extreme

Reynolds numbers. Phys. Rev. Lett. 108, 094501.

926 A28-18

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Turbulence in pipe ﬂow

HULTMARK, M., VALLIKIVI, M., BAILEY, S.C.C. & SMITS, A.J. 2013 Logarithmic scaling of turbulence

in smooth-and rough-wall pipe ﬂow. J. Fluid Mech. 728, 376–395.

JIMÉNEZ, J. 2018 Coherent structures in wall-bounded turbulence. J. Fluid Mech. 842, P1. JIMÉNEZ, J. & MOSER, R.D. 2007 What are we learning from simulating wall turbulence? Phil. Trans. R.

Soc. Lond. A 365, 715–732.

KIM, J. & MOIN, P. 1985 Application of a fractional-step method to incompressible Navier–Stokes equations.

J. Comput. Phys. 59, 308–323.

LEE, M. & MOSER, R.D. 2015 Direct simulation of turbulent channel ﬂow layer up to Reτ = 5200. J. Fluid

Mech. 774, 395–415.

LONG, R.R. & CHEN, T.-C. 1981 Experimental evidence for the existence of the ‘mesolayer’ in turbulent

systems. J. Fluid Mech. 105, 19–59.

LUCHINI, P. 2017 Universality of the turbulent velocity proﬁle. Phys. Rev. Lett. 118 (22), 224501. MARUSIC, I., BAARS, W.J. & HUTCHINS, N. 2017 Scaling of the streamwise turbulence intensity in the

context of inner-outer interactions in wall turbulence. Phys. Rev. Fluids 2, 100502.

MARUSIC, I. & MONTY, J.P. 2019 Attached eddy model of wall turbulence. Annu. Rev. Fluid Mech. 51,

49–74.

MARUSIC, I., MONTY, J.P., HULTMARK, M. & SMITS, A.J. 2013 On the logarithmic region in wall

turbulence. J. Fluid Mech. 716, R3.

MCKEON, B.J., ZAGAROLA, M.V. & SMITS, A.J. 2005 A new friction factor relationship for fully developed

pipe ﬂow. J. Fluid Mech. 538, 429–443.

MOIN, P. & VERZICCO, R. 2016 On the suitability of second-order accurate discretizations for turbulent ﬂow

simulations. Eur. J. Mech. B/Fluids 55, 242–245.

MONKEWITZ, P.A. 2021 The late start of the mean velocity overlap log law at y+ = O(103) – a generic feature

of turbulent wall layers in ducts. J. Fluid Mech. 910, A45.

NAGIB, H.M. & CHAUHAN, K.A. 2009 Criteria for assessing experiments in zero pressure gradient boundary

layers. Fluid Dyn. Res. 41, 021404.

NAGIB, H.M., MONKEWITZ, P.A., MASCOTELLI, L., FIORINI, T., BELLANI, G., ZHENG, X. & TALAMELLI, A. 2017 Centerline Kármán ‘constant’ revisited and contrasted to log-layer Kármán constant at CICLoPE. In 10th International Symposium on Turbulence and Shear Flow Phenomena.

NIKURADSE, J. 1933 Stromungsgesetze in rauhen Rohren. VDI-Forschungsheft 361, 1. ORLANDI, P. & FATICA, M. 1997 Direct simulations of turbulent ﬂow in a pipe rotating about its axis. J. Fluid

Mech. 343, 43–72.

ÖRLÜ, R., FIORINI, T., SEGALINI, A., BELLANI, G., TALAMELLI, A. & ALFREDSSON, P.H. 2017 Reynolds stress scaling in pipe ﬂow turbulence – ﬁrst results from CICLoPe. Phil. Trans. R. Soc. Lond. A 375 (2089), 20160187.

PIROZZOLI, S. 2014 Revisiting the mixing-length hypothesis in the outer part of turbulent wall layers: mean

ﬂow and wall friction. J. Fluid Mech. 745, 378–397.

PIROZZOLI, S., BERNARDINI, M. & ORLANDI, P. 2016 Passive scalars in turbulent channel ﬂow at high

Reynolds number. J. Fluid Mech. 788, 614–639.

PIROZZOLI, S. & ORLANDI, P. 2021 Natural grid stretching for DNS of wall-bounded ﬂows. J. Comput. Phys.

439, 110408.

POPE, S.B. 2000 Turbulent Flows. Cambridge University Press. PULLIN, D.I., INOUE, M. & SAITO, N. 2013 On the asymptotic state of high Reynolds number, smooth-wall

turbulent ﬂows. Phys. Fluids 25, 015116.

REYNOLDS, O. 1883 An experimental investigation of the circumstances which determine whether the motion of water shall be direct or sinuous, and of the law of resistance in parallel channels. Phil. Trans. R. Soc. Lond. 174, 935–982.

RUETSCH, G. & FATICA, M. 2014 CUDA Fortran for Scientists and Engineers. Elsevier. RUSSO, S. & LUCHINI, P. 2017 A fast algorithm for the estimation of statistical error in DNS (or experimental)

time averages. J. Comput. Phys. 347, 328–340.

SCHULTZ, M.P. & FLACK, K.A. 2013 Reynolds-number scaling of turbulent channel ﬂow. Phys. Fluids 25,

025104.

STEVENS, R.J.A.M., VAN DER POEL, E.P., GROSSMANN, S. & LOHSE, D. 2013 The unifying theory of

scaling in thermal convection: the updated prefactors. J. Fluid Mech. 730, 295–308.

SWANSON, C.J., JULIAN, B., IHAS, G.G. & DONNELLY, R.J. 2002 Pipe ﬂow measurements over a wide

range of Reynolds numbers using liquid helium and various gases. J. Fluid Mech. 461, 51–60. TOWNSEND, A.A. 1976 The Structure of Turbulent Shear Flow, 2nd edn. Cambridge University Press. VERZICCO, R. & ORLANDI, P. 1996 A ﬁnite-difference scheme for three-dimensional incompressible ﬂows

in cylindrical coordinates. J. Comput. Phys. 123, 402–414.

926 A28-19

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 7 2 7 1 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli and others

WEI, T., FIFE, P., KLEWICKI, J. & MCMURTRY, P. 2005 Properties of the mean momentum balance in

turbulent boundary layer, pipe and channel ﬂow. J. Fluid Mech. 573, 303–327.

WILLERT, C.E., SORIA, J., STANISLAS, M., KLINNER, J., AMILI, O., EISFELDER, M., CUVIER, C., BELLANI, G., FIORINI, T. & TALAMELLI, A. 2017 Near-wall statistics of a turbulent pipe ﬂow at shear Reynolds numbers up to 40000. J. Fluid Mech. 826, R5.

WU, X. & MOIN, P. 2008 A direct numerical simulation study on the mean velocity characteristics in turbulent

pipe ﬂow. J. Fluid Mech. 608, 81–112.

ZAGAROLA, M.V. & SMITS, A.J. 1998 Mean-ﬂow scaling of turbulent pipe ﬂow. J. Fluid Mech. 373, 33–79.

926 A28-20