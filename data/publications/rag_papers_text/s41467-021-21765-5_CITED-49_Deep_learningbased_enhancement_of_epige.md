; , : ) ( 0 9 8 7 6 5 4 3 2 1

ARTICLE

https://doi.org/10.1038/s41467-021-21765-5

OPEN

Deep learning-based enhancement of epigenomics data with AtacWorks

1,3, Zachary D. Chiang2,3, Nikolai Yakovenko1, Fabiana M. Duarte

Avantika Lal Jason D. Buenrostro

2✉

2, Johnny Israeli1✉

ATAC-seq is a widely-applied assay used to measure genome-wide chromatin accessibility; however, its ability to detect active regulatory regions can depend on the depth of sequencing coverage and the signal-to-noise ratio. Here we introduce AtacWorks, a deep learning toolkit to denoise sequencing coverage and identify regulatory peaks at base-pair resolution from low cell count, low-coverage, or low-quality ATAC-seq data. Models trained by AtacWorks can detect peaks from cell types not seen in the training data, and are generalizable across diverse sample preparations and experimental platforms. We demonstrate that AtacWorks enhances the sensitivity of single-cell experiments by producing results on par with those of conventional methods using ~10 times as many cells, and further show that this framework can be adapted to enable cross-modality inference of protein-DNA interactions. Finally, we establish that AtacWorks can enable new biological discoveries by identifying active reg- ulatory regions associated with lineage priming in rare subpopulations of hematopoietic stem cells.

1NVIDIA Corporation, Santa Clara, CA, USA. 2Department of Stem Cell and Regenerative Biology, Harvard University, Cambridge, MA, USA. 3These authors contributed equally: Avantika Lal, Zachary D. Chiang.

✉

email: jisraeli@nvidia.com; jason_buenrostro@harvard.edu

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

&

1

ARTICLE

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

Within a single cell, the eukaryotic genome is hier-

archically organized to form a gradient of chromatin accessibility ranging from compact, repressive hetero- chromatin to nucleosome-free regions associated with increased gene expression. Assay for Transposase-Accessible Chromatin using Sequencing (ATAC-seq) leverages the Tn5 transposase to directly measure chromatin accessibility as a proxy for the relative activity of DNA regulatory regions across the genome1. ATAC-seq has been applied to identify the effects of transcription factors on chromatin, construct cellular regulatory networks, and localize epigenetic changes underlying diverse development and disease- associated transitions2–4. Recently, the development of single-cell ATAC-seq methods have made it possible to measure accessible chromatin in individual cells, enabling epigenomic analysis of rare cell types within heterogeneous tissues5.

The ability to measure biologically-meaningful changes in accessible chromatin using ATAC-seq depends on both the signal-to-noise ratio and the depth of sequencing coverage. Technical parameters such as the overall quality of cells or tissues, the nuclei extraction method6, or over-digestion of chromatin can result in attenuated measurements of accessibility. Importantly, these issues are exacerbated in single-cell experiments, where primary tissues may vary in quality and key cell types may be exceedingly rare.

Deep learning represents a potential tool to address these limitations, as it has been successfully used for problems such as denoising speech7 and image restoration8,9. An earlier study demonstrated that simple convolutional neural networks can be used to denoise and call peaks from ChIP-seq data, but was optimized for broad peak calling of histone modiﬁcations10. Another recent study applied deep learning to predict chromatin accessibility in a rare pancreatic islet cell type11, highlighting the need for a robust and generalizable method for the analysis of sparse ATAC-seq data.

(predicting the genomic location of accessible regulatory ele- ments). Once this mapping is learned, it is saved as a model that can be applied to denoise and call peaks from similar low- coverage or low-quality datasets at any given region in the genome.

The network makes predictions for each base in the genome based on coverage values from a surrounding region spanning several kilobases (6kb for the models presented here), but does not consider the DNA sequence itself, allowing it to generalize across cell types. AtacWorks uses the ResNet (residual neural network) architecture, which has been applied extensively for natural image classiﬁcation and localization13. Our architecture consists of multiple stacked residual blocks, each composed of three convolu- tional layers and a skip connection that bypasses intermediate layers (Fig. 1a). These skip connections allow propagation of the input through the layers of the network to avoid vanishing gradients13, enabling deeper and more accurate models to be trained. The model is trained using a multi-part loss function combining Mean Squared Error (MSE), 1 - Pearson Correlation, and Binary Cross-Entropy (BCE) losses (see Methods).

We used AtacWorks to train deep learning models with bulk ATAC-seq data from FACS-isolated human blood-derived cell types2. To do this, we obtained ATAC-seq datasets from four cell types (B cells, natural killer (NK) cells, CD4+ and CD8+ T cells) and sampled each to a depth of 50 million reads (25 million read pairs) to produce standardized clean (high-coverage) data. Peaks for each clean dataset were identiﬁed using MACS214 (see Methods) which is the standard peak caller for ATAC-seq data, despite not being developed speciﬁcally for that purpose. We then subsampled each clean dataset to multiple lower sequencing depths ranging from 0.2 million to 20 million reads (Supplementary Fig. 1). For each depth, we trained a model to take as input the low-coverage ATAC-seq signal and reconstruct both the clean ATAC-seq signal and peak calls.

(https://github.com/clara- parabricks/AtacWorks)12, a deep learning-based toolkit that takes as input a low-coverage or low-quality ATAC-seq signal, and denoises it to produce a higher-resolution or higher-quality signal. AtacWorks trains a model to accurately predict both chromatin accessibility at base-pair resolution (a coverage track), and the genomic locations of accessible regulatory regions (peak calls). We apply AtacWorks to subsampled low-coverage bulk ATAC-seq and show that AtacWorks improves the resolution of the chromatin accessibility signal and the identiﬁcation of reg- ulatory elements. Further, AtacWorks is able to denoise signal from cell types not present in the training set, demonstrating that our deep learning models learn generalizable features of chro- matin accessibility. We use the same framework to denoise aggregated single-cell ATAC-seq from a small number of cells, and also to improve the signal-to-noise ratio in an ATAC-seq dataset with low signal-to-noise. We further show that Atac- Works can be adapted for cross-modality prediction of tran- scription factor footprints and ChIP-seq peaks from low-input ATAC-seq. Finally, we apply AtacWorks to single-cell ATAC-seq of hematopoietic stem cells (HSCs) to identify regulatory ele- ments associated with rare lineage-primed subpopulations.

Here, we introduce AtacWorks

Results A deep learning framework for denoising low-coverage data. AtacWorks trains a deep neural network to learn a mapping between noisy, low-coverage or low-quality ATAC-seq data and matching high-coverage or high-quality ATAC-seq data from the same cell type. Given a noisy ATAC-seq signal track as input, a trained model performs two tasks: denoising at base-pair reso- lution (predicting an improved signal track) and peak calling

To assess the generalizability of our method, we tested the performance of these models on ATAC-seq data from erythro- blasts2, which were not included in the training set. We ﬁrst subsampled reads from erythroblasts to the same depths as the training data. For each sequencing depth, we then applied the trained model to the corresponding subsampled dataset to obtain a predicted high-coverage signal track and peak calls (Fig. 1b). By examining the resulting denoised tracks, we conﬁrmed that AtacWorks that were not present in the training data, including a region adjacent to erythroblast marker gene GYPA2 (Fig. 1c). This suggests that our models are learning generalizable features of chromatin accessi- bility rather than cell-type speciﬁc patterns.

identiﬁes cell-type-speciﬁc peaks

To quantitatively evaluate the denoised high-coverage signal tracks produced by AtacWorks, we compared them to a clean (50 million read) erythroblast signal. At all sequencing depths, the Pearson correlation, Spearman correlation, and MSE between the denoised and clean signal tracks were substantially greater than that between the noisy and clean signal, both within and outside accessible chromatin peaks (Fig. 1d, Supplementary Table 1, Supplementary Fig. 2). We further found that our method outperforms smoothing using linear regression based on these metrics (Supplementary Table 2). Next, we evaluated the peaks identiﬁed by AtacWorks from each sequencing depth, and found that both the Area Under the Precision-Recall Curve (AUPRC) and Area Under the Receiver-Operator Characteristic (AUROC) of peaks were superior to MACS2 called peaks from the same subsampled data (Fig. 1e, Supplementary Table 1, Supplementary Fig. 2). For this analysis, AtacWorks produced output data of quality equivalent to (on average) 2.6× the number of reads in the input data based on Pearson correlation, and 4.2× based on AUPRC (Supplementary Table 1).

2

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

ARTICLE

a

d

Input Noisy ATAC-seq signal

Deep Learning Model

Pearson Correlation with clean (50M read) data

1

k c o B

l

l

a u d s e R

i

Residual Block

2

k c o B

l

a u d s e R

i

3

k c o B

l

l

a u d s e R

i

4

k c o B

l

l

a u d s e R

i

5

k c o B

l

a u d s e R

i

Output 1: Denoised signal

6

k c o B

l

a u d s e R

i

7

k c o B

l

l

a u d s e R

i

Output 2: Peak calls

n o i t a e r r o C n o s r a e P

l

1.00

0.75

0.50

0.25

Subsampled

Subsampled+ AtacWorks

Subsampled (Chr10) Subsampled+ AtacWorks (Chr10)

Skip connection

Input

+

Output

1-D Convolution

ReLU Activation

Evaluation Pearson Correlation MSE

Evaluation AUROC AUPRC

0.00

0 5 10 15 20 Sequencing Depth (Millions of Reads)

b

A e p m a S

l

Randomly subsample reads

e

0.8

AUPRC of peak calls

Clean signal + peak calls (50 million reads)

Training

Noisy signal (0.2-20 million reads)

0.6

MACS2

AtacWorks

AtacWorks Model

C R P U A

0.4

0.2

MACS2 (Chr10) AtacWorks (Chr10)

B e p m a S

l

AtacWorks denoised signal + peak calls

Inference

Noisy signal from unseen cell type

0.0

0 5 10 15 20 Sequencing Depth (Millions of Reads)

c

chr4:145,021,501 - 145,098,191

B

181 181

246

t

e S g n n a r T

i

i

CD4

CD8

NK

0 0 181 181

0 0 181 181

0 0 181 181

0

3.0

0.0 239

0

0 0 181 181

Erythro (50M)

0 0 2.0 2

Erythro (0.2M)

Erythro (0.2M) + AtacWorks

0 0.0 181 181

0 0

To show that the models are not simply learning features speciﬁc to the training set, we calculated performance metrics on chromosome 10, which was previously held-out from training, and obtained highly similar results to those computed on the whole genome (Figs. 1d and 1e, Supplementary Table 1). We also evaluated model performance speciﬁcally on differential peaks present in only either the training or test set, and found that

AtacWorks improves both the signal track accuracy and peak calling in these regions (Supplementary Table 1). Further, we found that the results were highly robust to different subsets of the training data used (Supplementary Table 3).

Since ATAC-seq is commonly applied to tissues containing a mixture of cell types, we sought to test whether our models could be applied to data of this nature. We found that a model trained

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

3

ARTICLE

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

Fig. 1 A deep learning approach to denoise ATAC-seq data. a Schematic of the ResNet architecture. The zoomed-in region displays a residual block composed of 1-dimensional convolutional layers (green squares), nonlinear ReLU activation functions (purple squares), and a skip connection. b Schematic showing how to train and validate AtacWorks on subsampled bulk ATAC-seq data. Clean high-coverage bulk ATAC-seq data is subsampled to create noisy data. Matched pairs of clean and noisy data are used to train AtacWorks models, which are then applied to denoise and call peaks from subsampled noisy data derived from a different cell type. c ATAC-seq signal tracks near the erythroblast marker gene GYPA, for four cell types used to train an AtacWorks model (gray), high-coverage erythroblast data (50 million reads; black), and erythroblast data subsampled to 0.2 million reads before (blue) and after (green) denoising with AtacWorks. Red bars below the zoomed-in tracks show peak calls by MACS2 (for the 50 M and 0.2 M read tracks) and AtacWorks (for the denoised track). d Pearson correlation between a clean ATAC-seq signal track (50 million reads) and subsampled data for erythroblasts, before (blue) and after (green) denoising with AtacWorks. Solid lines show correlation over the genome; dotted lines show correlation over chromosome 10. e AUPRC for MACS2 (blue) and AtacWorks (green) showing their peak calling performance on subsampled data, using peaks called by MACS2 subcommands on the clean (50 million reads) signal track as ground truth. Solid lines show AUPRC over the genome; dotted lines show AUPRC over chromosome 10. AUPRC: Area Under the Precision-Recall Curve. AUROC: Area Under the Receiver Operating Characteristic. MSE: Mean Squared Error. ReLU: Rectiﬁed Linear Unit. Source data are provided as a Source Data ﬁle.

on FACS-isolated cell types from human blood was able to denoise subsampled low-coverage ATAC-seq data from a mixture of human cell types derived from the intestinal Peyer’s Patch by the ENCODE consortium15,16 (Supplementary Fig. 3, Supple- mentary Table 4). This suggests that our models are robust to data from mixtures of cell types, as well as varied experimental preparation of cells and tissues. However, we note that a model trained on three different ENCODE datasets produces better results on this task (Supplementary Table 4), suggesting that results may be improved when the training and test data are obtained from the same experimental protocol.

datasets. The resulting trained models improved signal track accuracy and peak calling from aggregated NK cells sequenced using the same protocol (Fig. 2b, Supplementary Table 8, Sup- plementary Table 9). Notably, AtacWorks improved the AUPRC of peak calls from 50 NK cells from 0.2048 to 0.7008, a result that MACS2 requires over 400 cells to obtain (Fig. 2b, Supplementary Table 8). Though we observed improved signal quality and peak calls for any number of cells, the results on 1 and 5 cell samples may be too noisy for downstream biological analysis, possibly due to single-cell heterogeneity not captured by the aggregate data used for training.

Another present challenge in adapting ATAC-seq to novel biological contexts is developing experimental protocols that optimize enrichment of open chromatin. To help address this issue, we applied AtacWorks to improve signal quality in ATAC- seq datasets with low signal-to-noise ratio. We trained a model to learn a mapping between paired high and low-quality ATAC-seq datasets from FACS-isolated human monocytes2 (Supplementary Table 5, Methods). Both datasets had similar sequencing depth (~20 million reads); however, one had a higher signal-to-noise ratio estimated using the global enrichment of signal surrounding transcription start sites (TSSs). We then applied this trained model to denoise low-quality bulk ATAC-seq data of similar depth from erythroid cells. AtacWorks improved the enrichment at TSSs (Supplementary Fig. 4a), producing a signal track and peak calls more similar to those obtained from higher-quality data (Supplementary Fig. 4b, Supplementary Table 6).

Finally, we compared our method to a recent study11 that also reported the use of a deep learning model that could perform either ATAC-seq denoising or peak calling. We implemented the U-Net model architecture reported in this study, and found that the ResNet architecture used in AtacWorks outperforms this model in denoising, peak calling, and runtime (Supplementary Note 1, Supplementary Table 7).

AtacWorks enhances single-cell data from low numbers of cells. To demonstrate our method is also adaptable to broad use cases of ATAC-seq, we applied AtacWorks to denoise data from a high-throughput single-cell ATAC-seq experiment. We ﬁrst obtained droplet single-cell ATAC-seq (dscATAC-seq) data from bead-isolated human blood cells and aggregated single-cell chromatin accessibility proﬁles by cell type17. We selected two cell types (B cells and monocytes) from the dataset, and produced clean ATAC-seq signal tracks and peak calls by aggregating data over 2400 cells (~50 million reads) of each type. We then gen- erated noisy ATAC-seq signals by randomly subsampling subsets of cells of each type, and trained AtacWorks models on the paired clean and noisy datasets (Fig. 2a). We randomly sampled 1 cell (~20,000 reads), 5 cells (~0.1 million reads), 10 cells (~0.2 million reads) or 50 cells (~1 million reads) for the low-coverage training

We then tested whether these models trained on dscATAC data from human blood could generalize to less-similar cell types. To do this, we obtained single-cell data from a mouse brain using the same dscATAC protocol17. We then applied the models trained on human blood to data aggregated from mouse pyramidal and oscillatory neurons. For both types of neurons, we observed that AtacWorks improved the signal track and peak calls, both overall and within cell-type speciﬁc peaks (Fig. 2c, d, Supplementary Data 1). This result demonstrates that AtacWorks is broadly applicable across both cell types and species.

Finally, because the previous experiment was limited to dscATAC data, we sought to investigate the generalizability of AtacWorks models to data from different single-cell platforms. To this end, we applied one of the previously-described AtacWorks models trained on dscATAC-seq data to human CD4+ T cells sequenced using a combinatorial indexing approach (dsciATAC-seq17), and observed improvements in both the signal track and peak calls (Supplementary Table 10). We also applied a similar model trained on dscATAC-seq data from human blood to macrophages from mouse primary lung tumors sequenced using the sciATAC-seq protocol18. Once again, we observed that the model trained on human dscATAC-seq data improved both signal track accuracy and peak calls (Supplementary Table 11). However, we note that a model trained on sciATAC-seq data from B cells and monocytes returned slightly better results on most metrics when applied to the same sciATAC-seq dataset from macrophages (Supplementary Table 11). Collectively, these results support AtacWorks as a highly generalizable tool to study single-cell ATAC-seq data.

AtacWorks enables cross-modality predictions. Seeing that AtacWorks accurately predicts denoised coverage at base-pair for transcription factor to extend it resolution, we sought footprinting1,19. Footprinting leverages the fact that transcription factors vary in how they bind to DNA, which allows binding events to be identiﬁed via a characteristic Tn5 insertion signature. footprinting requires over 100 million reads19, Traditionally, prohibiting its widespread use. To test the feasibility of performing footprinting from low-input ATAC-seq, we obtained high-

4

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

ARTICLE

a

Single-cell experiment

Abundant cell type

b

AUPRC of peak calls

0.6

MACS2

Rare cell type

Clean signal + peak calls

All cells

Training

Random subset of cells

Noisy signal

AtacWorks

0.4

2 S C A M + s

C R P U A

2 S C A M + s

l l

0.2

e c 0 8 1

l l

e c 0 0 1

0 2

0.0 Cells 1 5 10 50 Reads 0.02 0.1 0.2 1 (Millions)

2 S C A M + s

l l

e c 0 0 4

AtacWorks Model

c

0.6

MACS2

d

AtacWorks denoised signal + peak calls

Inference

Noisy signal

Rare cell type from the same or other experiment

AtacWorks

C R P U A

0.4

0.2

2 S C A M + s

2 S C A M + s

l l

e c

l l

e c

0 8

0 7

0.0 Cells 4 8 40 0.1 0.2 1

Reads (Millions)

2 S C A M + s

l l

e c 0 0 2

chr10: 25,265,981 - 25,302,183

Akap7

Gm25016

Akap7

Gm26167

Gm40617

Pyramidal neurons (1800 cells, ~40M reads)

248 248

0 0

Pyramidal neurons (40 cells, ~1M reads)

4.5 4.5

0.0 0

Pyramidal neurons (40 cells + AtacWorks)

193 193

0 0

Fig. 2 AtacWorks enhances single-cell data from low numbers of cells. a Schematic showing the strategy to train and test AtacWorks on single-cell ATAC-seq data. A clean high-coverage ATAC-seq signal is obtained by aggregating data from all cells belonging to an abundant cell type. Data are aggregated over a randomly selected subset of these cells to obtain a noisy signal. Paired clean and noisy datasets are used to train an AtacWorks model. The model can be applied to denoise and call peaks from noisy aggregate data from small numbers of cells, either from the same experiment or a different experiment. b AUPRC of peak calls on aggregate single-cell ATAC-seq data from human natural killer (NK) cells. Peak calls were produced by MACS2 (blue) and AtacWorks (green) on noisy data aggregated over 1–50 cells. Gray bars show AUPRC of MACS2 on larger numbers of cells, to illustrate how many cells MACS2 requires to reach the same performance as AtacWorks. c AUPRC of peak calls on aggregate single-cell ATAC-seq data from mouse pyramidal neurons. Peak calls were produced by MACS2 (blue) and AtacWorks (green) on noisy data aggregated over 4, 8 or 40 cells. Gray bars show AUPRC of MACS2 on larger numbers of cells, to illustrate how many cells MACS2 requires to reach the same performance as AtacWorks. d ATAC-seq signal tracks near the Akap7 gene, for single-cell mouse pyramidal neuron data (~40 million reads from 1800 cells; black), and neuron data subsampled to 40 cells (~1 million reads), before (blue) and after (green) denoising with AtacWorks. Red bars show peak calls by MACS2 (for the 1800 cell and 40 cell tracks) and AtacWorks (for the denoised track). AUPRC: Area Under the Precision-Recall Curve. Source data are provided as a Source Data ﬁle.

coverage (100 million reads) ATAC-seq data from FACS-sorted human blood cell types (multipotent progenitor cells, CD8+ T cells, NK cells)2 and reduced track smoothing to preserve transcription factor-speciﬁc patterns of Tn5 insertions (see Methods). We then downsampled these tracks to lower sequen- cing depths and trained a model for each depth, which we tested on data from similarly-processed HSCs. We evaluated the per- formance of these models on a set of 200 bp genomic regions spanning binding motifs for genome architectural protein CTCF. At all sequencing depths, AtacWorks improved the signal track spanning CTCF motifs in HSCs (Supplementary Table 12),

enhancing the characteristic footprint of CTCF binding (Supple- mentary Fig. 5).

Encouraged by these results, we reasoned we may adapt our method to directly predict ChIP-seq peaks from low-input ATAC-seq. Like footprinting, standard ChIP-seq protocols also require large quantities of input material (at least 107 cells), though this number has been reduced in certain contexts by recent technological developments20. To demonstrate the feasi- bility of cross-modality prediction, we trained AtacWorks models to learn a mapping from low-coverage aggregate dscATAC-seq signal to CTCF and H3K27ac (an active histone mark) ChIP-seq

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

5

ARTICLE

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

signal and peak calls in the same cell type. For the prediction of CTCF ChIP-seq, we also supplied the model with the positions of the genome (see CTCF binding motifs on both strands of Methods). We trained models on noisy aggregate dscATAC-seq data from small numbers of B cells, and tested them on similarly- processed monocytes. For small numbers of cells ranging from 10 to 500, AtacWorks predicted CTCF and H3K27ac peak calls with surprisingly high concordance to ChIP-seq data from the same cell type (AUROC > 0.9 from 500 cells; Supplementary Fig. 6, Supplementary Data 2).

samples of 50 similar HSCs each, representing putative populations of long-term, lymphoid and erythroid-primed HSCs (Fig. 3b). For each sample of 50 aggregated cells, we performed signal denoising using AtacWorks and visualized the denoised chromatin accessi- bility proﬁles near genes suggested to be indicators of lineage priming24,29 (Fig. 3f). We observed considerable differences between the denoised tracks that could not be readily distinguished from the original low-coverage signal (Supplementary Fig. 7), including potential regulatory elements seemingly present in the lymphoid, but not the erythroid-primed cells (near MEF2C, POU2F2) and vice-versa (near GATA1, GATA2).

These cross-modality predictions demonstrate the potential for AtacWorks to generate multiple layers of information in single cells from one of the most commonly-used epigenomic assays, at no additional cost. It is generally experimentally challenging to make multiple measurements from the same cells, so this approach may be especially useful in cases where running infeasible due to time, multiple ChIP-seq experiments reagents, sample availability, or biological variability. Though the models presented here tend to perform better on active histone marks (e.g., H3K27ac) or abundant architectural proteins (e.g., CTCF), for distinguishing active vs. poised enhancers21 or characterizing changes in 3D genome structure across differentiation22. We anticipate future work will extend these capabilities to enable cross-modality inference of additional latent epigenetic states from a single experiment.

is

these speciﬁc predictions may be useful

AtacWorks enhances the resolution of single-cell studies. Empowered by the improved resolution afforded by AtacWorks, we sought to investigate epigenetic changes underlying differ- entiation in rare cell subpopulations that cannot be experimen- tally isolated, and thus cannot be analyzed using traditional approaches. Previous single-cell studies of FACS-isolated bone marrow mononuclear cells (BMMCs) have observed epigenetic heterogeneity within immunophenotypically-deﬁned cellular populations, suggesting that hematopoietic stem and progenitor cells lie along a continuum of differentiation states (Fig. 3a)23,24. In particular, HSCs are thought to include rare subpopulations of cells that are primed toward either the lymphoid or erythroid lineage23,25,26. Though single-cell ATAC-seq enables measure- ments of chromatin accessibility over aggregate genomic features, such as sets of transcription factor motifs27 or the regions sur- rounding TSSs27,28, with such granular lineage-primed states, there is typically not enough sequencing coverage to identify which speciﬁc regulatory regions are associated with each dif- ferentiation trajectory.

We reasoned we could use AtacWorks to identify sets of regulatory regions that are unique to lymphoid or erythroid- primed HSCs. First, we performed dscATAC-seq17 on FACS- isolated HSCs to generate 9974 single-cell chromatin accessibility proﬁles (see Methods). To deﬁne lymphoid and erythroid differentiation trajectories, we collected published dscATAC-seq data from bead-enriched CD34+ cells and used a bulk reference- guided approach (see Methods) to project all single-cell proﬁles into a shared latent space, visualized using UMAP for dimensionality reduction (Fig. 3b, c). This analysis localized FACS-isolated HSCs to a region at the top of the projection. We then conﬁrmed that HSCs localized in this region exhibited directional signal bias in transcription factor motif accessibility scores for the GATA2 motif (Fig. 3d) and smoothed gene accessibility scores for MEF2C (Fig. 3e), genes which have been implicated as markers of erythroid and lymphoid lineage priming respectively24,29 (see Methods).

To assess the signiﬁcance of these chromatin accessibility differences, we took 1000 random samples of 50 similar HSCs each and calculated a normalized mean and standard deviation of the coverage from the 1000 denoised tracks, allowing us to estimate z-scores for each regulatory region we observed in our (see denoised long-term HSC and lineage-primed samples Methods). We identiﬁed a total of 8590 signiﬁcant regulatory regions surrounding genes associated with differential expression in CD34+ cells (Supplementary Data 3). To validate that these identiﬁed regulatory elements are associated with lineage- priming, we conﬁrmed that the lymphoid-primed elements were more accessible in the CD34+ cells from lymphoid lineage (Supplementary Fig. 8a), while the erythroid-primed elements were more accessible in CD34+ cells from the erythroid lineage (Supplementary Fig. 8b). We also observed that the most differentially-accessible sequence motifs in these subsets of peaks included transcription factors crucial to differentiation, including E2F30 and MYB families31 (Supplementary Table 13). Altogether, these results demonstrate the unique capacity of deep learning to enhance the resolution of sparse single-cell ATAC-seq studies.

Discussion ATAC-seq has become a widely adopted tool for high-resolution characterization of the epigenome, providing insights into the mechanisms underlying gene expression changes associated with development, evolution, and disease. However, technical limita- tions in tissue quality, assay performance, and sequencing cov- erage constrain our ability to measure the full spectrum of chromatin states across the genome. These limitations also per- tain to emerging single-cell ATAC-seq technologies, as cell types of interest are often difﬁcult to experimentally isolate, and are present at low frequencies in heterogeneous contexts.

Here we present AtacWorks, an easy-to-use and generalizable toolkit to train and apply deep learning models to ATAC-seq data. Unlike previous deep learning methods for epigenomics, AtacWorks denoises ATAC-seq signal at base-pair resolution and simultaneously predicts the genomic location of accessible regulatory elements. The models we present here outperform existing approaches at both of these tasks, and moreover, are robust across cell and tissue types, individuals, and experimental protocols. AtacWorks is not provided with the DNA sequence as an input, which means it is agnostic to cell- or condition- speciﬁc correlations between chromatin accessi- bility and sequence motifs. Instead, the model learns features based on the shape of the coverage track, which generalize across datasets. In addition to generalization across different cell types, we also observed that our trained models can generalize to data from dif- ferent species, experimental platforms, and quality levels. However, we observed that we could obtain slightly better results (e.g., AUPRC increase from 0.7332 to 0.7483) on a test dataset by using a model trained on more closely matched data (Supplementary Table 11), suggesting that there remain small beneﬁts to matching training and test data when possible.

To generate high-resolution chromatin accessibility tracks of lineage-primed cells using our model, we selected three distant

We also demonstrate that AtacWorks can be adapted for cross- modality prediction of transcription factor footprints and ChIP-

6

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

ARTICLE

a

c

d

GATA2 motif accessibility

HSC

z−score 2

n o i t a i t n e r e f f i

D

s C P S H

+ 4 3 D C

LMPP

MPP

CMP

20

Nearest cell type

Isolated HSC

HSC

2 P A M U

15

10

0

−2

CLP

pDC

GMP

MEP

10

MPP

5

b

B, T NK cells

Peripheral pDC

Monocyte, mDC Granulocytes

Ery, Mega

FACS-isolated HSCs (9,974 cells)

2 P A M U

0

LMPP

CMP

CLP

e

0

0

10

UMAP1

MEF2C gene accessibility

15

long-term HSCs

pDC

gene score

15

lymphoid-primed

erythroid-primed

−10

GMP

15

0.03

0.02

2 P A M U

10

−20

Monocyte

MEP

2 P A M U

10

0.01

5

f

0

5

UMAP1

10

15

−20

−10

0 UMAP1

10

20

0

0

5

UMAP1

10

15

ACTB

CD34

PROCR

MEF2C

POU2F2

GATA1

GATA2

FACS-isolated HSCs (9,974 cells)

Denoised long-term HSCs (50 cells)

Denoised lymphoid-primed HSCs (50 cells)

Denoised erythroid-primed HSCs (50 cells)

ACTB

CD34

PROCR

EF2C MEF2C

MEF2C-A

POU2F2

GATA1

GATA2

GATA2-AS1

Fig. 3 AtacWorks identiﬁes differentially-accessible regulatory regions associated with lineage-primed hematopoietic stem cells. a A schematic of the classical hierarchy of human hematopoietic differentiation. b A UMAP dimensionality reduction of single-cell ATAC-seq proﬁles from 9974 FACS-isolated hematopoietic stem cells (HSCs). The colored points represent three 50-cell subsamples, each generated by selecting a single cell and identifying its nearest neighbors in principal component space. c A combined UMAP dimensionality reduction of single-cell ATAC-seq proﬁles from HSCs shown in (b) and 28,505 published bead-enriched CD34+ bone marrow progenitor cells17. The bead-enriched CD34+ cells are colored by the most correlated cell type from a FACS-isolated single-cell ATAC-seq reference24. The box indicates the region containing FACS-isolated HSCs shown in (b), (d) and (e). d FACS- isolated HSCs colored by chromVAR transcription factor motif accessibility z-scores for GATA2. These scores represent enrichment or depletion of chromatin accessibility within peaks that contain the GATA2 motif (see Methods). e FACS-isolated HSCs colored by smoothed gene accessibility scores for MEF2C. These scores are a weighted sum of read counts within 10 kb of the MEF2C transcription start site, averaged over each cell’s 50 nearest neighbors (see Methods). f Aggregate chromatin accessibility signal tracks surrounding genes implicated as markers of lineage priming24,29 for all 9974 FACS-isolated HSCs and the three denoised 50-cell subsamples of HSCs shown in (b). The arrows denote select regulatory regions with signiﬁcant differences in chromatin accessibility relative to a random background. HSC: hematopoietic stem cell. MPP: Multipotent progenitor. LMPP: lymphoid- primed multipotent progenitor. CMP: common myeloid progenitor. CLP: common lymphoid progenitor. pDC: plasmacytoid dendritic cell. GMP: granulocyte-macrophage progenitor. MEP: megakaryocyte-erythroid progenitor. Source data are provided as a Source Data ﬁle.

seq peaks from low-input ATAC-seq. As such, we anticipate this framework may be broadly useful for other deep learning appli- cations in genomics, such as DNase, MNase, ChIP-seq, and the recently-developed method CUT&RUN20, which has comparable high-throughput single-cell adaptations32,33

reads in a read pair were retained (e.g., 100,000 read pairs were selected to obtain a total of 200,000 sequencing reads). For CTCF footprinting experiments, down- sampling was repeated independently ﬁve times to produce ﬁve times the amount of training data. This was done to ensure that the model received enough training data, as only a small fraction of the genome was used for training in these experiments.

Finally, the robustness and speed of AtacWorks enable its application to high-throughput single-cell ATAC-seq datasets of heterogeneous tissues. We show that our method can be used on small subsets of rare lineage-priming cells to denoise signal and identify accessible regulatory regions at previously-unattainable genomic resolution. Based on these advancements, we anticipate that AtacWorks will broadly enhance the utility of epigenomic assays, providing a powerful platform to investigate the regulatory circuits that underlie cellular heterogeneity.

Methods Data preprocessing. BAM ﬁles for bulk ATAC-seq were downsampled to a ﬁxed number of reads using SAMtools v.1.934. For paired-end sequencing data, both

For single-cell ATAC-seq experiments, a number of cells of the chosen cell type were randomly selected and all reads from those cells were extracted from the BAM ﬁle via cell barcodes. This random sampling of cells was repeated independently ﬁve times due to the sparsity of the input single-cell ATAC-seq data.

To identify the exact location of Tn5 insertions with base-pair resolution, each ATAC-seq read was converted to a single genomic position corresponding to the ﬁrst base pair of the read. Previous work has demonstrated that the Tn5 transposase inserts adapters separated by 9 bp, so reads aligning to the + strand were offset by +4 bp, while reads aligning to the - strand were offset by −5 bp1. Each cut site location was extended by 100 bp in either direction, except for transcription factor footprinting experiments where each cut site was extended by 5 bp in either direction. The bedtools genomecov function (v2.26.0)35 was then used to convert the list of locations into a genome coverage track containing the ATAC-seq signal at each genomic position.

To call peaks from clean and noisy signal tracks, MACS2 (v2.2.7) subcommands bdgcmp and bdgpeakcall were run with the ppois parameter and a -log10(p value)

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

7

ARTICLE

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

cutoff of 3. BED ﬁles with equal coverage over all chromosomes were provided as a control input track.

Input data for AtacWorks. Deep learning models were trained using one or more pairs of matching ATAC-seq datasets. Each pair consisted of two ATAC-seq datasets from the same sample or cell type: a clean dataset of high sequencing coverage or quality, and a noisy dataset of lower coverage or quality. Unless indicated otherwise, low-coverage datasets were generated computationally by randomly subsampling a fraction of reads or cells from the high-coverage dataset.

Model evaluation in AtacWorks. The performance of the model in regression was measured by computing Pearson correlation, Spearman correlation and MSE of the denoised data with respect to the clean dataset. For classiﬁcation (peak calling), the model outputs the probability of belonging to a peak, for each position in the genome. In order to obtain predicted peaks, there is a set probability threshold above which a base is said to be a peak. Similarly, MACS2 produces a p value for each position and the ﬁnal peak calls depend on a user-deﬁned probability threshold. Therefore the AUPRC and Area under the Receiver Operating Char- acteristic (AUROC) metrics were used to evaluate classiﬁcation performance over the entire range of possible thresholds.

Models were given three inputs for each such pair of datasets:

1. a signal track representing the number of sequencing reads mapped to each position on the genome in the noisy dataset.

2. a signal track representing the number of sequencing reads mapped to each

Peak calling. In order to call peaks from the base pair-resolution probabilities produced by AtacWorks, the macs2 bdgpeakcall command from MACS2 (v2.2.7)14 was run with a threshold of 0.5. This is the same procedure used by MACS2 to call peaks from base pair-resolution p values.

position on the genome in the clean dataset. 3. the genomic positions of peaks called by MACS2 on the clean dataset. Models learned a mapping from (1) to both (2) and (3); in other words, from the noisy signal track, they learned to predict both the clean signal track, and the positions of peaks in the clean dataset.

Input ATAC-seq datasets were divided into training, validation and holdout sets. The validation set consisted of data for chromosome 20 (for human data) or chromosome 11 (for mouse data), while the holdout set consisted of data for chromosome 10. Datasets for all other autosomes were included in the training set. These datasets were then further divided into non-overlapping intervals of 50 kb, unless otherwise speciﬁed (Supplementary Table 14), each representing a single training example. Each 50 kb long interval was padded with an additional 5 kb at either end, unless otherwise speciﬁed (Supplementary Table 14) so that the convolutional ﬁlter had enough neighboring bases to make predictions for every base inside the interval. Balanced training datasets with a ﬁxed proportion of peaks were tested; however, this feature did not improve the overall performance metrics and was therefore not employed in genome-wide experiments.

ResNet architecture used in AtacWorks. The PyTorch neural network frame- work36 was used to train a ResNet (residual neural network) model consisting of multiple stacked residual blocks. Each residual block included three convolutional layers and a skip layer to add the input to the ﬁrst layer to the output of the third layer (Fig. 1a). Unless speciﬁed otherwise (Supplementary Table 14), each con- volutional layer used 15 convolutional ﬁlters with a kernel size of 51 and a dilation of 8. Dilated convolutional layers were used to increase the receptive ﬁeld of the model without increasing the parameter count. This approach has been effective in image classiﬁcation tasks where a larger receptive ﬁeld is desirable37. Models did not utilize batch normalization38 for the convolutional layers, as it did not improve accuracy on either the regression or classiﬁcation tasks in our experiments.

For each position in the given interval, the model performed two tasks; a regression or denoising task (predicting the ATAC-seq signal at each position) and a classiﬁcation or peak calling task (predicting the likelihood that each position is part of a peak).

Running AtacWorks. AtacWorks v0.3.0 was used for all experiments.

All the parameters describing the models used in this paper are given in Supplementary Table 14. These parameters were chosen in a grid search based on validation set performance. Deeper and larger models produced slightly better results; however, larger models were also expensive and time-consuming to train. AtacWorks took 2.7 min per epoch to train on one ATAC-seq dataset, and 22 min to test on a different whole genome, using 8 Tesla V100 16GB GPUs in an NVIDIA DGX-1 server.

Paired high and low-quality ATAC-seq tracks. Paired high and low-quality chromatin accessibility tracks were computationally generated from the same experiment in order to minimize the impact of potential batch effects. Published bulk ATAC-seq tracks from monocytes and erythroblasts2 were split by technical and biological replicate, and then quantiﬁed using a TSS enrichment score. Tracks were then visually classiﬁed as high or low enrichment, and then aggregated based on classiﬁcation and cell type to form the paired high and low-quality tracks (Supplementary Table 5). The original study describing these datasets found that ATAC-seq proﬁles were highly reproducible across both technical and biological replicates (mean Pearson r = 0.94 and r = 0.91, respectively)2.

Application of AtacWorks to dscATAC-seq of human blood. Published dscATAC-seq datasets from human B cells, monocytes, and NK cells were obtained17. 2400 cells (~48 million reads) of each type were randomly selected to generate clean high coverage signal tracks and peak calls. Then, 1 cell (~20,000 reads), 5 cells (~100,000 reads), 10 cells (~200,000 reads), or 50 cells (~1 million reads) were randomly sampled from the 2400 cells of each type to obtain noisy low-coverage data. For B cells and monocytes, this subsampling was repeated 5 times for 5, 10, and 50 cells, and 15 times for 1 cell in order to generate diverse training data. For each subsampling level, the data from B cells and monocytes was used to train a model, which was then tested on the corresponding subsampled data from NK cells. The 1 cell denoising model was tested on 4 different randomly chosen NK cells to obtain a more robust estimate of its performance.

In order to perform both tasks, the input was passed through several residual blocks, followed by a regression output layer that returns the predicted ATAC-seq signal at each position in the input. The regression output was then passed through another series of residual blocks followed by a classiﬁcation output layer that returned a prediction for whether each base in the input is part of a peak. The rectiﬁed linear unit (ReLU) activation function was used throughout the network, except for the classiﬁcation output layer, which used a sigmoid activation function. The sigmoid activation forced the network to return a value between 0 and 1 for each input base, which was interpreted as the probability of that base being part of a peak. A cutoff of 0.5 was used to call peaks from these probability values.

Other convolutional neural network architectures, including the U-Net39 were tested, and the selected architecture was chosen based on its robust performance in both denoising and peak calling tasks on several datasets.

Application of AtacWorks to dscATAC-seq of mouse brain. dscATAC-seq data from the mouse brain18 was obtained, and 1800 cells (~48 million reads) each of the EN04 and EN12 excitatory neuron types were randomly selected to generate clean high coverage signal tracks and peak calls. Then, 4 cells (~100,000 reads), 8 cells (~200,000 reads) or 40 cells (~1 million reads) were randomly selected from among the 1800 cells of each type, to obtain noisy low-coverage data. The Atac- Works models trained on dscATAC-seq data from human B cells and monocytes were then applied to denoise these noisy datasets. Models were matched to low- coverage data based on sequencing depth; thus, the model trained on ten blood cells was applied to eight mouse brain cells as the latter had slightly higher sequencing depth. The denoised tracks and peak calls produced by AtacWorks were evaluated by comparing them to the clean tracks and peak calls for the same cell types.

Model training in AtacWorks. All deep learning models were trained using a multi-part loss function, comprising a weighted sum of three individual loss functions:

Application of AtacWorks to sciATAC-seq and dsciATAC-seq. Two experi- ments were performed to test whether AtacWorks models could generalize to single-cell data sequenced using different platforms.

1. Mean squared error (MSE; for the regression output) 2. 1 - Pearson correlation coefﬁcient (for the regression output) 3. Binary cross-entropy (for the classiﬁcation output) The relative importance of these loss functions was tuned by assigning different

weights to each (Supplementary Table 14).

Training examples were randomly shufﬂed at the beginning of each training epoch and passed to the deep learning model in batches of 64 examples each, unless otherwise speciﬁed (Supplementary Table 14). At the end of each epoch of training, the performance of the model on the validation set was evaluated, and the model with the best validation set performance was saved and used.

First, dsciATAC-seq data from human blood cell types was obtained17. Data was aggregated over 20,378 CD4+ T cells to generate a clean high coverage signal track (~43 million reads) and peak calls. 450 cells (~1 million reads) were subsampled to obtain noisy low-coverage data. The dscATAC-seq model trained on 50 human blood cells (described above) was applied to denoise and call peaks from this noisy dataset. The denoised tracks and peak calls produced by AtacWorks were evaluated by comparing them to the clean high coverage signal track. Due to the low sequencing depth for other cell types in this dataset, it was not possible to generate sufﬁciently high-coverage clean tracks for any other cell types besides CD4+ T cells.

Models were trained using the Adam optimizer40 with a learning rate of 2 × 10−4

for 25 epochs.

Second, sciATAC-seq data from a mouse lung tumor was obtained18. The sequencing depth in this dataset was insufﬁcient to obtain clean datasets of >40

8

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

ARTICLE

million reads as described in the previous examples. Instead, clean coverage tracks and peak calls were obtained by aggregating data over 550 cells (~15 million reads) each of B cells, monocytes and macrophages. 35 cells (~1 million reads) were randomly sampled from among the 550 cells of each type to obtain noisy low- coverage data. For B cells and monocytes, this subsampling was repeated ﬁve times in order to generate diverse training data. The data from B cells and monocytes was used to train a model, which was then tested on the subsampled data from the macrophages.

To demonstrate the feasibility of cross-platform application, dscATAC-seq data from human monocytes and B cells was subsampled to generate data of the same sequencing depths as the sci-ATAC data, i.e., 700 cells (~15 million reads) were aggregated to generate clean data, and 50 cells (~1 million reads) were aggregated to generate noisy data. Subsampling was repeated ﬁve times to generate diverse training data. A model was trained using this dscATAC-seq data and was applied to the subsampled sciATAC-seq dataset of macrophages.

A custom sequencing primer (part of the SureCell ATAC-Seq Library Prep Kit) is required for read 1.

Preprocessing of dscATAC-seq data for FACS-isolated HSCs. Per-read bead barcodes were parsed and trimmed using UMI-tools v1.0.041. Constitutive ele- ments of the bead barcodes were assigned to the closest known sequence allowing for up to 1 mismatch per 6-mer or 7-mer (mean >99% parsing efﬁciency across experiments). Paired-end reads were aligned to hg19 using BWA v0.7.1742 on the Illumina BaseSpace online application. Bead-based ATAC-seq processing (BAP)17 was used to identify systematic biases (i.e., reads aligning to an inordinately large number of barcodes) and barcode-aware deduplicate reads, as well as perform merging of multiple bead barcode instances associated with the same cell. Barcode merging was necessary due to the nature of the BioRad SureCell scATAC-seq procedure used in this study, which enables multiple beads per droplet. BAP was given an alignment (.bam) ﬁle for a given experiment with a bead barcode identiﬁer indicated by a SAM tag as input. Aligned reads were combined using samtools merge (v1.9).

Adding binding motif locations for CTCF ChIP-seq prediction. The deep learning model was modiﬁed to take additional inputs along with the noisy ATAC- seq signal. Potential CTCF (CCCTC-binding factor) binding sites were identiﬁed on both strands of the genome using motifmatchr (https://github.com/ GreenleafLab/motifmatchr). The top 200,000 sites were selected and expanded to 500 bp regions centered on the known binding motif. In order to predict CTCF ChIP-seq peaks from ATAC-seq data, the model was given the positions of CTCF binding motifs on the genome in addition to the noisy ATAC-seq coverage track. For every position in the genome, the model received three numeric inputs: the coverage at that position in the noisy ATAC-seq dataset, a 0 or 1 representing whether that position was part of a CTCF binding motif on the forward strand, and a 0 or 1 representing whether that position was part of a CTCF binding motif on the reverse strand.

Bulk-guided projection of single cells. The bulk-guided UMAP projection of single cells (Fig. 2c) was performed as described in Lareau et al.17. In brief, a common set of peaks (k = 156,311) was used to create a vector of read counts for each CD34+ single-cell ATAC-seq proﬁle. Principal Component Analysis (PCA) was run on published bulk ATAC-seq data2 to generate eigenvectors capturing variations in regulatory element accessibility across cell types. Each single cell was then projected in the same space as these eigenvectors by multiplying their counts vector by the common PCA loading coefﬁcients. The resulting projection scores were scaled and centered prior to being visualized using UMAP. Predicted labels for the CD34+ cells were derived by correlating their projected single-cell scores with those of a reference set of FACS-isolated PBMCs24 and assigning the label of the closest match.

Generation of dscATAC-seq data for FACS-isolated HSCs. Cryopreserved human BMMCs were purchased from Allcells (catalog number BM, CR, MNC, 10 M). Cells were quickly thawed in a 37 °C water bath, rinsed with culture medium (RPMI 1640 medium supplemented with 15% FBS) and then treated with 0.2 U/μL DNase I (Thermo Fisher Scientiﬁc) in 2 mL of culture medium at room tem- perature for 15 min. After DNase I treatment, cells were ﬁltered with a 40 μm cell strainer, washed with MACS buffer (1x PBS, 2 mM EDTA and 0.5% BSA), and cell viability and concentration were measured with trypan blue on the TC20 Auto- mated Cell Counter (Bio-Rad). Cell viability was greater than 90% for all samples. CD34+ cells were then bead enriched using the CD34 MicroBead Kit UltraPure (Miltenyi Biotec, catalog number 130-100-453) following manufacturer’s instruc- tions. The enriched population was then simultaneously stained with CD45, Lineage cocktail, CD34, CD38, CD45RA and CD90 antibodies in MACS buffer for 20 min at 4 °C, using the following antibody dilutions: CD45 (BV711; BioLegend #304050) - 1:100, Lineage cocktail (FITC; BioLegend #348801) - 1:25, CD34 (APC- Cy7; BioLegend #343514) - 1:50, CD38 (PE-Cy7; BioLegend #303516) - 1:50, CD45RA (BUV737; BD Biosciences #612846) - 1:50, CD90 (BV421; BioLegend #328122) - 1:25. Stained cells were then washed with MACS buffer and the CD45+ Lin- CD38− CD34+ CD45RA− CD90+ fraction (HSCs) was FACS sorted using a MoFlo Astrios EQ Cell Sorter (Beckman Coulter), using the Beckman Coulter MoFlo Astrios EQ Cell Sorter’s Summit v62 software to collect the data. The FACS data was analyzed using FlowJo v10.7, and the gating strategy is shown in Sup- plementary Fig. 9.

Single-cell ATAC-seq data was then generated for the sorted HSCs using the dscATAC-seq Whole Cell protocol as described in Lareau et al.17. For a detailed description of tagmentation protocols and buffer formulations, refer to the SureCell ATAC-Seq Library Prep Kit (17004620, Bio-Rad) User Guide (10000106678, Bio- Rad). Brieﬂy, the sorted HSCs were resuspended in Whole Cell Tagmentation Mix containing 0.1% Tween-20, 0.01% digitonin, 1× PBS supplemented with 0.1% BSA, ATAC Tagmentation Buffer and ATAC Tagmentation Enzyme. Cells were mixed and agitated on a ThermoMixer (5382000023, Eppendorf) for 30 min at 37 °C. Tagmented cells were kept on ice before being loaded onto a ddSEQ Single-Cell Isolator (12004336, Bio-Rad). scATAC-seq libraries were prepared using the SureCell ATAC-Seq Library Prep Kit (17004620, Bio-Rad) and SureCell ATAC-Seq Index Kit (12009360, Bio-Rad). Bead barcoding and sample indexing were performed in a C1000 Touch thermal cycler with a 96-Deep Well Reaction Module (1851197, Bio-Rad); PCR conditions were as follows: 37 °C for 30 min, 85 °C for 10 min, 72 °C for 5 min, 98 °C for 30 s, eight cycles of 98 °C for 10 s, 55 °C for 30 s and 72 °C for 60 s, and a single 72 °C extension for 5 min to ﬁnish. Emulsions were broken and products were cleaned up using Ampure XP beads (A63880, Beckman Coulter). Barcoded amplicons were further ampliﬁed using a C1000 Touch thermal cycler with a 96-Deep Well Reaction Module; PCR conditions were as follows: 98 ° C for 30 s, seven cycles of 98 °C for 10 s, 55 °C for 30 s and 72 °C for 60 s, and a single 72 °C extension for 5 min to ﬁnish. PCR products were puriﬁed using Ampure XP beads and quantiﬁed on an Agilent Bioanalyzer (G2939BA, Agilent) using the High-Sensitivity DNA kit (5067-4626, Agilent). Libraries were loaded at 1.5 pM on a NextSeq 550 (SY-415-1002, Illumina) using the NextSeq High Output Kit (150 cycles; 20024907, Illumina) and sequencing was performed using the following read protocol: read 1, 118 cycles; i7 index read, 8 cycles; read 2, 40 cycles.

Transcription factor motif accessibility z-scores. Motif accessibility z-scores for GATA2 (Fig. 2d) were computed using chromVAR version 1.12.027. The method calculates enrichment or depletion in accessibility within peaks that share a common transcription factor motif while adjusting for GC content and overall region accessibility. The single cells were scored using a list of human transcription factor motifs from the CIS-BP database (http://cisbp.ccbr.utoronto.ca/index.php).

Smoothed gene accessibility scores. Gene accessibility scores for MEF2C (Fig. 2e) were computed as described in Lareau et al.17. Brieﬂy, to obtain gene scores for a particular gene across all cells, any sequencing reads within 10 kb of the gene’s transcription start site were compiled and weighted using an inverse exponential decay function. The weighted reads were then summed for each cell and smoothed by averaging the scores from each cell’s 50 nearest neighbors in principal component space. A list of TSSs for hg19 was obtained from the UCSC Table Browser (https://genome.ucsc.edu/cgi-bin/hgTables).

Denoising lineage-priming HSCs with AtacWorks. Each subsample of lineage- priming HSCs was generated by selecting a single HSC and aggregating the 50 most similar HSCs in principal component space. The selected HSCs were chosen and annotated based on their proximity to speciﬁc populations of labeled CD34+ cells (Fig. 2b). After aggregation, three resulting subsamples were converted from BAM to bigWig format as described in Data Preprocessing and denoised using a model trained on dscATAC-seq data from B cells and monocytes. The denoised tracks were then normalized by coverage for cross-sample comparisons.

Denoising of randomly permuted HSCs with AtacWorks. A list of differentially expressed genes in blood cells was obtained from the Human Cell Atlas Data Portal (https://data.humancellatlas.org) and ﬁltered down to a set of 2303 genes relevant to HSCs. Transcription start sites (TSSs) for each of these genes were obtained and expanded by 100 kb in both directions to generate a set of hematopoiesis regulatory regions comprising around 300 million bases, or 10% of the genome.

To provide a background model for the denoised lineage-primed samples, 1000 subsamples were generated by randomly selecting 1000 HSCs from the pool of 9974 and for each selected cell, aggregating the 50 most similar HSCs in principal component space. These random samples were converted from BAM to bigWig format as described in Data Preprocessing. The 1000 random samples were then denoised using the same AtacWorks model used to denoise the lineage-priming HSCs, but only in deﬁned hematopoiesis regulatory regions, reducing the runtime by over 90%. The denoised random samples were normalized by coverage. For each genomic position in the hematopoiesis regulatory regions, a mean and standard deviation of coverage was calculated across the 1000 denoised random samples. For each subsample of lineage-primed HSCs, a z-score for each genomic position in the hematopoiesis regulatory regions was generated based on the normalized coverage relative to the mean and standard deviation in the 1000 denoised random samples. Regulatory peaks were called by combining all genomic positions with an absolute z-score >2 within 200 bp of each other. The top z-scores for each peak were converted to p values and then corrected for multiple hypothesis

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

9

ARTICLE

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

testing using the Benjamini Hochberg procedure. All peaks with a false discovery rate <0.05 were saved in a BED ﬁle. Peaks were then ﬁltered by a minimum coverage value to remove low-coverage regions that would not be identiﬁed through typical ATAC-seq analysis. BED ﬁles were converted to bigWig format for visualization using the bedGraphtoBigWig utility (v4).

Code availability AtacWorks is available at https://github.com/clara-parabricks/AtacWorks12. Custom scripts used to batch process samples for input and identify differentially-accessible regulatory regions in lineage-primed hematopoietic stem cells are available at https:// github.com/zchiang/atacworks_analysis44.

Validation of putative regulatory elements. The set of 28,505 bead-enriched CD34+ bone marrow progenitor cells was loaded into chromVAR27 as described in Lareau et al.17. In brief, the published BAM ﬁles were converted to a cells by peaks matrix, where each matrix element represents the sequencing coverage. The sets of ﬁltered genomic regions for each subsample of lineage-primed HSCs were then loaded as discrete annotations. The chromVAR computeDeviations function was then used to quantify the normalized accessibility of each of these subsets in every CD34+. The resulting accessibility z-scores were then visualized on the UMAP projection to conﬁrm that the identiﬁed lineage-priming elements were generally more accessible in the corresponding differentiated cell populations. To quantify the most differentially-accessible transcription factor motifs across these elements, a new counts matrix was generated in chromVAR, but only from HSCs and the identiﬁed lineage-priming peaks. The overlap between the peaks and transcription factor motifs was found, and then the normalized accessibility of any overlapping motifs was calculated using the computeDeviations function. Lastly, the variability of each motif was calculated using the computeVariability function.

Received: 20 April 2020; Accepted: 3 February 2021;

References 1.

Buenrostro, J. D., Giresi, P. G., Zaba, L. C., Chang, H. Y. & Greenleaf, W. J. Transposition of native chromatin for fast and sensitive epigenomic proﬁling of open chromatin, DNA-binding proteins and nucleosome position. Nat. Methods 10, 1213–1218 (2013).

2. Corces, M. R. et al. Lineage-speciﬁc and single-cell chromatin accessibility charts human hematopoiesis and leukemia evolution. Nat. Genet. 48, 1193–1203 (2016). vol.

3. Yoshida, H. et al. The cis-Regulatory Atlas of the Mouse Immune System. Cell 176, 897–912 (2019). e20.

Data visualization. Unless otherwise speciﬁed, the WashU epigenome browser (http://epigenomegateway.wustl.edu/browser/) was used for ATAC-seq signal track visualization. The denoised lineage-priming HSC subsamples (Fig. 3f) were visualized using the Integrative Genomics Viewer43.

4. Corces, M. R. et al. The chromatin accessibility landscape of primary human cancers. Science 362, eaav1898 (2018). Buenrostro, J. D. et al. Single-cell chromatin accessibility reveals principles of regulatory variation. Nature 523, 486–490 (2015).

4. Corces, M. R. et al. The chromatin accessibility landscape of primary human cancers. Science 362, eaav1898 (2018). Buenrostro, J. D. et al. Single-cell chromatin accessibility reveals principles of regulatory variation. Nature 523, 486–490 (2015).

Reporting summary. Further information on experimental design is available in the Nature Research Reporting Summary linked to this paper.

6. Corces, M. R. et al. An improved ATAC-seq protocol reduces background and enables interrogation of frozen tissues. Nat. Methods 14, 959–962 (2017). vol. Pascual, S., Bonafonte, A. & Serrà, J. SEGAN: speech Enhancement Generative Adversarial Network. Preprint at https://arxiv.org/abs/1703.09452 (2017).

7.

Data availability Bulk ATAC-seq datasets of various blood cell types are available from GEO under accession number “GSE74912 [https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi? acc=GSE74912]”. From these datasets, B cells, NK cells, CD4+ and CD8+ T cells were used for model training, while erythroblasts and monocytes were used for testing. For the transcription factor footprinting model, NK cells, CD8+ T cells, and multipotent progenitor (MPP) cells were used for training, while HSCs were used for testing. The bulk ATAC-seq dataset for Peyer’s Patch is available from ENCODE under experiment “ENCSR017RQC [https://www.encodeproject.org/experiments/ENCSR017RQC/]”.

The dscATAC-seq dataset of hematopoietic stem cells generated for this study is available from GEO under accession number “GSE147113 [https://www.ncbi.nlm.nih. gov/geo/query/acc.cgi?acc=GSE147113]”.

Other dscATAC-seq and dsciATAC-seq datasets are available from GEO under

8. Yang, C. et al. High-Resolution Image Inpainting using Multi-Scale Neural Patch Synthesis. Preprint at https://arxiv.org/abs/1611.09969 (2016). Liu, G. et al. Image Inpainting for Irregular Holes Using Partial Convolutions. Preprint at https://arxiv.org/abs/1804.07723 (2018).

9.

10. Koh, P. W., Pierson, E. & Kundaje, A. Denoising genome-wide histone ChIP- seq with convolutional neural networks. Bioinformatics 33, i225–i233 (2017).

11. Rai, V. et al. Single-cell ATAC-Seq in human pancreatic islets and deep learning upscaling of rare cells reveals cell-speciﬁc type 2 diabetes regulatory signatures. Mol. Metab. 32, 109–121 (2020).

12. Lal, A. et al. AtacWorks v0.3.0. (2021). https://doi.org/10.5281/zenodo.4421705. 13. He, K., Zhang, X., Ren, S. & Sun, J. Deep residual learning for image recognition. Proceedings of the IEEE conference on computer vision and pattern recognition, 770–778, (Institute of Electrical and Electronics Engineers, 2016). 14. Zhang, Y. et al. Model-based analysis of ChIP-Seq (MACS). Genome Biol. 9,

accession number “GSE123581 [https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi? acc=GSE123581]”. From these datasets, CD4+ T cells, CD8+ T cells, and pre-B cells were used for model training, while monocytes were used for testing. Bead-isolated CD34+ cells were used for the combined UMAP projection. The sciATAC-seq datasets of B cells, monocytes, and macrophages from primary lung tumor are available from GEO under accession number “GSE145194 [https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi? acc=GSE145194]”. B cells and monocytes were used for model training, while macrophages were used for testing. The scATAC-seq dataset of FACS-isolated peripheral blood mononuclear cells (PBMCs) is available from GEO under accession number “GSE96772 [https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE96772]”. These cells were used to infer cell type labels for CD34+ cells in the combined UMAP projection.

R137 (2008).

15. Consortium, T. E. P., The ENCODE Project Consortium. An integrated encyclopedia of DNA elements in the human genome. Nature 489, 57–74 (2012). vol.

16. Davis, C. A. et al. The Encyclopedia of DNA elements (ENCODE): data portal update. Nucleic Acids Res 46, D794–D801 (2018).

17. Lareau, C. A. et al. Droplet-based combinatorial indexing for massive-scale single-cell chromatin accessibility. Nat. Biotechnol. 37, 916–924 (2019). 18. LaFave, L. M. et al. Epigenomic State Transitions Characterize Tumor Progression in Mouse Lung Adenocarcinoma. Cancer Cell 38, 212–228 (2020). vole13.

CTCF ChIP-seq tracks are available from ENCODE under experiments

“ENCSR000DLK [https://www.encodeproject.org/experiments/ENCSR000DLK/]” (HSCs), “ENCSR000ATN [https://www.encodeproject.org/experiments/ ENCSR000ATN/]” (Monocytes) and “ENCSR000AUV [https://www.encodeproject.org/ experiments/ENCSR000AUV/]” (B cells). H3K27ac ChIP-seq tracks are available from ENCODE under experiments “ENCSR000AUP [https://www.encodeproject.org/ experiments/ENCSR000AUP/]” (B cells) and “ENCSR000ASJ [https://www. encodeproject.org/experiments/ENCSR000ASJ/]” (monocytes).

The list of human transcription factor motifs was curated from the CIS-BP database

19. Neph, S. et al. An expansive human regulatory lexicon encoded in transcription factor footprints. Nature 489, 83–90 (2012).

20. Skene, P. J. & Henikoff, S. An efﬁcient targeted nuclease strategy for high-

resolution mapping of DNA binding sites. Elife 6, e21856 (2017). 21. Creyghton, M. P. et al. Histone H3K27ac separates active from poised

enhancers and predicts developmental state. Proc. Natl Acad. Sci. U. S. A. 107, 21931–21936 (2010).

22. Arzate-Mejía, R. G., Recillas-Targa, F. & Corces, V. G. Developing in 3D: the role of CTCF in cell differentiation. Development 145, dev137729 (2018).

(http://cisbp.ccbr.utoronto.ca/index.php) and is available at https://github.com/ GreenleafLab/chromVARmotifs. The list of transcription start sites for hg19 was obtained from the UCSC Table Browser (https://genome.ucsc.edu/cgi-bin/hgTables). The list of differentially expressed genes in blood cells was curated from the Human Cell Atlas Data Portal (https://data.humancellatlas.org) and is available at https://github.com/ zchiang/atacworks_analysis.

23. Yu, V. W. C. et al. Epigenetic Memory Underlies Cell-Autonomous Heterogeneous Behavior of Hematopoietic Stem Cells. Cell 168, 944–945 (2017).

24. Buenrostro, J. D. et al. Integrated Single-Cell Analysis Maps the Continuous Regulatory Landscape of Human Hematopoietic Differentiation. Cell 173, 1535–1548 (2018). e16.

All of the processed data, trained models, and output signal tracks described in this

paper are publicly available at https://atacworks-paper.s3.us-east-2.amazonaws.com.

25. Rodriguez-Fraticelli, A. E. et al. Clonal analysis of lineage fate in native haematopoiesis. Nature 553, 212–216 (2018).

All other relevant data supporting the key ﬁndings of this study are available within the article and its Supplementary Information ﬁles or from the corresponding author upon reasonable request. Source data are provided with this paper. A reporting summary for this Article is available as a Supplementary Information ﬁle. Source data are provided with this paper.

26. Pei, W. et al. Polylox barcoding reveals haematopoietic stem cell fates realized in vivo. Nature 548, 456–460 (2017).

27. Schep, A. N., Wu, B., Buenrostro, J. D. & Greenleaf, W. J. chromVAR: inferring transcription-factor-associated accessibility from single-cell epigenomic data. Nat. Methods 14, 975–978 (2017).

10

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-021-21765-5

ARTICLE

28. Pliner, H. A. et al. Cicero Predicts cis-Regulatory DNA Interactions from Single-Cell Chromatin Accessibility Data. Mol. Cell 71, 858–871 (2018). e8. 29. Weinreb, C., Rodriguez-Fraticelli, A., Camargo, F. D. & Klein, A. M. Lineage tracing on transcriptional landscapes links state to fate during differentiation. Science 367, eaaw3381 (2020).

30. Trikha, P. et al. E2f1–3 Are Critical for Myeloid Development. J. Biol. Chem. 286, 4783–4795 (2011).

throughout the development of this work. J.D.B., Z.D.C., and F.M.D. acknowledge support by the Allen Distinguished Investigator Program through the Paul G. Allen Frontiers Group. This work was further supported by the Chan Zuckerberg Initiative and the NIH Director’s New Innovator award. Z.D.C. is supported by the NSF- Simons Center for Mathematical and Statistical Analysis of Biology at Harvard (#1764269).

31. Baker, S. J. et al. B-myb is an essential regulator of hematopoietic stem cell and myeloid progenitor cell development. Proc. Natl Acad. Sci. U. S. A. 111, 3122–3127 (2014).

32. Bartosovic, M., Kabbe, M. & Castelo-Branco, G. Single-cell proﬁling of histone modiﬁcations in the mouse brain. Preprint at https://www.biorxiv.org/ content/10.1101/2020.09.02.279703v1 (2020).

Author contributions N.Y. and A.L. developed the deep learning model. A.L. and Z.D.C. performed data analysis. F.M.D. performed HSC dscATAC-seq experiments. A.L., Z.D.C., and J.D.B. wrote the paper with input from all authors. J.I. and J.D.B. jointly conceptualized and supervised this work. A.L. and Z.D.C. contributed equally.

33. Wu, S. J. et al. Single-cell analysis of chromatin silencing programs in developmental and tumor progression. 2020.09.04.282418 (2020) https://doi. org/10.1101/2020.09.04.282418.

34. Li, H. et al. The Sequence Alignment/Map format and SAMtools. Bioinformatics 25, 2078–2079 (2009).

Competing interests J.D.B. holds patents related to ATAC-seq and is a member of the scientiﬁc advisory board for Camp4, Seqwell, and Celsee. A.L., N.Y., and J.I. are employees of NVIDIA Corporation. All other authors declare no competing interests.

35. Quinlan, A. R. & Hall, I. M. BEDTools: a ﬂexible suite of utilities for comparing genomic features. Bioinformatics 26, 841–842 (2010).

36. Adam, P. et al. Automatic differentiation in pytorch. Proceedings of Neural Information Processing Systems, https://proceedings.neurips.cc/paper/2019/ ﬁle/bdbca288fee7f92f2bfa9f7012727740-Paper.pdf (2017).

Additional information Supplementary information The online version contains supplementary material available at https://doi.org/10.1038/s41467-021-21765-5.

37. Kudo, Y. & Aoki, Y. Dilated convolutions for image classiﬁcation and object localization. in 2017 Fifteenth IAPR International Conference on Machine Vision Applications (MVA) 452–455 (2017). Ioffe, S. & Szegedy, C. Batch Normalization: accelerating Deep Network Training by Reducing Internal Covariate Shift. Preprint at https://arxiv.org/ abs/1502.03167 (2015).

38.

Correspondence and requests for materials should be addressed to J.I. or J.D.B.

Peer review information Nature Communications thanks Andrew Adey, Nathan Shefﬁeld, Jie Zheng and the other, anonymous, reviewer(s) for their contribution to the peer review of this work. Peer reviewer reports are available.

39. Ronneberger, O., Fischer, P. & Brox, T. U-Net: Convolutional Networks for Biomedical Image Segmentation. Lecture Notes in Computer Science 234–241 (2015) https://doi.org/10.1007/978-3-319-24574-4_28.

40. Kingma, D. P. & Ba, J. Adam: a Method for Stochastic Optimization. Preprint at https://arxiv.org/abs/1412.6980 (2014).

Reprints and permission information is available at http://www.nature.com/reprints

Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional afﬁliations.

41. Smith, T., Heger, A. & Sudbery, I. UMI-tools: modeling sequencing errors in Unique Molecular Identiﬁers to improve quantiﬁcation accuracy. Genome Res. 27, 491–499 (2017).

42. Li, H. & Durbin, R. Fast and accurate short read alignment with Burrows- Wheeler transform. Bioinformatics 25, 1754–1760 (2009).

43. Robinson, J. T. et al. Integrative genomics viewer. Nat. Biotechnol. 29, 24–26 (2011).

44. Chiang, Z. zchiang/atacworks_analysis: AtacWorks preprocessing and HSC analysis code. (2021) https://doi.org/10.5281/zenodo.4433018.

Acknowledgements We thank Eric Xu, Joyjit Daw, Neha Tadimeti and Ohad Mosaﬁ for contributing to the code for AtacWorks. We thank Ronald Lebofsky and Giulia Schiroli for assistance in generating dscATAC-seq data. We thank Yan Hu for critical reading of the paper. We thank members of the Buenrostro lab and NVIDIA team for insightful comments

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this license, visit http://creativecommons.org/ licenses/by/4.0/.

© The Author(s) 2021

NATURE COMMUNICATIONS|

(2021) 12:1507 |https://doi.org/10.1038/s41467-021-21765-5|www.nature.com/naturecommunications

11