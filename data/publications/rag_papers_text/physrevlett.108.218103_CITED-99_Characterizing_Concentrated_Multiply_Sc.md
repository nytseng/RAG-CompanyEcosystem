This is the accepted manuscript made available via CHORUS. The article has been published as:

Characterizing Concentrated, Multiply Scattering, and Actively Driven Fluorescent Systems with Confocal Differential Dynamic Microscopy Peter J. Lu (陸述義), Fabio Giavazzi, Thomas E. Angelini, Emanuela Zaccarelli, Frank

Jargstorff, Andrew B. Schofield, James N. Wilking, Mark B. Romanowsky, David A. Weitz,

and Roberto Cerbino

Phys. Rev. Lett. 108, 218103 — Published 22 May 2012

DOI: 10.1103/PhysRevLett.108.218103

LT12127

Characterizing concentrated, multiply-scattering and actively-driven ﬂuorescent systems with Confocal Differential Dynamic Microscopy (ConDDM)

Peter J. Lu (陸述義),1 Fabio Giavazzi,2 Thomas E. Angelini,1 Emanuela Zaccarelli,3 Frank Jargstorff,4 Andrew B. Schoﬁeld,5 James N. Wilking,1 Mark B. Romanowsky,1 David A. Weitz,1 and Roberto Cerbino2 1Department of Physics and SEAS, Harvard University, Cambridge, Massachusetts 02138, USA 2Dipartimento di Chimica, Biochimica e Biotecnologie per la Medicina, Universita degli Studi di Milano, I-20090, Italy 3CNR-ISC and Dipartimento di Fisica, Universita di Roma La Sapienza, I-00185 Rome, Italy 4NVIDIA, Santa Clara, California 95050, USA 5Department of Physics, University of Edinburgh, Edinburgh EH9 3JZ, United Kingdom

We introduce confocal differential dynamic microscopy (ConDDM), a new technique yielding information comparable to that given by light scattering, but in dense, opaque, ﬂuorescent samples of micron-sized objects that cannot be probed easily with other existing techniques. We measure the correct wavevector q-dependent structure and hydrodynamic factors of concentrated hard-sphere-like colloids. We characterize concentrated swimming bacteria, observing ballistic motion in the bulk and a new compressed-exponential scaling of dy- namics, and determine the velocity distribution; by contrast, near the coverslip, dynamics scale differently, suggesting that bacterial motion near surfaces fundamentally differs from that of freely-swimming organisms.

N O T FO R DISTRIB U TIO N RE VIE W C OPY

those that can be measured accurately with DLS and DDM; our measured diffusion coefﬁcient is in good agreement with the value determined using other techniques. Moreover, con- focal microscopy allows sufﬁcient signal, even in these dense samples, to measure meaningfully the difference between im- age pairs separated by long time delays. This provides infor- mation on static structure, analogous to that given by static light scattering (SLS), but here for highly concentrated sam- ples that multiply-scatter light; our measurement of the static structure factor S(q) in colloidal suspensions is in quantita- tive agreement with theory and independent measurements. Furthermore, we combine these measurements to probe par- ticle interactions: our purely-experimental determinations of the hydrodynamic factor H(q) are in quantitative agreement with theory, which has not been achieved with any light-based technique for such dense suspensions. To illustrate further the technique’s power, we apply it to an actively-driven, biolog- ical system: dense, macroscopically-opaque suspensions of ﬂuorescent bacteria swimming freely. We observe new scal- ing ofdynamicsthatdependson distancefromthecoverslip, a new phenomena in the bulk not seen when organisms swim in a 2D plane near the cover slip, and determine the distribution of swimming velocities. We term this technique, which en- ables these measurements, confocal differential dynamic mi- croscopy (ConDDM).

Fluorescence imaging is an important and versatile form of optical microscopy. Fluorescent tags can selectively iden- tify speciﬁc features within an image, thereby enhancing con- trast; this is particularly powerful in biology and soft-matter physics. A major difﬁculty, however,is that all ﬂuorescent ob- jects within the illumination beam emit light, even if outside the microscope’s focal plane, hindering collection of high- quality images. Using a confocal pinhole, which limits de- tected light to only that originating from the focal plane, con- focal microscopy allows true 3D imaging. By its very nature, however, confocal microscopy is relatively slow; collecting a 3D stack of images usually requires several seconds, limiting the study of dynamics to relatively slow phenomena, charac- terized by timescales well in excess of a second[1, 2].

Even traditional brightﬁeld microscopy is limited in its ability to follow rapid dynamics; by contrast, another opti- cal method, dynamic light scattering (DLS), is well-suited to characterize dynamics at high speeds, speciﬁcally ensem- ble averages as a function of scattering wavevector q, albeit at the cost of losing real-space information[3]. One way to combine DLS with the advantages of real-space imaging in wideﬁeld is differential dynamic microscopy (DDM), which extends to lower-q information analogous to that given by DLS[4–6]. However, DDM has thus far been restricted to wideﬁeld imaging; consequently,like DLS, DDM only probes dilute suspensions[4–6]. No equivalent method exists for ﬂu- orescence, particularly in high-concentration samples where imaging is obscured. This severely limits the use of ﬂuores- cence microscopy for studies of dynamics in dense samples.

Our confocal ﬂuorescence microscope includes Nipkow spinning-disk [Yokogawa], CCD camera [QImaging], 100× oil 1.4 NA objective [Leica], solid-state 532-nm laser [Laser- glow]and hardwaretiming control[1]. We suspend spheres of sterically-stabilized PMMA with DiIC18 dye [2] in a solvent of 18% (by mass) cis-decahydronaphthalene (cDHN), 22% tetrahydronaphthalene (THN) and 60% tetrachloroethylene (TCE). At 25◦C, the solvent has density 1.280±0.002 g/cm3, dynamicviscosity 1.288±0.002mPa-sec, and refractiveindex n=1.505; particles remain neutrally buoyant for days, and are macroscopically transparent at close-packed densities.

In this Letter, we introduce a new technique using confo- cal ﬂuorescence microscopy that provides a powerful probe not only of rapid dynamics, but also of the static structure of dense, ﬂuorescent samples that multiply-scatter light, pre- cluding their study with other techniques. Motivated by DDM analysis, we examine the Fourier spectra of the differences between pairs of images within a sequence; the short-time differences conﬁrm diffusive motion of hard-sphere-like col- loidal suspensions, even at volume fractions φ far higher than

We collect multiple uninterrupted sequences of >1000 im- ages of 256×256 pixels, at a depth 20 µm from the cover

a

c

e

10 µm

b

d

f

103 102 101 0

)

q ∆

(

5

10 q (1/µm)

g

) t δ ∆

(

3K 2K 1K 0 0

h

B 0.2

A

0.4

0.6

0.8 δt (sec)

1.0

1.2

1.4

FIG. 1. (color online) (a) Raw confocal ﬂuorescence image of particles at φ=0.20. Difference between images separated in time by (b) δt=0.06 sec, (c) δt=0.25 sec and (d) δt=1.00 sec. (e) 2D ¯∆(~q,δt=1.00) averaged over 104 image pairs, and (f) its 1D az- imuthual average, ∆(q,δt=1.00), plotted on the same scale in q. (g) ∆(q,δt), where the function in (f) corresponds to the white rectan- −1,δt) shows the time evolution at constant gle. (h) ∆(q=3.9 µm q=3.9 µm

−1, and corresponds to blue rectangle in (g).

slip, at 33.4 frames per second; a typical image from the sam- ple at φ=0.20 is shown in Fig. 1(a). We select pairs of im- ages separated by a time interval δt and subtract one from the other, removing any time-independentbackground,shown for δt=0.06, 0.25 and 1.00 seconds in Figs. 1(b)-1(d). We calculate the 2D Fourier transform of this difference, square its magnitude to give a 2D power spectrum as a function of wavevector ~q=(qx,qy), and average for all image pairs of equal δt within the sequence [4, 5] to yield ¯∆(~q), shown for 104 image pairs in Fig. 1(e) for δt=1.00 sec. The original implemention of this algorithm [MATLAB], requires several hours of computation for typical image sequences; however, the numerous independent FFTs and image pair subtractions make this calculation well-suited to parallelization. There- fore, we implement the same algorithm on a graphics pro- cessing unit (GPU) [NVIDIA Tesla C2050 GPU, CUDA C, CuFFT, NPP]; our accelerated code is two orders of magni- tude faster, reducingprocessing time to arounda minute, mak- ing the experiment far more interactive.

The sample dynamics and structure are isotropic, evi- denced by the circular symmetry of ¯∆(~q) in ﬁg. 1(e); there- fore, we average azimuthally to determine ∆(q) as a func- 1 tion of scalar wavevector magnitude q≡(q2 2, shown in Fig. 1(f). Repeating this procedure for different δt yields the image structure function ∆(q,δt), shown in Fig. 1(g),

x + q2 y)

15

scattering angle

0.33º

3.3º

32.6º

ConDDM: point-scanner, φ=0.01

ConDDM: Nipkow, φ=0.005

100

DLS: φ<0.001

]

c e s [

)

10-1

1/(D0q2) 1/(v0q)

q ( τ

10-2

bacteria: 1 μm bacteria: 2 μm bacteria: 4 μm bacteria: 8 μm bacteria: 16 μm

0.1

1 q [1/µm]

10

FIG. 2. (color online) τ(q) for dilute colloidal suspensions, us- ing data from a Nipkow disk confocal (open blue triangles), point- scanning confocal (open red triangles) and DLS (ﬁlled black circles), scale at high-q as q−2 and fall on the same (dashed blue) line. At low- q, the Nipkow-disk data plateau to a far higher value than that from the point-scanner, demonstrating the latter’s higher resolution along the optical axis. For swimming bacteria, τ(q) data collected deep in −1 (dotted the bulk (open diamonds and squares) scale at high-q as q line), indicating ballistic motion; by contrast, data from bacteria near the cover slip (open circles) follow no clear power law, but instead are sigmoidal curves with inﬂection points near q≈0.8 µm−1.

where the slice outlined by the vertical (white) rectangle cor- responds to ∆(q,δt=1.00 sec) in ﬁg. 1(f). To probe tem- poral dependence, for each q we slice ∆(q,δt) along the δt axis; the data from one slice, outlined by the horizontal (blue) rectangle in Fig. 1(g), represents sample time evolu- tion at ﬁxed q=3.9 µm−1, and are marked with symbols in Fig. 1(h). For δt=0, ∆(q,δt→0)=B(q), a time-independent noise ﬂoor; as δt increases, the differences between images in each pair increase. Consequently, ∆(q,δt) rises until sat- urating when the images are totally decorrelated, following the form ∆(q,δt)=2A(q)[1 − g(q,δt)]+ B(q), where the im- age correlation function g(q,δt) is equivalent to the interme- diate scattering function in DLS. For dilute Brownian parti- cles, g(q,δt)≡exp[−δt/τ(q)], where τdil(q)≡1/(D0q2) and D0 is the single-particle diffusion coefﬁcient[4, 5]; our exper- imental data conform closely to this exponential form, shown with the solid curve in Fig. 1(h). We repeat the ﬁt for each q to yield estimates of A(q), B(q) and τ(q). The ﬁt is valid when q>qmin≡2π/L=0.2 µm−1, where L is the image size, and when q<qmax=8 µm−1. In general, qmax is set by the minimum distance particles move between successive frames, though here qmax coincides with a particle form factor mini- mum, shown with a dotted grey line in Fig. 3(a); these q values map to scattering angles between 0.4◦ and 25◦, well below those accessed easily with traditional light scattering setups.

At high q→qmax, the τdil(q) data from a dilute sample at φ=0.005 scale as q−2, as in DDM, shown in Fig. 2; the ﬁt to the data yields D0=0.338±0.005 µm2/s. For comparison,

2

we measure a dilute sample at φ<0.001 of the same parti- cles and solvent with DLS [ALV], which fall on the same dashed line shown in Fig. 2; the ﬁt yields DDLS =0.330±0.01 µm2/s, in quantitative agreement with the ConDDM-derived value, and a particle hydrodynamic radius ah= 508±6 nm via the Stokes-Einstein relation. By contrast, at low-q, confo- cal sectioning causes τ(q) in ConDDM to plateau to a con- stant τ(q→0)≡τz≈6 sec, roughly the time for particles to diffuse out of the confocal imaging plane, similar to ﬂuo- rescence correlation spectroscopy (FCS) [3]. We estimate τz∼=(δz)2/D0, where δz≈1.5 µm approximates the confocal slice thickness; separately, we measure the full-width, half- maximum (FWHM) of the axial point-spread function (PSF), by dispersing quantum dots on a cover slip, and ﬁnd it to be 1.6±0.1µm, comparableto δz. To test whetherthe plateau re- ﬂects generally the confocal ˆz-resolution, we repeat the mea- surements with a different confocal microscope: a resonant- galvanometer point-scanner with 63× oil 1.4 NA objective [Leica], collecting at 55.0 fps with a 0.5 Airy-disk pinhole. At high-q, the τ(q) data completely overlap the Nipkow and DLS data, shown in Fig. 2; by contrast, at low-q, we ﬁnd δz≈0.5 µm, close to the measured FWHM of 0.52±0.01 µm. These data demonstratethe novelability of ConDDM to characterize the effective in-situ PSF using any confocal microscope.

0

to measure meaningfully the long-time limit A(q) in dense samples, a new capability not possible in wideﬁeld DDM. In gen- eral, A(q)≡φP(q)S(q)T(q), whereP(q) is thesingle-particle form factor; S(q), the structure factor; and T(q), the imaging- system transfer function [5]. P(q) and T(q) are ﬁxed for sam- ples with the same particles and solvents. For dilute φ→0 suspensions, Sdil(q)=1 and Adil(q)=φdilT(q)P(q); therefore we can determine S(q) at any φ: S(q)=φdilA(q)/φAdil(q), as shown with ﬁlled symbols in Fig. 3(a). We compare this measured data to theoretical S(q) estimates within the Percus- Yevick (PY) model; the PY calculations are in excellent quan- titative agreement with our data, shown with solid curves in Fig. 3(a); in all cases, the ﬁts yield an estimate of particle ra- dius aPY=510±5 nm, within error of ah. To compare with traditional confocal microscope usage, we collect 3D stacks of these indexed-matched colloids, determine 3D particle po- sitions with software [1], and calculate S(q) with a discrete sum [2]. In all cases, the 3D data are slightly noisier but still in good agreement with both the ConDDM data and PY cal- culation, as shown with open symbols in Fig. 3(a).

Confocal sectioning allows enough signal

Simultaneously determining the DLS-like dynamic τ(q) (Fig. 2) and SLS-like static S(q) (Fig. 3(a)) provides a tantalizing new way to measure hydrodynamics directly, For diffusing spheres, g(q,δt) with no additional data. is an exponential at any φ for δt less than the Brown- ian time τB≡4a2/D0 [7]; gs(q,δt)∼=exp(−δt/τs(q)), where τs(q)=(D0q2)−1S(q)/H(q), and the hydrodynamic factor H(q) characterizes hydrodynamic interactions among parti- cles [7, 8]. We ﬁnd that H(q) remains below 1 and decreases with increasingφ, expectedforhard spheres[7] and consistent with previous XPCS measurements [8], as shown with open

3.3º

scattering angle

32.6º

)

q S

(

2.0

1.5

1.0

a

φ=0.04 φ=0.09 φ=0.20 φ=0.40

25 µm

0.5

)

q H

(

0.0 1.0

0.5

b

φ=.04 φ=.09 φ=.20

φ=.40

0.0

)

1.0

c

q S

(

0.5

25 µm

0.0

1

q (μm-1)

10

FIG. 3. (color online) (a) S(q) for index-matched colloidal suspen- sions, from ConDDM (closed symbols), 3D particle positions (open symbols), and the PY model (solid curves). Particle form-factor shown in grey dotted line. (inset) ˆx-ˆz image of the indexed-matched sample at φ=0.40 shows constant contrast 50 µm into the sample. (b) H(q) for the same suspensions, from ConDDM (open symbols), and a theoretical model (solid curves). (c) S(q) for an opaque, index- mismatched colloidal suspension at φ=0.25 (open squares). The PY prediction (solid curve) is in quantitative agreement with the data, while S(q) from 3D particle positions (dashed curve) is completely different. (inset) ˆx-ˆz image of the indexed-mismatched sample at φ=0.25 shows complete loss of contrast tens of µm into the sample.

symbols in Fig. 3(b). We compare our H(q) data with theo- retical predictions for hard spheres [9], marked with curves in Fig. 3(b), which are all in excellent agreement with our exper- imentaldata. PreviousH(q) estimates derived from lightscat- tering assume a theoretical P(q) [7]; by contrast, our purely- experimental technique makes no such assumptions. More- over, the quantitative agreement between experimental and theoretical S(q) and H(q) persists through the entire q-range, and will do so as long as ah≤δz (Supplementary Material); this agreement is especially striking at low-q, inaccessible to light scattering, and high-φ, not probed easily with FCS.

The confocal pinhole’s rejection of out-of-plane light per- mits observation deep in the bulk of ﬂuorescent samples, even when they scatter light; therefore, ConDDM might provide new capabilities to make these light-scattering-like measure- ments in dense samples that scatter light multiply, not possi- ble with DDM or traditional light scattering. To test this, we create a colloidal suspension with different solvents (1:3 do- decane:TCE) that closely matches the particles’ density, but with n=1.47 so strongly mismatches their refractiveindex that suspensionsat φ=0.25 are macroscopicallyopaque. Here, par- ticles near the coverslip can be resolved individually; those greater than 30 µm away are indistinguishable from the noise,

3

1.0

0.8

a

) t δ q g

(

0.6

0.4

0.2

0.0

0.8

b

0.3

c

) t δ q g

(

0.6

0.4

) 0 v / v ( P

0.2

0.1

0.2

0.0

0.01

qδt

0.0 0

0.1

2

4 v/v0

6

FIG. 4. (color online) (a) g(qδt) and ˆx-ˆy image (inset) for bacteria swimming at the coverslip, for 43 values of q in the range 0.2<q<4 µm−1, each plotted with different symbols, as a function of rescaled time delay qδt. (b) g(qδt)for bacteria swimming deep in the bulk, 16 µm from the coverslip, in the same q-range as in (a); here, data from all 43 values of q (symbols) scale onto a single master (solid black) curve of the form exp[−(qv0δt)1.35], with v0=39.6±0.3 m/s. (inset) ˆx-ˆy image of bacteria deep in the bulk, 8 µm from the coverslip. (c) Population velocity distribution P(v/v0) for the bacteria in (b).

as shown in the inset to Fig. 3(c). Using ConDDM, we mea- sure S(q) and H(q) 10 µm from the cover slip. Our measured S(q) is excellent; the PY prediction again conforms closely to the data, as shown with solid curves and symbols in Fig. 3(c). By contrast, particles deep in the sample cannot be resolved above the noise; therefore, S(q) from 3D particle positions fails completely, as shown with the dashed curve in Fig. 3(c). Probing deeply within multiply-scattering, dense samples could allow ConDDM to characterize systems that change too rapidly for traditional microscopy-based object tracking [6], and are too dense for DLS and DDM. We explore this ca- pability in swimming bacteria, which have been character- ized on the microscopic level with many techniques [10, 11] including DDM [6], but only in 2D or in dilute concentra- tions. To our knowledge, no study has investigated rapid dynamics of bacteria at higher density [11–13] free to swim in 3D, with sufﬁciently high resolution to resolve individual organisms. To investigate such behavior, we image dense, macroscopically-opaque suspensions of Bacillus subtilis, a ﬂagellated bacterium, collecting images of 256×128 pixels at 100.0 fps with the point-scanning confocal at various depths from the coverslip; we maintain the sample at 37◦C. Near the coverslip, we observe that bacteria move in a 2D plane, their long axes aligned parallel to the coverslip, shown in the inset to Fig. 4(a). Here, each calculated g(q,δt) is not exponential, as for diffusing particles, but has a different functional form for each value of q, as shown in Fig. 4(a); there is no universal scaling, and τ(q) does not follow a simple power law, but is instead a sigmoidal curve, shown with open circles in Fig. 2. By contrast, deeper within the bulk of the sample, the bac-

1

teria do not swim within a single plane, and their axes appear to be distributed randomly, shown in the inset to Fig. 4(b). We again ﬁnd that g(q,δt) is not simply exponential. How- ever, unlike the surface-constrained bacteria, those swimming in the bulk have dynamics that, surprisingly, can be scaled onto a single master curve, shown with the solid curve in these g(q,δt) follow a compressed exponential Fig. 4(b): form, g(q,δt)=exp[−(qv0δt)γ], where γ=1.35 for all depths greater than 4 µm from the coverslip; intriguingly, a similar exponent is observed in aging gels and glasses [14]. More- over, the resulting τb(q) conform closely to a power law with slope -1, shown with open quadrilaterals and dotted line in Fig. 2; this linearity demonstrates that bacteria in the bulk move ballistically over the distances we measure, and deﬁnes their characteristic speed, τb(q)∼(v0q)−1; our mea- sured v0=39.6±0.3 µm/s is consistent with previous measure- ments in dilute bacterial suspensions [15]. Moreover, we can extract the population’s swimming-speed distribution P(v) ∞ by inverting g(q,δt)=hexp[ı~q ·~vδt]i=R 0 vP(v)J0(qvδt)dv, where J0 is the zeroeth-order Bessel function, as shown in Fig. 4(c). By contrast, because τ(q) does not follow a linear power-law for the bacteria swimming near the coverslip, they cannot have a well-deﬁned velocity distribution, contrasting measurements in different bacteria [6]. While the particular numerical values depend on environmental conditions (tem- perature, nutrients), qualitative differences in scaling demon- strate a fundamentallynew measurementusing ConDDM,and its unique contribution to the study of microorganism motion.

We gratefully acknowledge R. Guerra, T. F. Kosar, D. Lue- bke, R. Prescott, P. Sims, V. Trappe, B. Calloway, and funding from NASA (NNX08AE09G), the NSF (DMR-1006546), the Harvard MRSEC (DMR-0820484) and NVIDIA.

[1] P. J. Lu et al, Opt. Express 15, 8702 (2007). [2] P. J. Lu et al., Nature 453, 499-504 (2008). [3] R. Borsali and R. Pecora, Soft matter: scattering, imaging and

manipulation (Springer, Berlin, 2008).

[4] R. Cerbino and V. Trappe, Phys. Rev. Lett. 100, 188102 (2008). [5] F. Giavazzi, D. Brogioli, V. Trappe, T. Bellini and R. Cerbino,

Phys. Rev. E 80, 031403 (2009).

[6] L. G. Wilson et al., Phys. Rev. Lett. 106, 018101 (2011). [7] P. N. Segre, O. P. Behrend and P. N. Pusey, Phys. Rev. E 52,

5070 (1995).

[8] A. Robert et al., Eur. Phys. J. E. 25, 77 (2008). [9] C. W. J. Beenaker and P. Mazur, Physica A 126, 349 (1984). [10] H. P. Zhang, A. Be’er, R. S. Smith, E. L. Florin and H. L. Swin-

ney, Europhys. Lett. 87, 48011 (2009)

[11] A. Sokolov, I. S. Aranson, J. O. Kessler and R. E. Goldstein,

Phys. Rev. Lett. 98, 158102 (2007).

[12] I. Tuval, L. Cisneros, C. Dombrowksi, C. W. Wolgemuth, J. O. Kessler and R. E. Goldstein, Proc. Acad. Nat. Sci. USA 102, 2277 (2005).

[13] A. Sokolov, R. E. Goldstein, F. I. Feldchtein, and I. S. Aranson,

Phys. Rev. E 80, 031903 (2009)

[14] L. Cipelletti et al., Farad. Discuss. 123, 237 (2003). [15] A. Zaritsky and R. M. Macnab, J. Bacteriol. 147, 1054-1062

4

(1981).

5