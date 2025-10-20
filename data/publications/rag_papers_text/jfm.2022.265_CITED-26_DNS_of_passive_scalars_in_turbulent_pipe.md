s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

J. Fluid Mech. (2022), vol. 940, A45, doi:10.1017/jfm.2022.265

DNS of passive scalars in turbulent pipe ﬂow

Sergio Pirozzoli1,†, Joshua Romero2, Massimiliano Fatica2, Roberto Verzicco3,4 and Paolo Orlandi1 1Dipartimento di Ingegneria Meccanica e Aerospaziale, Sapienza Università di Roma, Via Eudossiana 18, 00184 Roma, Italy 2NVIDIA Corporation, 2701 San Tomas Expressway, Santa Clara, CA 95050, USA 3Dipartimento di Ingegneria Industriale, Università di Roma TorVergata, Via del Politecnico 1, 00133 Roma, Italy 4Physics of Fluid Group, University of Twente, P.O. Box 217, 7500 AE Enschede, The Netherlands

(Received 6 October 2021; revised 31 January 2022; accepted 21 March 2022)

We study the statistics of passive scalars at Pr = 1, for turbulent ﬂow within a smooth straight pipe of circular cross section up to Reτ ≈ 6000 using direct numerical simulation (DNS) of the Navier–Stokes equations. While featuring a general organisation similar to the axial velocity ﬁeld, passive scalar ﬁelds show additional energy at small wavenumbers, resulting in a higher degree of mixing and in a k−4/3 spectral inertial range. The DNS results highlight logarithmic growth of the inner-scaled bulk and mean centreline scalar values with the friction Reynolds number, implying an estimated scalar von Kármán constant kθ ≈ 0.459, which also nicely ﬁts the mean scalar proﬁles. The DNS data are used to synthesise a modiﬁed form of the classical predictive formula of Kader & Yaglom (Intl J. Heat Mass Transfer, vol. 15 (12), 1972, pp. 2329–2351), which points to some shortcomings of the original formulation. Universality of the mean core scalar proﬁle in defect form is recovered, with very nearly parabolic shape. Logarithmic growth of the buffer-layer peak of the scalar variance is found in the Reynolds number range under scrutiny, which well conforms with Townsend’s attached-eddy hypothesis, whose validity is also supported by the spectral maps. The behaviour of the turbulent Prandtl number shows good universality in the outer wall layer, with values Prt ≈ 0.84, as also found in previous studies, but closer to unity near the wall, where existing correlations do not reproduce the observed trends.

Key words: pipe ﬂow, pipe ﬂow boundary layer, turbulence simulation

†Email address for correspondence: sergio.pirozzoli@uniroma1.it

© The Author(s), 2022. Published by Cambridge University Press. This is an Open Access article, distributed under the terms of the Creative Commons Attribution licence (https://creativecommons. org/licenses/by/4.0/), which permits unrestricted re-use, distribution, and reproduction in any medium, provided the original work is properly cited.

940 A45-1

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

1. Introduction The study of passive scalars evolving within wall-bounded turbulent ﬂows has great practical importance, being relevant for the behaviour of diluted contaminants and/or as a model for the temperature ﬁeld under the assumption of low Mach number and small temperature differences (Monin & Yaglom 1971; Cebeci & Bradshaw 1984). It is well known that measurements of concentration of passive tracers and of small temperature differences are quite difﬁcult and, in fact, available information about even basic passive scalar statistics are rather limited (Gowen & Smith 1967; Kader 1981; Subramanian & Antonia 1981; Nagano & Tagawa 1988), mostly including basic mean properties and overall mass or heat transfer coefﬁcients. Although existing semi-empirical correlations have sufﬁcient accuracy for engineering design (Kays, Crawford & Weigand 1980), their theoretical foundations are not ﬁrmly established. Furthermore, assumptions typically made in turbulence models such as constant turbulent Prandtl number are known to be crude approximations in the absence of reliable reference data.

Given this scenario, direct numerical simulation (DNS) is the natural candidate to establish a credible database for the physical analysis of passive scalars in wall turbulence, and for the development and validation of phenomenological prediction formulae and turbulence models. Most DNS studies of passive scalars in wall turbulence have been so far carried out for the prototype case of planar channel ﬂow, starting with the work of Kim & Moin (1989), at Reτ = 180 (here Reτ = uτR/ν is the friction Reynolds number, with uτ = (τw/ρ)1/2 the friction velocity, R the pipe radius, ν the ﬂuid kinematic viscosity, ρ the ﬂuid density and τw the wall shear stress), in which the forcing of the scalar ﬁeld was achieved using a spatially and temporally uniform source term. Additional simulations at increasingly high Reynolds number were carried out by Kawamura, Abe & Matsuo (1999) and Abe, Kawamura & Matsuo (2004), based on enforcement of strictly constant heat ﬂux in time (this approach is hereafter referred to as CHF), which ﬁrst allowed scale separation effects to be appreciated and a reasonable value of the scalar von Kármán constant kθ ≈ 0.43 to be deduced, as well as effects of Prandtl number variation (the molecular Prandtl number is here deﬁned as the ratio of the kinematic viscosity to the scalar diffusivity, Pr = ν/α). Those studies showed close similarity between the streamwise velocity and passive scalar ﬁeld in the near-wall region, as after the classical Reynolds analogy. Speciﬁcally, the scalar ﬁeld was found to be organised into streaks whose size scales in wall units, with a correlation coefﬁcient between streamwise velocity ﬂuctuations and scalar ﬂuctuations close to unit. Computationally high Reynolds numbers (Reτ ≈ 4000, with Pr ≤ 1) were reached in the study of Pirozzoli, Bernardini & Orlandi (2016), using spatially uniform forcing in such a way as to maintain the bulk temperature constant in time (this approach is hereafter referred to as CMT). Recent large-scale channel ﬂow DNS with passive scalars using the CHF forcing at Pr = 0.71 (as representative of air) have been carried out by Alcántara-Ávila, Hoyas & Pérez-Quiles (2021).

Flow in a circular pipe is clearly more practically relevant than planar channel ﬂow in view of applications such as heat exchangers, and it has been the subject of a number of experimental studies, mainly aimed at predicting the heat transfer coefﬁcient as a function of the bulk ﬂow Reynolds number (Kays et al. 1980). High-ﬁdelity numerical simulations including passive scalars in pipe ﬂow have been quite scarce so far and mainly include studies at Reτ ≤ 1000 (Piller 2005; Redjem-Saad, Ould-Rouiss & Lauriat 2007; Saha et al. 2011; Antoranz et al. 2015; Straub et al. 2019). The current knowledge about gross properties and mean scalar proﬁles across the Reynolds and Prandtl numbers envelope thus currently rests on semi-empirical correlations (Kays et al. 1980; Kader 1981), which, although suitable for practical applications, deserve careful scrutiny. Clearly, the state of the art is not as well developed as for planar channel ﬂow. 940 A45-2

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

z

ub

r φ

R

Lz

Figure 1. Deﬁnition of the coordinate system for DNS of pipe ﬂow, where z, r and φ are the axial, radial and azimuthal directions, respectively, R is the pipe radius, Lz the pipe length and ub is the bulk velocity.

In this paper, we thus present DNS data of turbulent ﬂow in a smooth circular pipe up to Reτ ≈ 6000, including a passive scalar ﬁeld with Pr = 1, at which some asymptotic high-Reynolds-number effects appear which were not observed in previous studies. Relying on the DNS database, we carry out an analysis of the structure of passive scalars in turbulent pipe ﬂow, revisit current theoretical inferences and discuss implications about possible trends in the extreme-Reynolds-number regime. From a more engineering standpoint, we also revisit formulae for heat transfer prediction, as well as assumptions made in Reynolds-averaged Navier–Stokes (RANS) models for passive scalar turbulence. Although, as previously pointed out, the study of passive scalars is relevant in several contexts, the main ﬁeld of application is heat transfer and, therefore, from now on we refer to the passive scalar ﬁeld as the temperature ﬁeld (denoted as T), and scalar ﬂuxes will be interpreted as heat ﬂuxes. Details on the velocity statistics from the present DNS database were reported in a separate publication (Pirozzoli et al. 2021).

2. Numerical dataset Numerical simulations of fully developed turbulent ﬂow in a circular pipe are carried out assuming periodic boundary conditions in the axial (z) and azimuthal (φ) directions, as shown in ﬁgure 1. The velocity ﬁeld is controlled by two parameters, namely the bulk Reynolds number (Reb = 2Rub/ν, with ub the bulk velocity namely averaged over the cross section), and the relative pipe length, Lz/R. The incompressible Navier–Stokes equations are supplemented with the transport equation for a passive scalar ﬁeld (hence, buoyancy effects are disregarded), with the same diffusivity as the velocity ﬁeld (hence, we assume Pr = 1) and with isothermal boundary conditions at the pipe wall (r = R). The passive scalar equation is forced through a time-varying, spatially uniform source term (CMT approach), in the interest of achieving complete similarity with the streamwise momentum equation, with the obvious exclusion of pressure. Although the total heat ﬂux resulting from the CMT approach is not strictly constant in time, it oscillates around its mean value under statistically steady conditions. Differences of the results obtained with the CMT and CHF approaches have been described by Abe & Antonia (2017) and Alcántara-Ávila et al. (2021), which although generally small deserve some attention.

The computer code used for the DNS is the spin-off of an existing solver previously used to study Rayleigh–Bénard convection in cylindrical containers at extreme Rayleigh numbers (Stevens et al. 2013). That code is, in turn, the evolution of the solver originally developed by Verzicco & Orlandi (1996), and used for DNS of pipe ﬂow by Orlandi & Fatica (1997). A second-order ﬁnite-difference discretisation of the incompressible

940 A45-3

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

Navier–Stokes equations in cylindrical coordinates is used, based on the classical marker-and-cell method (Harlow & Welch 1965), whereby pressure and passive scalars are located at the cell centres, whereas the velocity components are located at the cell faces, thus removing odd–even decoupling phenomena and guaranteeing discrete conservation of the total kinetic energy and passive scalar variance in the inviscid limit. The Poisson equation resulting from enforcement of the divergence-free condition is efﬁciently solved by double trigonometric expansion in the periodic axial and azimuthal directions, and inversion of tridiagonal matrices in the radial direction (Kim & Moin 1985). An extensive series of previous studies about wall-bounded ﬂows from this group proved that second-order ﬁnite-difference discretisation yields in practical cases of wall-bounded turbulence results which are by no means inferior in quality to those of pseudo-spectral methods (e.g. Moin & Verzicco 2016; Pirozzoli et al. 2016). A crucial issue is the proper treatment of the polar singularity at the pipe axis. A detailed description of the subject is reported in Verzicco & Orlandi (1996), but, basically, the radial velocity ur in the governing equations is replaced by qr = rur (r is the radial space coordinate), which by construction vanishes at the axis. The governing equations are advanced in time by means of a hybrid third-order low-storage Runge–Kutta algorithm, whereby the diffusive terms are handled implicitly, and convective terms in the axial and radial direction explicitly. An important issue in this respect is the convective time step limitation in the azimuthal direction, due to intrinsic shrinking of the cells size toward the pipe axis. To alleviate this limitation, we use implicit treatment of the convective terms in the azimuthal direction (Akselvoll & Moin 1996; Wu & Moin 2008), which enables marching in time with similar time step as in planar domains ﬂow in practical computations. In order to minimise numerical errors associated with implicit time stepping, explicit and implicit discretisations of the azimuthal convective terms are linearly blended with the radial coordinate, in such a way that near the pipe wall the treatment is fully explicit, and near the pipe axis it is fully implicit. The code was adapted to run on clusters of graphic accelerators (GPUs), using a combination of CUDA Fortran and OpenACC directives, and relying on the CUFFT libraries for efﬁcient execution of fast Fourier transforms (FFTs) (Ruetsch & Fatica 2014).

From now on, inner normalisation of the ﬂow properties will be denoted with the ‘+’ superscript, whereby velocities are scaled by uτ, wall distances by ν/uτ and temperatures with respect to the friction temperature,

(cid:2)

(cid:3)

α

dT dy

.

Tτ =

uτ In particular, the inner-scaled temperature is deﬁned as θ+ = (T − Tw)/Tτ, where T is the local temperature and Tw is the wall temperature. Capital letters are used to denote ﬂow properties averaged in the homogeneous spatial directions and in time, brackets to denote the averaging operator and lowercase letters to denote ﬂuctuations from the mean. Finally, bulk values of axial velocity and temperature are deﬁned as

w

ub = 2

(cid:4)

R

r(cid:4)uz(cid:5)dr

(cid:5)

R2,

Tb = 2

(cid:4)

R

r(cid:4)T(cid:5)dr

(cid:5)

R2.

0

0

A list of the main simulations that we have carried out is given in table 1. The mesh resolution is designed based on the criteria discussed by Pirozzoli & Orlandi (2021). In particular, the collocation points are distributed in the wall-normal direction so that approximately 30 points are placed within y+ ≤ 40 (y = R − r is the wall distance), with the ﬁrst grid point at y+ < 0.1, and the mesh is progressively stretched in the

940 A45-4

(2.1)

(2.2a,b)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

Dataset

Lz/R Mesh (Nz × Nr × Nφ)

Reb

Nu

Reτ

Δtstat/τt

Line colour

DNS-A DNS-B DNS-C DNS-C-SH DNS-C-LO DNS-C-FF DNS-C-FR DNS-C-FZ DNS-D DNS-E DNS-F

15 15 15 7.5 30 15 15 15 15 15 15

256 × 67 × 256 768 × 140 × 768 1792 × 270 × 1792 1792 × 270 × 986 1792 × 270 × 3944 3944 × 270 × 1792 1792 × 540 × 1792 1792 × 270 × 3944 3072 × 399 × 3072 4608 × 540 × 4608 9216 × 910 × 9216

5300 17 000 44 000 44 000 44 000 44 000 44 000 44 000 82 500 133 000 285 000

24.8251 60.2341 124.178 124.098 123.958 123.569 124.625 122.196 202.662 296.485 539.975

180.3 495.3 1136.6 1144.2 1134.6 1131.0 1135.7 1135.7 1976.0 3028.1 6019.4

204.0 87.4 25.9 31.1 24.5 31.3 28.6 15.5 22.4 16.6 8.32

NA NA NA NA NA

Table 1. Flow parameters for DNS of pipe ﬂow. Cases are labelled in increasing order of Reynolds number, from A to F. Sufﬁxes SH and LO indicate DNS in short and long domains, respectively; FF, FR and FZ denote reﬁnement along the φ, r and z directions, respectively.

outer wall layer in such a way that the mesh spacing is proportional to the local Kolmogorov length scale, which there varies as η+ ≈ 0.8y+1/4 (Jiménez 2018). Regarding the axial and azimuthal directions, ﬁnite-difference simulations of wall-bounded ﬂows yield grid-independent results as long as Δx+ ≈ 10, R+Δφ ≈ 4.5 (Pirozzoli et al. 2016), hence we have selected the number of grid points along the homogeneous ﬂow directions as Nz = Lz/R × Reτ/9.8, Nφ ∼ 2π × Reτ/4.1. According to the established practice (Hoyas & Jiménez 2006; Ahn et al. 2015; Lee & Moser 2015), the time intervals used to collect the ﬂow statistics (Δtstat) are reported as a fraction of the eddy-turnover time (R/uτ).

The sampling errors for some key properties discussed in this paper have been estimated using the method of Russo & Luchini (2017), based on extension of the classical batch means approach. The results of the uncertainty estimation analysis are listed in table 2, where we provide expected values and associated standard deviations for the Nusselt number (Nu), mean temperature at the pipe centreline (Θ+ CL) and peak temperature variance and its wall distance ((cid:4)θ2(cid:5)+ + IP, respectively). We ﬁnd that the sampling error is generally quite limited, being larger in the largest DNS, which have been run for shorter time. In particular, in DNS-F, the expected sampling error in Nusselt number, centreline temperature and peak temperature variance is approximately 0.5%. Additional tests aimed at establishing the effect of axial domain length and grid size have been carried out for the DNS-C ﬂow case, whose results are also reported in table 2. We ﬁnd that even halving the pipe length yields minimal change in the basic ﬂow properties, which is well within the uncertainty bounds. This is in contrast to properties related to the velocity ﬁeld, which are signiﬁcantly affected from use of a short domain (Pirozzoli et al. 2021). The interesting consequence of this observation is the possibility to carry out DNS of scalar ﬁelds in more limited domains, as also noted by Alcántara-Ávila et al. (2021). In order to quantify uncertainties associated with numerical discretisation, additional simulations have been carried out by doubling the number of grid points in the azimuthal, radial and axial directions, respectively. Based on the data reported in the table, after discarding the short-pipe case, we can thus quantify the uncertainty due to numerical discretisation and limited pipe length to be approximately 0.2% for the Nusselt number, 0.4% for the pipe centreline temperature and 0.7% for the peak temperature variance.

IP and y

940 A45-5

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

Dataset

Nu

Θ+ CL

(cid:4)θ2(cid:5)+ IP

+ y IP

DNS-A DNS-B DNS-C DNS-C-SH DNS-C-LO DNS-C-FF DNS-C-FR DNS-C-FZ DNS-D DNS-E DNS-F

18.31 ± 0.054% 7.667 ± 0.24% 15.40 ± 0.24% 24.8251 ± 0.16% 14.69 ± 0.29% 60.2341 ± 0.072% 19.86 ± 0.099% 7.988 ± 0.11% 124.178 ± 0.11% 21.83 ± 0.083% 8.668 ± 0.18% 14.93 ± 0.064% 124.098 ± 0.11% 22.21 ± 0.091% 8.760 ± 0.28% 14.89 ± 0.082% 123.958 ± 0.12% 21.84 ± 0.093% 8.636 ± 0.26% 14.88 ± 0.048% 8.591 ± 0.18% 14.88 ± 0.053% 123.569 ± 0.12% 124.625 ± 0.18% 21.79 ± 0.079% 8.537 ± 0.22% 14.62 ± 0.074% 22.25 ± 0.10% 122.196 ± 0.16% 15.40 ± 0.10% 9.011 ± 0.25% 23.12 ± 0.19% 9.034 ± 0.32% 15.00 ± 0.068% 202.662 ± 0.19% 23.96 ± 0.16% 9.326 ± 0.42% 15.05 ± 0.13% 296.485 ± 0.26% 15.30 ± 0.17% 25.37 ± 0.23% 9.794 ± 0.60% 539.975 ± 0.32%

21.89 ± 0.12%

Table 2. Uncertainty estimation study: mean values of representative quantities and standard deviation of their estimates, where Nu is the Nusselt number, Θ+ (cid:5)+ IP is the peak temperature variance and y

CL is the mean pipe centreline temperature, (cid:4)θ2 z

+ IP is its distance from the wall.

3. Results

3.1. General organisation of the temperature ﬁeld Qualitative information about the structure of the ﬂow ﬁeld is provided by instantaneous perspective views of the axial velocity and temperature ﬁelds, which we show in ﬁgure 2. Although ﬁner-scale details are visible at the higher Reb, the ﬂow in the cross-stream planes is always characterised by a limited number of bulges distributed along the azimuthal direction, which correspond to alternating intrusions of high-speed ﬂuid from the pipe core and ejections of low-speed ﬂuid from the wall. Streaks are visible in the near-wall cylindrical shells, whose organisation has clear association with the cross-stream pattern. Speciﬁcally, R-sized low-speed streaks are observed in association with large-scale ejections, whereas R-sized high-speed streaks occur in the presence of large-scale inrush from the core ﬂow. At the same time, smaller streaks scaling in wall units appear, corresponding to buffer-layer ejections/sweeps. Hence, organisation of the ﬂow on at least two length scales is apparent here, whose separation increases with Reτ. As ﬁgure 2 shows, the temperature ﬁeld has the same qualitative organisation as axial velocity, and low-speed streaks correspond to low-temperature thermal streaks. This is not surprising, given the formal similarity of the controlling equations at Pr = 1, and close association of the two quantities pointed out in many previous studies (e.g. Abe & Antonia 2009; Pirozzoli et al. 2016; Alcántara-Ávila, Hoyas & Pérez-Quiles 2018). It is interesting that this association includes both the large ﬂow scales in the pipe core and the small, near-wall streaks. Zooming in closer (see ﬁgure 3), one can nevertheless detect some differences between the two ﬁelds, in that temperature tends to form sharper fronts, whereas the axial velocity ﬁeld tends to be more blurred. As noted by Pirozzoli et al. (2016), this is due to the fact that the axial velocity is not passively advected, but rather it can react to the formation of fronts through feedback pressure. As a result, whereas the organisation at large scales is similar, smaller features are found in the temperature ﬁelds, as clearly highlighted in the corresponding spectral densities.

The spectral maps of uz and θ are depicted in ﬁgure 4, for the DNS-F ﬂow case. In order to isolate changes in the typical length scales, in the ﬁgure we show the azimuthal spectral densities normalised by the respective variances, deﬁned as

ˆEx(kφ) = Ex(kφ)/(cid:4)x2(cid:5),

940 A45-6

(3.1)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

uz/(cid:2)u(cid:3)(cid:2)(cid:3), T/(cid:2)T(cid:3)(cid:2)(cid:3)

0

0.10

0.15

0.20

0.30

0.40

0.50

0.60

0.70

0.80

0.85

0.90

1.00

(a)

(b)

(c)

(d)

Figure 2. (a),(c) Instantaneous axial velocity and (b),(d) temperature contours in turbulent pipe ﬂow as obtained from (a),(b) DNS-A and (c),(d) DNS-F. Thirty contours (from zero to the mean centreline value) are shown on a cross-stream plane and on a near-wall cylindrical shell (y+ ≈ 15), in colour scale from blue to red.

where kφ = 2π/λφ is the relevant wavenumber for the φ direction and x is the generic ﬂow property. The axial velocity spectra clearly bring out a two-scale organisation of the ﬂow ﬁeld, with a near-wall peak associated with the wall regeneration cycle (Jiménez & Pinelli 1999), and an outer peak associated with outer-layer large-scale motions (Hutchins & Marusic 2007). The latter peak is found to be centred around y/R ≈ 0.3, and to correspond to eddies with typical wavelength λφ ≈ 1.5R, consistent with that found by Ahn et al. (2015) for pipe ﬂow at Reτ = 3000. Secondary peaks corresponding to harmonics of this fundamental wavelength are also observed here, suggesting that the typical outer modes are not purely sinusoidal with respect to the azimuthal direction. Notably, very similar organisation is found in the temperature ﬁeld, the main difference being a somewhat broader peak at large wavelengths. Both the axial velocity and the temperature ﬁeld exhibit a prominent spectral ridge corresponding to modes with typical azimuthal length scale λφ ∼ y, extending over about two decades, which can be interpreted as the footprint of a hierarchy of wall-attached eddies following Tonwsend’s hypothesis (Townsend 1976).

940 A45-7

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

uz/(cid:2)u(cid:3)(cid:2)(cid:3), T/(cid:2)T(cid:3)(cid:2)(cid:3)

0

0.10 0.15 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.85 0.90 1.00

(a)

(b)

Figure 3. (a) Instantaneous axial velocity and (b) temperature contours in a subregion of the pipe cross section for DNS-F.

(a)

10–2

λφ/R 10–1

100

101

100

(b)

10–2

λφ/R 10–1

100

101

100

103

10–1

103

10–1

y+

102

10–2

102

10–2

101

10–3

101

10–3

100

101

102

103 + λφ

104

105

100

101

102

103 + λφ

104

105

Figure 4. Variation of pre-multiplied, normalised azimuthal spectral densities of uz (ˆEuz, (a)) and θ (ˆEθ, (b)) with wall distance, for ﬂow case DNS-F. Wall distances and wavelengths are reported both in inner units (bottom, left), and in outer units (top, right). The solid diagonal line marks the trend λφ = 7.16y. Contour levels from 0.05 to 0.5 are shown, in intervals of 0.05.

Hence, we may expect that inferences of the attached-eddy hypothesis regarding the behaviour of the axial velocity ﬁeld also carry on to the temperature ﬁeld.

Differences between velocity and scalar spectra are better scrutinised in ﬁgure 5, where we show spectral densities at a discrete set of wall distances. Figure 5(a) clearly brings out the bi-modal distribution of energy between the inner and the outer energetic sites. At intermediate wall distances (y+ ≈ 100) there is some mild evidence for a ˆEx ∼ λφ range which is also predicted from Townsend’s theory (Nickels et al. 2005). Most importantly, the ﬁgure shows extra energy at small wavelengths in the temperature spectra, with exception of the nearest wall location. This difference is emphasised in ﬁgure 5(b), which shows spectra at y/R = 0.3 (at which the Taylor microscale Reynolds number is

940 A45-8

y/R

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

(a)

0.8

(b)

104

0.7

102

0.6

100

θ Ê φ+ k

,

z

0.5

0.4

θ Ê

,

z

10–2

10–4

3 / φ5 k

x

)

(

u Ê φ+ k

0.3

0.2

u Ê

10–6

10–8

3 / φ4 k

0.1

10–10

x

)

(

0 101

102

103 + λφ

104

105

10–12

10–4

10–3

10–2 + kφ

10–1

100

Figure 5. (a) Pre-multiplied, normalised spectral densities of uz (solid) and θ (dashed), at y+ = 15 (gold), y+ = 50 (green), y+ = 100 (cyan) and y/R = 0.3 (purple), for the DNS-F ﬂow case. (b) Normalised spectral densities of uz (solid) and θ (dashed) at y/R = 0.3, compensated by k5/3 (top inset) and by k4/3 (bottom inset).

Reλ ≈ 400) in the classical log–log, non-pre-multiplied representation. Whereas the uz and θ spectra are very similar at the largest scales of motion, temperature tends to have a more shallow decay in the inertial and dissipative regions. This is well seen in the compensated representations shown in the insets. Whereas the classical k−5/3 behaviour can be traced in the uz spectra (at least in a tiny range of wavenumbers), the θ spectra seem to feature instead a k−4/3 range, which is the theoretically expected behaviour for passive scalars in sheared turbulence (Lohse 1994).

Differences between axial velocity and temperature ﬁelds are also apparent in the close proximity of the wall. In ﬁgure 6 we show the probability density functions (p.d.f.s) for the wall-normal derivatives of uz and θ. Both variables seem to tend to limit distributions in the inﬁnite-Re limit, however whereas θ is mathematically bound to be positive, hence its wall-normal derivative must also be positive, uz can have instantaneously negative values corresponding to local ﬂow reversal. As a result, we ﬁnd that the p.d.f. of the temperature gradient is well approximated by a log–normal distribution, as resulting from random multiplicative events. On the other hand, the p.d.f. of uz obviously deviates from log–normality near the origin, but also its positive tail seems to be less prominent than for θ. The existence of local ﬂow inversion at the wall, although with small probability (about 0.1% overall) was noted in several previous studies (e.g. Lenaers et al. 2012), and related to the presence of oblique vortices inducing negative pressure ﬂuctuations. This again corroborates the interpretation of different behaviour of uz and θ as being due to the action of pressure.

3.2. Mean temperature ﬁeld The mean temperature proﬁle in turbulent pipes has received extensive attention from theoretical and experimental studies, and the general consensus (Kader 1981) is that a logarithmic law well ﬁts the experimental data. Recent studies have instead questioned the validity of the logarithmic law for the mean velocity ﬁeld at ﬁnite Reynolds number (Jiménez & Moser 2007; Pirozzoli, Bernardini & Orlandi 2014; Lee & Moser 2015), and corrections to account for the effect of the core ﬂow on the overlap layer have been proposed (e.g. Luchini 2017; Cantwell 2019; Monkewitz 2021). Such corrections mainly amount to addition of a linear term to the logarithmic proﬁle which can be justiﬁed as a

940 A45-9

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

(a)

(b)

100

100

10–1

10–1

. f . d . p

10–2

10–2

10–3

10–3

10–4

10–4

–2

–1

0

1

2 +/dy+

duz

3

4

5

6

–2

–1

0

1

3 2 dθ+/dy+

4

Figure 6. Probability density function of wall-normal derivatives of (a) axial velocity and (b) temperature. The colour codes are as in table 1. The dashed grey lines denote a log–normal distribution made to ﬁt the DNS-F data.

(a)

(b)

8

25

6

4

Θ+

20

15

10

5

g o +l Θ – + Θ

2

0

+

y d

/ + Θ d +

y

6

4

2

2

0

0.2

0.4

y/R

0.6

100

101

100 102 y+

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

Figure 7. (a) Inner-scaled mean temperature proﬁles and (b) corresponding log-law diagnostic functions. Deviations from the assumed logarithmic wall law, Θ+ = logy+/0.459 + 5.78, are highlighted in the inset log of (a). Circles denote the functional approximation proposed by Kader (1981), here evaluated for Reτ = 6019, Pr = 1. In (b), the dashed horizontal line denotes the inverse of the Kármán constant, 1/kθ, and the dash-dotted lines in the inset denote the linear ﬁt (3.3), with kθ = 0.459, αθ = 1.81. See table 1 for colour codes.

higher-order term in the asymptotic matching between the inner and the outer layer (Afzal & Yajnik 1973), or as due to the presence of a mean pressure gradient in internal ﬂows (Luchini 2017). Deviations of the proﬁles of passive scalars from the assumed logarithmic distribution were also observed in DNS of channel ﬂow by Pirozzoli et al. (2016) and Alcántara-Ávila et al. (2021), amounting to a linear correction whose inner-scaled slope decreases with Reτ. In ﬁgure 7, we show a series of temperature proﬁles computed with the present DNS, ﬁtted with a logarithmic function with inverse slope kθ = 0.459, determined as described in the next section. The additive constant resulting from best ﬁtting of the DNS data is Cθ ≈ 5.78. As shown in the inset of ﬁgure 7(a), the velocity proﬁles for Reτ ≥ 103 follow this distribution with deviations smaller than 0.1 wall units from y+ ≈ 30 to y/R ≈ 0.1. Hence, the standard log law is a good approximation of the temperature proﬁle in the overlap layer for most practical purposes. The functional expression proposed by Kader (1981, (9), circles in panel (a)) is also found to provide

940 A45-10

5

0.8

6

1.0

104

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

reasonable approximation of the data throughout the wall layer, even if with somewhat unnatural behaviour in the buffer layer and slight overprediction in the outer wall layer.

Very similar considerations apply to the mean axial velocity proﬁles (Pirozzoli et al. 2021, ﬁgure 3), which are visually well ﬁtted with a logarithmic distribution, with estimated value of the von Kármán constant k ≈ 0.387 (Pirozzoli et al. 2021), hence much less than kθ, as consistently noted in previous studies on the subject. Based on the results presented in §3.1, this difference can be justiﬁed by recalling that in the log layer (if present), k/kθ ≈ νt/αt, where νt and αt are the turbulent kinematic and thermal diffusivities. As noted previously, the temperature ﬁeld has a tendency to form sharper fronts, with steeper gradients, hence its effective diffusivity is expected to be larger than for the axial momentum. Accordingly, one may expect k to be smaller than kθ, and the turbulent Prandtl number to be less than unity in the outer layer. More formal arguments to justify this difference, based on the properties of the similarity solution for the logarithmic mean proﬁle over the inertial (non-diffusive) domain, were offered by Zhou, Klewicki & Pirozzoli (2019).

More detailed scrutiny about the behaviour of the mean temperature proﬁle is carried

out in ﬁgure 7(b), where we show the logarithmic diagnostic function,

Ξθ = y

+

dΘ+/dy

+,

(3.2)

which is expected to be constant in the presence of a genuine logarithmic layer. As found previously for the axial velocity ﬁeld (Pirozzoli et al. 2021, ﬁgure 4), no region with ﬂat distribution of this indicator is, in fact, present. Rather, we note the occurrence of a nearly linear distribution from y+ ≈ 100 to y/R ≈ 0.4, whose slope is approximately constant in outer units, hence the diagnostic function can be expressed as

Ξθ ≈ 1 kθ with αθ ≈ 1.81. In other words, whereas a simple logarithmic proﬁle is a reasonable approximation for engineering estimates, a linear correction yields signiﬁcant improvement in the representation of the temperature proﬁle, over a wider range of wall distances. Based on (3.3), a genuine log layer in the mean temperature proﬁle would only emerge at inﬁnite Reynolds number.

y R

+ αθ

,

(3.3)

The structure of the core region of the ﬂow is inspected in ﬁgure 8, where the mean temperature proﬁles are shown in defect form. Disregarding the DNS at the lowest Reynolds number (DNS-A and DNS-B) the scatter across the various temperature proﬁles for y/R ≥ 0.2 is less than 1%, which suggests that outer-layer similarity is very nearly achieved. As suggested by Pirozzoli (2014) and Orlandi, Bernardini & Pirozzoli (2015), the core velocity and temperature proﬁles can be closely approximated with simple universal quadratic distributions, which one can derive under the assumption of constant eddy diffusivity of momentum and temperature. In particular, we ﬁnd that the formula

Θ+ CL

−Θ+ = CO(1 − y/R)2,

(3.4) with CO = 5.5, ﬁts the mean temperature distribution in the pipe core quite well. Closer to the wall, the corrected logarithmic proﬁle sets in at y/R (cid:2) 0.44, here expressed in outer coordinates,

Θ+ CL

−Θ+ = − 1 kθ

log(y/R) − αθ

y R

+ Bθ,

(3.5)

where data ﬁtting yields Bθ = 0.732. Although more elaborate descriptions of the outer velocity proﬁles are possible (e.g. Krug, Philip & Marusic 2017; Luchini 2018), the

940 A45-11

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

(a)

20

(b)

20

15

15

+ Θ –

10

10

L +C Θ

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

Figure 8. Mean defect temperature proﬁles in (a) linear and (b) semi-logarithmic scale. The dashed grey line marks a parabolic ﬁt of the DNS data (Θ+ − Θ+ = 5.5(1 − y/R)2) and the dot-dashed purple line in (b) CL the corrected outer-layer logarithmic ﬁt Θ+ − Θ+ = 0.732 − 1/0.459log(y/R) − 1.81(y/R). Only datasets CL DNS-C to DNS-F are shown here, see table 1 for colour codes.

composite proﬁle compounding (3.4) and (3.5) yields accurate representation of the whole outer-layer mean temperature proﬁle to within the scatter of the available DNS data.

3.3. Heat transfer coefﬁcients The primary subject of engineering interest in the study of passive scalar ﬁelds is the transfer coefﬁcient at the wall, which can be expressed in terms of the Stanton number, (cid:3)

(cid:2)

dT dy ub(Tm − Tw)

α

= 1 + u b

w

St =

,

θ+ m

where Tm is the mixed mean temperature (Kays et al. 1980),

(cid:5)

(cid:4)

R

Tm = 2

r(cid:4)uz(cid:5)(cid:4)T(cid:5)dr

(ubR2),

0 with θm = (Tm − Tw)/Tτ or, more frequently, in terms of the Nusselt number,

Nu = StReb Pr. A predictive formula for the heat transfer coefﬁcient in wall-bounded turbulent ﬂows was derived by Kader & Yaglom (1972), based on the assumed existence of logarithmic layers for the mean velocity and temperature proﬁles as a function of the wall distance, and on universality of the core layer in defect representation. For the purpose of critically evaluating the assumptions made in the derivation of Kader’s formula, we show (in ﬁgure 9) the distributions of the bulk and mean centreline values (namely, at r = 0) of velocity (ﬁgure 9a) and temperature (ﬁgure 9b), as a function of the friction Reynolds number, Consistently with theoretical expectations (e.g. Monkewitz 2021), the data suggest logarithmic increase of the bulk and centreline velocity with Reτ according to

+ u b

= 1 k

logReτ + B, U

+ CL

= 1 k

logReτ + BCL,

with k = 0.387, B = 1.229 and BCL = 5.85 (Pirozzoli et al. 2021). The relative standard deviation of the above formulae with respect to DNS data is approximately 0.2% for ub

940 A45-12

100

(3.6)

(3.7)

(3.8)

(3.9a,b)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

(a)

30

(b)

30

L +C u

24

L +C Θ

,

24

, b+ u

18

+m θ

, b+ θ

18

12

102

103 Reτ

104

12

102

103 Reτ

104

b , θ+

+

b ) are CL) with circles. Diamonds in (b) denote the mixed mean m ). The dashed lines denote logarithmic ﬁts of the DNS data. The dash-dotted line in (b) refers

Figure 9. Bulk and centreline values of (a) axial velocity and (b) temperature. Bulk values (u CL, Θ+ denoted with squares and centreline values (U temperature (θ+ to the ﬁt (3.11).

+

and 0.5% for UCL. Similar trends are here observed for the temperature ﬁeld, which also exhibits logarithmic growth of the mean and centreline temperature with Reτ, according to

θ+ b

= 1 kθ

logReτ + β, Θ+ CL

= 1 kθ

logReτ + βCL,

(3.10a,b)

with θ+ = (Tb − Tw)/Tτ, and ﬁt of the DNS data suggests kθ = 0.459, β = 2.96 and b βCL = 6.46. The relative standard deviation of the above formulae with respect to DNS data is approximately 0.06% for θb and 0.5% for ΘCL, hence the quality of the ﬁts is excellent as for the axial velocity ﬁeld, and the resulting estimates of the ﬂow constants, and especially of the scalar von Kármán constant appear to be quite robust.

Considering a large number of experimental works, Kader & Yaglom (1972) suggested kθ ≈ 0.47, and provided empirical formulae for the additive constants as a function of the Prandtl number, β(Pr) = 12.5Pr2/3 + 1/kθ logPr − 5.3 and βCL = β + 0.6. Studies carried out by means of DNS in planar channel ﬂows with CHF show some scatter in the prediction of kθ, likely due to low-Reynolds-number effects. For instance, Kawamura et al. (1999) reported 0.40 ≤ kθ ≤ 0.42, Abe et al. (2004) reported kθ ≈ 0.43, whereas more data at higher Reynolds number suggest kθ ≈ 0.44 (Alcántara-Ávila et al. 2021). Studies carried out with CMT typically tend to yield slightly higher values, namely kθ ≈ 0.46 (Pirozzoli et al. 2016), thus closer to Kader’s prediction. It should be noted that all the above estimates were based on attempting to ﬁt the temperature proﬁles with a logarithmic law, which as shown previously may not be a good approximation, especially at low Reynolds number. The method herein used to estimate the scalar von Kármán constant from the bulk and centreline temperatures yields greater accuracy and robustness, resulting in a value similar to that suggested by Kader & Yaglom (1972), and to values obtained using a similar approach, based on channel ﬂow DNS data (Abe & Antonia 2017). It is also worth pointing out that the additive constants β,βCL in (3.10a,b) do depend on the molecular Prandtl number (Kader & Yaglom 1972), hence the values herein reported are speciﬁc to the Pr = 1 case.

Determination of the appropriate Reynolds number trends of the mixed mean temperature is not as straightforward as for the bulk or the centreline temperature, because it involves integrating the product of the mean velocity and temperature distributions.

940 A45-13

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

Simple developments (Kader & Yaglom 1972) suggest the expected behaviour to be

θ+ m

= Θ+ CL

−β2 +

β3 + u b

,

with β2 and β3 universal constants, hence, on account of (3.9a,b) and (3.10a,b), deviations from logarithmic dependence on Reτ are to be expected. Figure 9 shows that it is indeed the case, and the mixed mean temperature (diamond symbols) seems to follow a near logarithmic distribution only at the highest Reynolds numbers under consideration. Values of the constants β2 = 4.92, β3 = 39.6, in (3.11) yield a fair ﬁt of the DNS data. Although the scatter in the analytical ﬁt (see the dash-dotted line) is more signiﬁcant than for the other ﬂow properties, this is clearly more accurate than a simple logarithmic ﬁt. Corrections to the logarithmic law in the mixed mean temperature were generally disregarded in previous studies (Kader & Yaglom 1972; Abe & Antonia 2017), although they can be included in the analysis without additional difﬁculty.

Proceeding as proposed by Kader & Yaglom (1972), it is straightforward to derive a

predictive formula for the inverse Stanton number,

1 St

= k kθ

8 λ

+

(cid:6) βCL − β2 − k kθ

B

(cid:7)(cid:8)

8 λ

+ β3,

+ where the friction factor λ = 8/u can be obtained from (3.9a,b). Assuming strictly b logarithmic variation of the mixed mean temperature with Reτ (hence, setting β3 = 0), Kader & Yaglom (1972) arrived at the following expression,

2

1 St

= 2.12log(Reb

√

λ/4) + 12.5Pr2/3 + 2.12logPr − 10.1

√

λ/8

,

which could also be rearranged to a form more similar to (3.12). Additional correlations which are in wide use in the engineering practice were proposed by Gnielinski (1976),

Nu =

Prλ/8(Reb − 1000) 1 + 12.7(λ/8)1/2(Pr2/3 − 1)

,

and by Kays et al. (1980),

Nu = 0.022Re0.8 Last, direct ﬁtting of the DNS data (at Pr = 1) with a power-law expression yields

b Pr0.5.

Nu = 0.0219Re0.804

b

.

All the above predictive formulae are tested in ﬁgure 10, showing the predicted inverse Stanton number (ﬁgure 10a) and Nusselt number (ﬁgure 10b). With little surprise, we ﬁnd that (3.12) with DNS-informed deﬁnition of the coefﬁcients matches the DNS data quite well, with maximum relative error of 0.8%. Despite minor differences in the coefﬁcients with respect to the baseline predictive formula (3.15), the direct power-law ﬁt given in (3.16) is also quite accurate, except at low Reb. All other formulae fall short of the DNS data for St by up to 5%. This difference may be partly due to inaccuracy of correlations based on old experimental data, to the fact that those are mainly tuned for the Pr = 0.71 case, whereas here Pr = 1, but also to the fact that the CMT setup herein used tends to slightly overpredict the heat ﬂux as compared with the CHF approach (Abe & Antonia 2017; Alcántara-Ávila et al. 2021). It is interesting that differences are levelled off when

940 A45-14

(3.11)

(3.12)

(3.13)

(3.14)

(3.15)

(3.16)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

(a)

600

(b)

103

500

102

0.025

1/St

400

300

Nu

101

8 . 0 b– e R u N

0.023

200

104

105

100

104

0.021

104

105

105

Reb

Reb

Figure 10. Distribution of (a) inverse Stanton number and (b) Nusselt number obtained from DNS (circles), and as predicted from (3.12) (solid line), from Kader’s formula ((3.13), dashed), from the power-law data ﬁt (3.16) (dotted), from Gnielinski analogy ((3.14), dot-dot-dashed) and from Kays–Crawford correlation ((3.15), dot-dashed). The inset in (b) shows the Nusselt number in compensated form (Nu × Re

−0.8 b

).

the popular representation in terms of the Nusselt number is used, as in ﬁgure 10(b). This suggests that the 1/St representation should be used when relatively small differences must be discriminated, or perhaps the compensated Nusselt representation used in the inset of ﬁgure 10(b).

3.4. Temperature ﬂuctuations statistics The distributions of the axial velocity and temperature variances are shown in ﬁgure 11, in inner scaling. All the proﬁles feature a prominent peak in the buffer layer at y+ ≈ 15, and an outer-layer shoulder which starts to form at sufﬁciently high Reynolds number. The most notable Reynolds number effect on the temperature variance proﬁles is sustained increase, as is the case of the axial velocity variance (Marusic & Monty 2019). According to Townsend’s attached eddy model (Townsend 1976), growth of the wall-parallel velocity variances is expected to be logarithmic with Reτ, on account of increased inﬂuence of ‘distant’ eddies. According to the spectral maps presented in ﬁgure 4, the attached-eddy hypothesis is also expected to apply to the temperature ﬁeld. In fact, logarithmic growth of the peak temperature variance in turbulent planar channels was observed by Pirozzoli et al. (2016). This is conﬁrmed by the present pipe DNS data, see ﬁgure 11(b), which compare the growth of the peak temperature variance with the axial velocity variance. Although the inferred growth rate is the same, the magnitude of the temperature variance peak is larger than for the axial velocity. This is the consequence (Pirozzoli et al. 2014) of near equality of the corresponding production terms in the buffer layer, however with extra energy draining in the axial velocity variance equation from the pressure term which tends to equalise kinetic energy across all the velocity components. No evidence is found based on the present data for saturation of the logarithmic growth, which has been inferred for the axial velocity variance in recent theoretical studies (Chen & Sreenivasan 2021).

The distributions of the turbulent heat ﬂux, (cid:4)urθ(cid:5), shown in ﬁgure 12, are visually indistinguishable from the corresponding turbulent shear stresses (reported with dashed lines). This is a further conﬁrmation that the lift-up mechanism which is responsible for the establishment of correlation of uz and θ with vertical velocity ﬂuctuations, ur, is nearly the same, and of essentially linear nature (Jiménez 2013). In both cases, the peak position grows approximately as the square root of Reτ, corresponding to the minimal wall

940 A45-15

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

(a)

10

(b)

11

8

10

+ (cid:3) 2 θ (cid:2)

6

P +I (cid:3) 2 θ (cid:2)

9

, + (cid:3) z2 u (cid:2)

4

,

P +I (cid:3) z2 u (cid:2)

8

2

7

0 100

101

102 y+

103

104

6 102

103 Reτ

Figure 11. Distribution of (a) temperature variances and (b) corresponding peak value as a function of Reτ. The dashed lines in (a) denote the distributions of the axial velocity variance. In (b), circles correspond to the peak temperature variance and squares to the peak axial velocity variance. Dash-dotted and dashed lines correspond to the associated logarithmic ﬁts, namely (cid:4)θ2(cid:5)+ = 0.67logReτ + IP 3.3. Refer to table 1 for colour codes.

(cid:5)+ IP

= 0.68logReτ + 3.9, (cid:4)u2 z

(a)

1.0

(b)

4.0

+ (cid:3) θ

r

u (cid:2)

0.8

0.6

0.4

0.2

x a m – 1

, + (cid:3) θ

2 / τ1 e R



) + (cid:3)

r

u (cid:2)

z

u

x a m – 1 (

r

u (cid:2)

3.5

3.0

2.5

0 100

101

102 y+

103

104

2.0

102

103 Reτ

Figure 12. Distribution of (a) turbulent heat ﬂux and (b) corresponding peak value (complement to one and premultiplied by Re1/2 ) as a function of Reτ. The dashed lines in (a) (barely visible) correspond to the distributions of the turbulent shear stress. In (b), circles correspond to the peak turbulent heat ﬂux and squares to the peak turbulent shear stress. Dashed and dash-dotted lines correspond to the theoretical predictions (3.17) and (3.18), respectively. Refer to table 1 for colour codes.

τ

distance for a logarithmic layer to develop (Klewicki, Fife & Wei 2009). Slight differences between the two distributions are nevertheless responsible for differences in the mean axial velocity and temperature proﬁles, on account on mean momentum balance and mean thermal balance (Saha et al. 2015; Zhou, Pirozzoli & Klewicki 2017). These differences are better appreciated in ﬁgure 12(b), where we show the peak turbulent heat ﬂux and shear stress as a function of Reτ. Based on mean momentum balance, and assuming the presence of a logarithmic layer (which is a bit inaccurate in view of what previously said), Orlandi et al. (2015) inferred that the peak turbulent shear stress should scale as

max(cid:4)uruz(cid:5) ≈ 1 − 2√

kReτ

.

Similarly, it can be readily shown, based on mean thermal balance and assuming a log layer in the mean temperature distribution, that the peak turbulent heat ﬂux should

940 A45-16

104

104

(3.17)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

(a)

1.2

(b)

1.2

1.0

1.0

Prt

0.8

0.8

0.6

10–1

100

101

y+

102

103

104

0.6

0

0.2

0.4

y/R

0.6

0.8

1.0

Figure 13. Distribution of turbulent Prandtl number, in (a) inner and (b) outer coordinates. The dashed line denotes Pr = k/kθ = 0.843. In (a), the dash-dotted line denotes the prediction of (3.20) with the original set of constants and the dotted line the same formula, with B = 32.2. The dotted line in (b) denotes the ﬁtting function (3.21). Refer to table 1 for colour codes.

scale as

max(cid:4)urθ(cid:5) ≈ 1 −

2√

kθReτ

.

(3.18)

These two trends are compared in ﬁgure 12(b). Whereas the data points coincide at low Reynolds number, some segregation is observed at the highest Reynolds numbers, at which the peaks tend to follow their respective theoretical distributions.

A quantity of great relevance in turbulence models of scalar transport is the turbulent

Prandtl number, deﬁned as (Cebeci & Bradshaw 1984)

Prt =

νt αt

=

(cid:4)uruz(cid:5) (cid:4)urθ(cid:5)

dΘ/dy dU/dy

,

(3.19)

whose distributions are shown in ﬁgure 13. As expected based on its deﬁnition, Prt ≈ k/kθ ≈ 0.843, through a large part of the outer layer, say from y+ ≈ 100 to y/h ≈ 0.25. This is quite similar to what was found in channels (Pirozzoli et al. 2017; Alcántara-Ávila et al. 2021) and in general agreement with the values Prt ≈ 0.85 suggested in reference publications (Kader 1981; Cebeci & Bradshaw 1984). Closer to the wall, the turbulent Prandtl number tends to exhibit a plateau with nearly unit value within the buffer layer (5 ≤ y+ ≤ 40), as a result of the close similarity of the velocity and temperature ﬁelds in that region. At y+ (cid:2) 1 the eddy viscosity tends to exceed the eddy diffusivity, and as a consequence Prt > 1. Theoretical estimates for the near-wall behaviour of Prt were proposed by Cebeci (1973), based on a mixing length model with van Driest near-wall damping. This results in the estimate

Prt = k kθ

1 − exp(−y+/A) 1 − exp(−y+/B)

,

(3.20)

where A and B are the damping functions for the velocity and scalar ﬁelds, respectively. The original choice of those two parameters, A = 26, B = 34.96 (for Pr = 1), captures the near-wall growth of Prt, although its value is overpredicted. Changing the damping constant for the temperature ﬁeld to B = 32.2 (see the dotted grey line in ﬁgure 13a) improves the ﬁt signiﬁcantly, although the buffer-layer plateau is not captured. Regarding the outer layer, ﬁgure 13(b) seems to show tendency to universality in outer scaling at

940 A45-17

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

sufﬁciently high Reynolds number. As suggested by Rotta (1962) and Abe & Antonia (2017), the data are well ﬁtted by a quadratic correlation, and we ﬁnd

Prt = 0.87 − 0.3(y/R)2,

for y/R (cid:3) 0.25.

4. Concluding comments We have analysed the dynamics of passive scalars in turbulent pipe ﬂow up to Reτ ≈ 6000, at unit Prandtl number. Compared with previous studies, the Reynolds number is sufﬁciently high here that the results are representative of realistic fully developed turbulence. A general expected ﬁnding, at least at Pr = 1, is that passive scalars exhibit a behaviour similar to the axial velocity ﬁeld, being organised into streaks in the buffer layer and featuring low-wavenumber azimuthal modes in the bulk of the ﬂow. The spectral maps also highlight close similarities at the large scales, which at the higher Reynolds number under study (Reτ ≈ 6000), exhibit a prominent ridge with eddy size proportional to the wall distance, as suggested by Townsend’s attached-eddy model. Besides overall similarity, differences are found as the passive scalar ﬁeld has stronger tendency to form steep fronts, which are prevented in the velocity ﬁeld by the action of pressure. Hence, scalar spectra tend to exhibit shallower k−4/3 inertial range, for which the present DNS data provide convincing evidence. Regarding the one-point statistics, we ﬁnd that the mean scalar proﬁles in the overlap layer can be conveniently approximated by logarithmic distributions. However, signiﬁcant improvement is obtained through addition of a linear corrective term scaling in outer units, which yields good ﬁt of the data up to y/R ≈ 0.44. Further away from the wall, the mean scalar proﬁle is approximated with excellent accuracy by a simple quadratic distribution. Notable differences are found in the von Kármán constants, which we estimate to be kθ ≈ 0.459 for the scalar ﬁeld, and k ≈ 0.387 for the axial velocity ﬁeld, which we obtain by ﬁtting the trends of the respective bulk values with the friction Reynolds number, with estimated error much less than 1%. The DNS data help explaining this difference as the result of greater effective diffusivity of the scalar ﬁeld resulting from the formation of smaller scales. Reynolds number effects are apparent in the distributions of the passive scalar variance, which show sustained logarithmic growth of the inner peak magnitude, as after Townsend’s attached-eddy hypothesis. No evidence for saturation of this growth is found, at the Reynolds numbers under scrutiny. Notably, the growth rate is found to be very nearly the same as for the axial velocity variance.

Full insight into the scalar and velocity statistics provided by DNS allows to pinpoint possible limitations of classical analyses of heat transfer in smooth pipes and of classical modelling assumptions for passive scalar transport. In particular, whereas logarithmic dependence of the mixed mean temperature over Reτ was assumed by Kader (1981), we ﬁnd that ﬁnite-Re deviations should be accounted for, thus obtaining the predictive formula (3.12), which is found to be more accurate than the classical Kader’s formula (3.13). It is noteworthy that deviations of empirical formulae employed in the engineering practice are sometimes hidden in the traditional Nu versus Reb representation, whereas they show up much more clearly when the inverse Stanton number is reported, as in ﬁgure 10(a). Regarding the distributions of the turbulent Prandtl number, which is needed for turbulence modelling, the DNS data show that in the overlap layer the assumption Prt ≈ 0.843 is quite appropriate. However, signiﬁcant deviations are found farther from the wall, with quadratic decrement with the wall distance. Deviations are also

940 A45-18

(3.21)

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

found in the near-wall region, where Prt exceeds unity. This fact is roughly acknowledged in existing engineering correlations (Cebeci 1973; Kays et al. 1980), but the accuracy is far from acceptable. Whereas the above-noted shortcoming of common modelling assumptions and predictive formulae may be minor to be appreciated in practical contexts, as may be related with the assumed unit Prandtl number, with the particular form of volumetric heating used as forcing and with assumed isothermal wall, the procedure herein outlined nevertheless serves to illustrate a general use of DNS as a way for testing hypotheses in more general situations, for instance at higher Prandtl number, at which the thermal boundary layer is thinner than the kinematic one.

A natural extension of the present study would be, in fact, considering the case of lower and higher Prandtl numbers, which we could not include in the present DNS owing to memory restrictions. That would allow to verify the Prandtl number dependence of the βCL constant in the main predictive equation for the heat transfer (3.12). Equally interesting would be carrying out the present DNS within the CHF approach, whereby strictly constant heat ﬂux is retained in time. That would allow the reasons for the small (but sizeable) deviations observed in ﬁgure 10 to be elucidated with respect to engineering correlations in current use.

Acknowledgements. We thank A. Ceci and M. Yu for help in processing the data. We acknowledge that the results reported in this paper have been achieved using the PRACE Research Infrastructure resource MARCONI based at CINECA, Casalecchio di Reno, Italy, under project PRACE no. 2021240112.

Funding. This research received no speciﬁc grant from any funding agency, commercial or not-for-proﬁt sectors.

Declaration of interests. The authors report no conﬂict of interest.

Data availability statement. The data that support the ﬁndings of this study are openly available at http://newton.dma.uniroma1.it/database/.

Author ORCIDs.

Sergio Pirozzoli https://orcid.org/0000-0002-7160-3023; Roberto Verzicco https://orcid.org/0000-0002-2690-9998; Paolo Orlandi https://orcid.org/0000-0002-0305-5723.

REFERENCES

ABE, H. & ANTONIA, R.A. 2009 Near-wall similarity between velocity and scalar ﬂuctuations in a turbulent

channel ﬂow. Phys. Fluids 21, 025109.

ABE, H. & ANTONIA, R.A. 2017 Relationship between the heat transfer law and the scalar dissipation function

in a turbulent channel ﬂow. J. Fluid Mech. 830, 300–325.

ABE, H., KAWAMURA, H. & MATSUO, Y. 2004 Surface heat-ﬂux ﬂuctuations in a turbulent channel ﬂow up

to Reτ = 1020 with Pr = 0.025 and 0.71. Intl J. Heat Fluid Flow 25, 404–419.

AFZAL, N. & YAJNIK, K. 1973 Analysis of turbulent pipe and channel ﬂows at moderately large Reynolds

number. J. Fluid Mech. 61, 23–31.

AHN, J., LEE, J.H., LEE, J., KANG, J.-H. & SUNG, H.J. 2015 Direct numerical simulation of a 30R long

turbulent pipe ﬂow at Reτ = 3000. Phys. Fluids 27, 065110.

AKSELVOLL, K. & MOIN, P. 1996 An efﬁcient method for temporal integration of the Navier–Stokes equations

in conﬁned axisymmetric geometries. J. Comput. Phys. 125, 454–463.

ALCÁNTARA-ÁVILA, F., HOYAS, S. & PÉREZ-QUILES, M.J. 2018 DNS of thermal channel ﬂow up to

Reτ = 2000 for medium to low Prandtl numbers. Intl J. Heat Mass Transfer 127, 349–361.

ALCÁNTARA-ÁVILA, F., HOYAS, S. & PÉREZ-QUILES, M.J. 2021 Direct numerical simulation of thermal

channel ﬂow for Reτ = 5000 and Pr = 0.71. J. Fluid Mech. 916, A29.

ANTORANZ, A., GONZALO, A., FLORES, O. & GARCIA-VILLALBA, M. 2015 Numerical simulation of heat transfer in a pipe with non-homogeneous thermal boundary conditions. Intl J. Heat Fluid Flow 55, 45–51.

CANTWELL, B.J. 2019 A universal velocity proﬁle for smooth wall pipe ﬂow. J. Fluid Mech. 878, 834–874.

940 A45-19

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

S. Pirozzoli, J. Romero, M. Fatica, R. Verzicco and P. Orlandi

CEBECI, T. 1973 A model for eddy conductivity and turbulent Prandtl number. J. Heat Transfer 95, 227–234. CEBECI, T. & BRADSHAW, P. 1984 Physical and Computational Aspects of Convective Heat Transfer.

Springer-Verlag.

CHEN, X. & SREENIVASAN, K.R. 2021 Reynolds number scaling of the peak turbulence intensity in wall

ﬂows. J. Fluid Mech. 908, R3.

GNIELINSKI, V. 1976 New equations for heat and mass transfer in turbulent pipe and channel ﬂow. Intl Chem.

Engng 16, 359–367.

GOWEN, R.A. & SMITH, J.W. 1967 The effect of the Prandtl number on temperature proﬁles for heat transfer

in turbulent pipe ﬂow. Chem. Engng Sci. 22, 1701–1711.

HARLOW, F.H. & WELCH, J.E. 1965 Numerical calculation of time-dependent viscous incompressible ﬂow

of ﬂuid with free surface. Phys. Fluids 8, 2182–2189.

HOYAS, S. & JIMÉNEZ, J. 2006 Scaling of velocity ﬂuctuations in turbulent channels up to Reτ = 2003. Phys.

Fluids 18, 011702.

HUTCHINS, N. & MARUSIC, I. 2007 Evidence of very long meandering features in the logarithmic region of

turbulent boundary layers. J. Fluid Mech. 579, 1–28.

JIMÉNEZ, J. 2013 How linear is wall-bounded turbulence? Phys. Fluids 25 (11), 110814. JIMÉNEZ, J. 2018 Coherent structures in wall-bounded turbulence. J. Fluid Mech. 842, P1. JIMÉNEZ, J. & MOSER, R.D. 2007 What are we learning from simulating wall turbulence? Phil. Trans. R.

Soc. Lond. A 365, 715–732.

JIMÉNEZ, J. & PINELLI, A. 1999 The autonomous cycle of near-wall turbulence. J. Fluid Mech. 389, 335–359. KADER, B.A. 1981 Temperature and concentration proﬁles in fully turbulent boundary layers. Intl J. Heat

Mass Transfer 24, 1541–1544.

KADER, B.A. & YAGLOM, A.M. 1972 Heat and mass transfer laws for fully turbulent wall ﬂows. Intl J. Heat

Mass Transfer 15 (12), 2329–2351.

KAWAMURA, H., ABE, H. & MATSUO, Y. 1999 DNS of turbulent heat transfer in channel ﬂow with respect

to Reynolds and Prandtl number effects. Intl J. Heat Fluid Flow 20, 196–207.

KAYS, W.M., CRAWFORD, M.E. & WEIGAND, B. 1980 Convective Heat and Mass Transfer. McGraw-Hill. KIM, J. & MOIN, P. 1985 Application of a fractional-step method to incompressible Navier–Stokes equations.

J. Comput. Phys. 59, 308–323.

KIM, J. & MOIN, P. 1989 Transport of passive scalars in a turbulent channel ﬂow. In Turbulent Shear Flows,

vol. 6, pp. 85–96. Springer.

KLEWICKI, J., FIFE, P. & WEI, T. 2009 On the logarithmic mean proﬁle. J. Fluid Mech. 638, 73–93. KRUG, D., PHILIP, J. & MARUSIC, I. 2017 Revisiting the law of the wake in wall turbulence. J. Fluid Mech.

811, 421–435.

LEE, M. & MOSER, R.D. 2015 Direct simulation of turbulent channel ﬂow layer up to Reτ = 5200. J. Fluid

Mech. 774, 395–415.

LENAERS, P., LI, Q., BRETHOUWER, G., SCHLATTER, P. & ÖRLÜ, R. 2012 Rare backﬂow and extreme

wall-normal velocity ﬂuctuations in near-wall turbulence. Phys. Fluids 24, 035110.

LOHSE, D. 1994 Temperature spectra in shear ﬂow and thermal convection. Phys. Lett. A 196, 70–75. LUCHINI, P. 2017 Universality of the turbulent velocity proﬁle. Phys. Rev. Lett. 118 (22), 224501. LUCHINI, P. 2018 Structure and interpolation of the turbulent velocity proﬁle in parallel ﬂow. Eur. J. Mech.

(B/Fluids) 71, 15–34.

MARUSIC, I. & MONTY, J.P. 2019 Attached eddy model of wall turbulence. Annu. Rev. Fluid Mech. 51,

49–74.

MOIN, P. & VERZICCO, R. 2016 On the suitability of second-order accurate discretizations for turbulent ﬂow

simulations. Eur. J. Mech. (B/Fluids) 55, 242–245.

MONIN, A.S. & YAGLOM, A.M. 1971 Statistical Fluid Mechanics: Mechanics of Turbulence, vol. 1. MIT

Press.

MONKEWITZ, P.A. 2021 The late start of the mean velocity overlap log law at y+ = O(103) – a generic feature

of turbulent wall layers in ducts. J. Fluid Mech. 910, A45.

NAGANO, Y. & TAGAWA, M. 1988 Statistical characteristics of wall turbulence with a passive scalar. J. Fluid

Mech. 196, 157–185.

NICKELS, T.B., MARUSIC, I., HAFEZ, S.M. & CHONG, M.S. 2005 Evidence of the k−1 law in a

high-Reynolds-number turbulent boundary layer. Phys. Rev. Lett. 95, 074501.

ORLANDI, P., BERNARDINI, M. & PIROZZOLI, S. 2015 Poiseuille and Couette ﬂows in the transitional and

fully turbulent regime. J. Fluid Mech. 770, 424–441.

ORLANDI, P. & FATICA, M. 1997 Direct simulations of turbulent ﬂow in a pipe rotating about its axis. J. Fluid

Mech. 343, 43–72.

940 A45-20

s s e r P y t i s r e v i n U e g d i r b m a C y b e n

i l

n o d e h s i l

b u P 5 6 2 2 2 0 2 m

.

.

f j / 7 1 0 1 0 1 / g r o

.

. i

o d / / : s p t t h

Passive scalars in pipe ﬂow

PILLER, M. 2005 Direct numerical simulation of turbulent forced convection in a pipe. Intl J. Numer. Meth.

Fluids 49 (6), 583–602.

PIROZZOLI, S. 2014 Revisiting the mixing-length hypothesis in the outer part of turbulent wall layers: mean

ﬂow and wall friction. J. Fluid Mech. 745, 378–397.

PIROZZOLI, S., BERNARDINI, M. & ORLANDI, P. 2014 Turbulence statistics in Couette ﬂow at high Reynolds

number. J. Fluid Mech. 758, 327–343.

PIROZZOLI, S., BERNARDINI, M. & ORLANDI, P. 2016 Passive scalars in turbulent channel ﬂow at high

Reynolds number. J. Fluid Mech. 788, 614–639.

PIROZZOLI, S., BERNARDINI, M., VERZICCO, R. & ORLANDI, P. 2017 Mixed convection in turbulent

channels with unstable stratiﬁcation. J. Fluid Mech. 821, 482–516.

PIROZZOLI, S. & ORLANDI, P. 2021 Natural grid stretching for DNS of wall-bounded ﬂows. J. Comput. Phys.

439, 110408.

PIROZZOLI, S., ROMERO, J., FATICA, M., VERZICCO, R. & ORLANDI, P. 2021 One-point statistics for

turbulent pipe ﬂow up to Reτ ≈ 6000. J. Fluid Mech. 926, A28.

REDJEM-SAAD, L., OULD-ROUISS, M. & LAURIAT, G. 2007 Direct numerical simulation of turbulent heat

transfer in pipe ﬂows: effect of Prandtl number. Intl J. Heat Fluid Flow 28 (5), 847–861.

ROTTA, J.C. 1962 Turbulent boundary layers in incompressible ﬂow. Prog. Aerosp. Sci. 2 (1), 1–95. RUETSCH, G. & FATICA, M. 2014 CUDA Fortran for Scientists and Engineers. Elsevier. RUSSO, S. & LUCHINI, P. 2017 A fast algorithm for the estimation of statistical error in DNS (or experimental)

time averages. J. Comput. Phys. 347, 328–340.

SAHA, S., CHIN, C., BLACKBURN, H.M. & OOI, A.S.H. 2011 The inﬂuence of pipe length on thermal

statistics computed from dns of turbulent heat transfer. Intl J. Heat Fluid Flow 32 (6), 1083–1097.

SAHA, S., KLEWICKI, J.C., OOI, A.S.H. & BLACKBURN, H.M. 2015 Comparison of thermal scaling

properties between turbulent pipe and channel ﬂows via DNS. Intl J. Therm. Sci. 89, 43–57.

STEVENS, R.J.A.M., VAN DER POEL, E.P., GROSSMANN, S. & LOHSE, D. 2013 The unifying theory of

scaling in thermal convection: the updated prefactors. J. Fluid Mech. 730, 295–308.

STRAUB, S., FOROOGHI, P., MAROCCO, L., WETZEL, T. & FROHNAPFEL, B. 2019 Azimuthally inhomogeneous thermal boundary conditions in turbulent forced convection pipe ﬂow for low to medium Prandtl numbers. Intl J. Heat Fluid Flow 77, 352–358.

SUBRAMANIAN, C.S. & ANTONIA, R.A. 1981 Effect of Reynolds number on a slightly heated turbulent

boundary layer. Intl J. Heat Mass Transfer 24, 1833–1846.

TOWNSEND, A.A. 1976 The Structure of Turbulent Shear Flow, 2nd edn. Cambridge University Press. VERZICCO, R. & ORLANDI, P. 1996 A ﬁnite-difference scheme for three-dimensional incompressible ﬂows

in cylindrical coordinates. J. Comput. Phys. 123, 402–414.

WU, X. & MOIN, P. 2008 A direct numerical simulation study on the mean velocity characteristics in turbulent

pipe ﬂow. J. Fluid Mech. 608, 81–112.

ZHOU, A., KLEWICKI, J. & PIROZZOLI, S. 2019 Properties of the scalar variance transport equation in

turbulent channel ﬂow. Phys. Rev. Fluids 4 (2), 024606.

ZHOU, A., PIROZZOLI, S. & KLEWICKI, J. 2017 Mean equation based scaling analysis of fully-developed

turbulent channel ﬂow with uniform heat generation. Intl J. Heat Mass Transfer 115, 50–61.

940 A45-21