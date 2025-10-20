; , : ) (

0 9 8 7 6 5 4 3 2 1

; , : ) (

0 9 8 7 6 5 4 3 2 1

npj | digital medicine

Article

Published in partnership with Seoul National University Bundang Hospital

https://doi.org/10.1038/s41746-024-01126-4

An in-depth evaluation of federated learning on biomedical natural language processing for information extraction

Check for updates

LePeng 1, GaoxiangLuo 2, SichengZhou3, JiandongChen3, Ziyue Xu4, JuSun 1

&RuiZhang 5

Language models (LMs) such as BERT and GPT have revolutionized natural language processing (NLP). However, the medical ﬁeld faces challenges in training LMs due to limited data access and privacyconstraintsimposedbyregulationsliketheHealthInsurancePortabilityandAccountabilityAct (HIPPA) and the General Data Protection Regulation (GDPR). Federated learning (FL) offers a decentralizedsolutionthatenablescollaborativelearningwhileensuringdataprivacy.Inthisstudy,we evaluated FL on 2 biomedical NLP tasks encompassing 8 corpora using 6 LMs. Our results show that: (1) FL models consistently outperformed models trained on individual clients’ data and sometimes performed comparably with models trained with polled data; (2) with the ﬁxed number of total data, FL models training with more clients produced inferior performance but pre-trained transformer-based modelsexhibitedgreatresilience.(3)FLmodelssigniﬁcantlyoutperformedpre-trainedLLMswithfew- shot prompting.

The recent advances in deep learning have sparked the widespread adoption of language models (LMs), including prominent examples of BERT1andGPT2,intheﬁeldofnaturallanguageprocessing(NLP).These LMs are trained on massive amounts of public text data, comprising billions of words, and have emerged as the dominant technology for various linguistic tasks, including text classiﬁcation3,4, text generation5,6, informationextraction7–9,andquestionanswering10,11.ThesuccessofLMs can be largely attributed to their ability to leverage large volumes of training data. However, in privacy-sensitive domains like medicine, data are often naturally distributed, making it difﬁcult to construct large cor- pora to train LMs. To tackle the challenge, the most common approach thusfarhasbeentoﬁne-tunepre-trainedLMsfordownstreamtasksusing limited annotated data12,13. Nevertheless, pre-trained LMs are typically trained on text data collected from the general domain, which exhibits divergent patterns from that in the biomedical domain, resulting in a phenomenon known as domain shift. Compared to general text, biome- dical texts can be highly specialized, containing domain-speciﬁc ter- minologies and abbreviations14. For example, medical records and drug descriptions often include speciﬁc terms that may not be present in general language corpora, and the terms often vary among different lacks uniformity and clinical

standardization across sources, making it challenging to develop NLP models that can effectively handle different formats and structures. Electronic Health Records (EHRs) from different healthcare institutions, for instance, can have varying templates and coding systems15. So, direct transfer learning from LMs pre-trained on the general domain usually suffers a drop in performance and generalizability when applied to the medical domain as is also demonstrated in the literature16. Therefore, developing LMs that are speciﬁcally designed for the medical domain, usinglargevolumesofdomain-speciﬁctrainingdata,isessential.Another vein of research explores pre-training the LM on biomedical data, e.g., BlueBERT12 and PubMedBERT17. These LMs were either pre-trained on mixed-domain data (ﬁrst pre-train on the general text and then keep pre- trainonbiomedicaltext)ordirectlypre-trainedondomain-speciﬁcpublic medical datasets, e.g., PubMed literature and the Medical Information Mart for Intensive Care (MIMIC III)18 and have shown improved per- formances compared to classical methods such as conditional random ﬁeld (CRF)19 and recurrent neural network (RNN) (e.g., long-short-term text mining tasks8,9,12,16,21. memory (LSTM)20) in many biomedical Nonetheless, it is important to highlight that the efﬁcacy of these pre- trained medical LMs heavily relies on the availability of large volumes of task-relevant public data, which may not always be readily accessible.

institutes. Also, biomedical data

1Department of Computer Science and Engineering, University of Minnesota, Minneapolis, MN, USA. 2Department of Computer and Information Science, University of Pennsylvania, Philadelphia, PA, USA. 3Institute for Health Informatics, University of Minnesota, Minneapolis, MN, USA. 4Nvidia Corporation, Santa Clara, CA, USA. 5Division ofComputational Health Sciences, DepartmentofSurgery, University ofMinnesota,Minneapolis,MN, USA. e-mail: jusun@umn.edu; zhan1386@umn.edu

npj Digital Medicine|

(2024) 7:127

1

https://doi.org/10.1038/s41746-024-01126-4

All these mentioned above represent the classical centralized learning regime, which involves aggregating data from distributed data sites and training a model in a single environment. However, this approach poses signiﬁcant challenges in medicine, where data privacy is crucial and data access is restricted due to regulatory concerns. Thus, in practice,people can only perform training with local datasets—single-client training. The drawback comes when the local dataset is small and often gives poor per- formance when evaluating an external dataset—poor generalization. To take advantage of the massively distributed data as well as improve the model generalizability, federated learning (FL) was initialized in 201622 as a novel learning scheme to empower training with a decentralized environ- ment and achieve many successes in critical domains with data privacy restriction23–25. In an FL training loop, clients jointly train a shared global model by sharing the model weights or gradients while keeping their data stored locally. By bringing the model to the data, FL strictly ensures data privacy while achieving competitive levels of performance compared to a model trained with pooled data. While there is a rise of research showing great promise of applying FL in general NLP26,27, applications of FL in biomedical NLP are still under-explored. Existing works in FL on biome- dicalNLPareeitherfocusedonoptimizingonetask28,29ortryingtoimprove communication efﬁciency28. The current literature lacks a comprehensive comparison of FL on varied biomedical NLP tasks with real-world pertur- bations. To close this gap, we conducted an in-depth study of two repre- sentative NLP tasks, i.e., named entity recognition (NER) and relation extraction(RE),toevaluatethefeasibilityofadoptingFL(e.g.,FedAvg30and FedProx31) with LMs (e.g., Transformer-based models) in biomedical NLP. Our study aims to provide an in-depth investigation of FL in biomedical NLP by studying several FL variants on multiple practical learning sce- narios,includingvariedfederationscales,differentmodelarchitectures,data heterogeneities, and comparison with large language models (LLMs) on multiple benchmark datasets. Our major ﬁndings include:

1. Whendatawereindependentandidenticallydistributed(IID),models trained using FL, especially pre-trained BERT-based models, performed comparable to centralized learning, a signiﬁcant boost to single-client learning. Even when data were non-IID distributed, the gap can be ﬁlled by using alternative FL algorithms.

2. Larger models exhibited better resistance to the changes in FL scales. With a ﬁxed number of data, the performance of FL models overall degraded as the clients’ size increased. However, the deterioration diminished when combined with larger pre-trained models such as BERT-based models and GPT-2.

3. FLsigniﬁcantlyoutperformedpre-trainedLLMs,e.g.,GPT-4,PaLM2, and Gemini Pro, with few-shot prompting.

Results Inthissection,wepresentourmainresultsofanalysisonFLwithafocuson several practical facets, including (1) learning tasks, (2) scalability, (3) data distribution, (4) model architectures and sizes, and (5) comparative assessments with LLMs.

FedAvg, single-client, and centralized learning for NER and RE tasks Table1offersasummaryoftheperformanceevaluationsforFedAvg,single- clientlearning,andcentralizedlearningon ﬁveNERdatasets, whileTable2 presents the results on three RE datasets. Our results on both tasks con- sistently demonstrate that FedAvg outperformed single-client learning. Notably, in cases involving large data volumes, such as BC4CHEMD and 2018 n2c2, FedAvg managed to attain performance levels on par with centralized learning, especially when combined with BERT-based pre- trained models.

Inﬂuence of FL scale on the performance of LMs In clinical applications, there are two distinct learning paradigms. The ﬁrst involves small-scale client cohorts, each equipped with substantial data resources,oftenseenincollaborationswithinhospitalnetworks.Incontrast,

npj Digital Medicine|

(2024) 7:127

Article

the second encompasses widely distributed clients, characterized by more limited data holders, often associated with collaborations within clinical facilitiesor on mobileplatforms. Weinvestigated theperformanceofFLon the two learning paradigms by varying client group sizes whilemaintaining a ﬁxed total training data volume. The results are summarized in Fig. 1, revealingaconsistenttrend:notably,largermodels,suchasthosebackedby BERT and GPT-2 architectures, exhibited great resilience to ﬂuctuations in federationscales.Incontrast,thelightweightmodel,asofBiLSMT-CRF,was susceptible to alterations of scale, resulting in a rapid deterioration in per- formance as the number of participating clients increased.

Comparison of FedAvg and FedProx with data heterogeneity Biomedical texts often exhibit high specialization due to distinct protocols employed by different hospitals when generating medical records, resulting in great variations—sublanguage differences. Therefore, FL practitioners should account for such data heterogeneity when implementing FL in healthcare systems. We simulated a real non-IID scenario by emulating BC2GM and JNLPBA as two clients and jointly performing FL. We con- sidered two FL algorithms including FedAvg and FedProx; both are widely deployed in practice. For comparison, we also studied a simulated IID settingusingthe2018n2c2datasetbyrandomsplitting.Detailedanalysisof the non-IID/IID distribution can be found in Supplementary Fig. 1 and Supplementary Table 3. As shown in Table 3, we observed that the per- formance of FedProx was sensitive to the choice of the hyper-parameter μ. Notably, a smaller μ consistently resulted in improved performance. When μwascarefullyselected,FedProxoutperformedFedAvgwhenthedatawere non-IIDdistributed(lenientF1scoreof0.994vs.0.934andstrictF1scoreof 0.901 vs. 0.884). However, the difference between the two algorithms was mostly indistinguishable when the data were IID distributed (lenient F1 score of 0.880 vs. 0.879 and strict F1 score of 0.820 vs. 0.818).

Impact of the LM size on the performance of different training schemes We investigated the impact of model size on the performance of FL. We compared 6 models with varying sizes, with the smallest one comprising 20M parameters and the largest one comprising 334M parameters. We picked the BC2GM dataset for illustration and anticipated similar trends wouldholdforotherdatasetsaswell.AsshowninFig.2,inmostcases,larger models (represented by large circles) overall exhibited better test perfor- mance than their smaller counterparts. For example, BlueBERT demon- strated uniform enhancements in performance compared to BiLSTM-CRF and GPT2. Among all the models, BioBERT emergedas the top performer, whereas GPT-2 gave the worst performance.

Comparison between FL and LLM Inlightofthewell-demonstratedperformanceofLLMsonvariouslinguistic tasks,weexploredtheperformancegapofLLMstothesmallerLMstrained using FL. Notably, it is usually not common to ﬁne-tune LLMs due to the formidablecomputationalcostsandprotractedtrainingtime.Therefore,we utilized in-context learning that enables direct inference from pre-trained LLMs, speciﬁcally few-shot prompting, and compared them with models trainedusingFL.Wefollowedtheexperimentalprotocoloutlinedinarecent study32 and evaluated all the models on two NER datasets (2018 n2c2 and NCBI-disease) and two RE datasets (2018 n2c2, and GAD). The results, as summarized in Fig. 3, show that (1) a longer prompt with more input examples (e.g., 10-shot and 20-shot) often enhances the performance of LLMs; and (2) FL, whether implemented with a BERT-based model (BlueBERT) or GPT-based model (GPT-2), consistently outperformed LLMs by a large margin.

Discussion In this study, we visitedFL for biomedical NLPand studiedtwo established tasks(NERandRE)across7benchmarkdatasets.Weexamined6LMswith varying parameter sizes (ranging from BiLSTM-CRF with 20M to transformer-based models up to 334M parameters) and compared their

2

https://doi.org/10.1038/s41746-024-01126-4

e d s n

i

i

, r e w o

l (

t c i r t s d n a ) r e p p u

(

t n e n e

i

l

h t i

w e r o c s - 1 F y b d e r u s a e m s k s a t

R E N 5 n o g n n r a e

i

l

t n e

i l

c - e g n s d n a g n n r a e

l

i

i

l

d e z

i l

a r t n e c h t i

w g v A d e F f o n o s i r a p m o C

|

1 e b a T

l

e m e h c s g n h c t a m

i

) s s e h t n e r a p

i

npj Digital Medicine|

(2024) 7:127

e s a e s d - I B C N

i

A B P L N J

D M E H C 4 C B

M G 2 C B

2 c 2 n 8 1 0 2

d o h t e M

l

e d o M

0 0 0 0 ± 3 7 9 0

.

.

(

1 0 0 0 ± 9 8 9 0

.

.

2 0 0 0 ± 9 3 9 0

.

.

(

1 0 0 0 ± 9 6 9 0

.

.

)

1 0 0 0 ± 8 6 9 0

.

(

1 0 0 0 ± 1 8 9 0

.

)

1 0 0 0 ± 8 2 9 0

.

.

(

1 0 0 0 ± 2 7 9 0

.

.

)

1 0 0 0 ± 2 2 8 0

.

.

(

2 0 0 0 ± 9 7 8 0

.

.

d e z

i l

a r t n e C

T R E B

8 0 0 0 ± 7 4 8 0

.

.

(

4 0 0 0 ± 7 1 9 0

.

.

3 0 0 0 ± 5 1 8 0

.

.

(

2 0 0 0 ± 5 0 9 0

.

.

)

2 0 0 0 ± 1 8 8 0

.

(

2 0 0 0 ± 1 2 9 0

.

)

3 0 0 0 ± 9 5 7 0

.

.

(

3 0 0 0 ± 8 8 8 0

.

.

)

7 0 0 0 ± 1 6 7 0

.

.

(

3 0 0 0 ± 8 2 8 0

.

.

)

g v a

(

e g n S

l

i

1 0 0 0 ± 9 4 9 0

.

.

(

1 0 0 0 ± 6 7 9 0

.

.

1 0 0 0 ± 6 9 8 0

.

.

(

1 0 0 0 ± 9 4 9 0

.

.

)

1 0 0 0 ± 4 5 9 0

.

(

0 0 0 0 ± 3 7 9 0

.

)

0 0 0 0 ± 7 9 8 0

.

.

(

1 0 0 0 ± 9 5 9 0

.

.

)

2 0 0 0 ± 7 1 8 0

.

.

(

2 0 0 0 ± 7 7 8 0

.

.

g v A d e F

9 0 0 0 ± 8 6 9 0

.

.

(

8 0 0 0 ± 7 8 9 0

.

.

3 0 0 0 ± 0 4 9 0

.

.

(

1 0 0 0 ± 9 6 9 0

.

.

)

7 0 0 0 ± 4 4 9 0

.

(

4 0 0 0 ± 5 6 9 0

.

)

2 0 0 0 ± 2 3 9 0

.

.

(

0 0 0 0 ± 5 7 9 0

.

.

)

7 0 0 0 ± 0 2 8 0

.

.

(

5 0 0 0 ± 9 7 8 0

.

.

d e z

i l

a r t n e C

T R E B e u B

l

9 0 0 0 ± 5 5 8 0

.

.

(

4 0 0 0 ± 5 2 9 0

.

.

3 0 0 0 ± 8 1 8 0

.

.

(

2 0 0 0 ± 8 0 9 0

.

.

)

4 0 0 0 ± 0 9 8 0

.

(

3 0 0 0 ± 7 2 9 0

.

)

4 0 0 0 ± 8 7 7 0

.

.

(

3 0 0 0 ± 6 0 9 0

.

.

)

7 4 0 0 ± 3 5 7 0

.

.

(

3 4 0 0 ± 3 2 8 0

.

.

)

g v a

(

e g n S

l

i

) 0 0 0 0 ± 3 6 9 0 ( 2 0 0 0 ± 4 8 9 0

.

.

.

.

1 0 0 0 ± 3 2 9 0

.

.

(

1 0 0 0 ± 3 6 9 0

.

.

) 0 0 0 0 ± 9 5 9 0 ( 0 0 0 0 ± 7 7 9 0

.

.

.

)

2 0 0 0 ± 9 1 9 0

.

.

(

1 0 0 0 ± 6 6 9 0

.

.

) 0 0 0 0 ± 7 1 8 0 ( 2 0 0 0 ± 6 7 8 0

.

.

.

.

g v A d e F

4 0 0 0 ± 4 4 9 0

.

.

(

2 0 0 0 ± 1 7 9 0

.

.

1 0 0 0 ± 4 2 9 0

.

.

(

0 0 0 0 ± 1 6 9 0

.

.

)

1 0 0 0 ± 4 3 9 0

.

(

1 0 0 0 ± 8 5 9 0

.

)

1 0 0 0 ± 6 6 8 0

.

.

(

1 0 0 0 ± 4 2 9 0

.

.

)

2 0 0 0 ± 3 8 7 0

.

.

(

2 0 0 0 ± 4 3 8 0

.

.

d e z

i l

a r t n e C

F R C - M T S L B

i

2 1 0 0 ± 9 8 5 0

.

.

(

0 1 0 0 ± 3 3 7 0

.

.

5 0 0 0 ± 0 7 6 0

.

.

(

2 0 0 0 ± 2 2 8 0

.

.

)

3 0 0 0 ± 3 7 6 0

.

(

2 0 0 0 ± 6 6 7 0

.

)

6 0 0 0 ± 5 1 4 0

.

.

(

6 0 0 0 ± 2 2 6 0

.

.

)

4 0 0 0 ± 3 6 6 0

.

.

(

4 0 0 0 ± 9 2 7 0

.

.

)

g v a

(

e g n S

l

i

5 3 0 0 ± 7 6 7 0

.

.

(

0 2 0 0 ± 5 6 8 0

.

.

4 0 0 0 ± 0 1 8 0

.

.

(

1 0 0 0 ± 2 0 9 0

.

.

)

2 0 0 0 ± 2 8 8 0

.

(

2 0 0 0 ± 0 2 9 0

.

)

3 1 0 0 ± 5 4 6 0

.

.

(

5 0 0 0 ± 3 9 7 0

.

.

)

3 0 0 0 ± 4 3 7 0

.

.

(

2 0 0 0 ± 2 8 7 0

.

.

g v A d e F

1 0 0 0 ± 5 7 9 0

.

.

(

1 0 0 0 ± 3 9 9 0

.

.

1 0 0 0 ± 3 4 9 0

.

.

(

0 0 0 0 ± 1 7 9 0

.

.

)

1 0 0 0 ± 2 7 9 0

.

(

1 0 0 0 ± 3 8 9 0

.

)

3 0 0 0 ± 7 3 9 0

.

.

(

0 0 0 0 ± 0 8 9 0

.

.

)

2 0 0 0 ± 3 2 8 0

.

.

(

2 0 0 0 ± 4 8 8 0

.

.

d e z

i l

a r t n e C

T R E B o B

i

6 0 0 0 ± 9 6 8 0

.

.

(

4 0 0 0 ± 6 3 9 0

.

.

3 0 0 0 ± 9 2 8 0

.

.

(

2 0 0 0 ± 5 1 9 0

.

.

)

2 0 0 0 ± 2 1 9 0

.

(

2 0 0 0 ± 4 4 9 0

.

)

2 0 0 0 ± 8 0 8 0

.

.

(

2 0 0 0 ± 1 3 9 0

.

.

)

7 0 0 0 ± 0 8 7 0

.

.

(

3 0 0 0 ± 5 4 8 0

.

.

)

g v a

(

e g n S

l

i

1 0 0 0 ± 8 5 9 0

.

.

(

2 0 0 0 ± 3 8 9 0

.

.

2 0 0 0 ± 0 1 9 0

.

.

(

1 0 0 0 ± 7 5 9 0

.

.

)

1 0 0 0 ± 3 6 9 0

.

(

0 0 0 0 ± 8 7 9 0

.

)

0 0 0 0 ± 2 2 9 0

.

.

(

1 0 0 0 ± 4 7 9 0

.

.

) 3 0 0 0 ± 8 1 8 0 ( 2 0 0 0 ± 9 7 8 0

.

.

.

.

g v A d e F

1 0 0 0 ± 5 7 9 0

.

.

(

1 0 0 0 ± 3 9 9 0

.

.

1 0 0 0 ± 1 4 9 0

.

.

(

1 0 0 0 ± 9 6 9 0

.

.

)

1 0 0 0 ± 7 6 9 0

.

(

1 0 0 0 ± 0 8 9 0

.

)

1 0 0 0 ± 3 3 9 0

.

.

(

1 0 0 0 ± 4 7 9 0

.

.

)

5 0 0 0 ± 7 2 8 0

.

.

(

6 0 0 0 ± 5 8 8 0

.

.

d e z

i l

a r t n e C

T R E B a c n

l

i

i l

c _ o B

i

8 0 0 0 ± 3 5 8 0

.

.

(

5 0 0 0 ± 2 2 9 0

.

.

3 0 0 0 ± 5 1 8 0

.

.

(

2 0 0 0 ± 5 0 9 0

.

.

)

2 0 0 0 ± 6 8 8 0

.

(

1 0 0 0 ± 4 2 9 0

.

)

4 0 0 0 ± 8 6 7 0

.

.

(

3 0 0 0 ± 8 9 8 0

.

.

)

7 0 0 0 ± 1 6 7 0

.

.

(

3 0 0 0 ± 8 2 8 0

.

.

)

g v a

(

e g n S

l

i

4 0 0 0 ± 8 5 9 0

.

.

(

3 0 0 0 ± 2 8 9 0

.

.

1 0 0 0 ± 1 0 9 0

.

.

(

0 0 0 0 ± 1 5 9 0

.

.

)

1 0 0 0 ± 3 5 9 0

.

(

1 0 0 0 ± 1 7 9 0

.

)

1 0 0 0 ± 1 0 9 0

.

.

(

2 0 0 0 ± 0 6 9 0

.

.

)

1 0 0 0 ± 5 1 8 0

.

.

(

1 0 0 0 ± 8 7 8 0

.

.

g v A d e F

2 0 0 0 ± 4 0 9 0

.

.

(

2 0 0 0 ± 8 2 9 0

.

.

1 0 0 0 ± 1 8 8 0

.

.

(

1 0 0 0 ± 5 2 9 0

.

.

)

2 0 0 0 ± 7 5 8 0

.

(

2 0 0 0 ± 9 7 8 0

.

)

1 0 0 0 ± 6 3 8 0

.

.

(

1 0 0 0 ± 1 9 8 0

.

.

)

1 0 0 0 ± 5 4 7 0

.

.

(

1 0 0 0 ± 1 0 8 0

.

.

d e z

i l

a r t n e C

2 - T P G

0 1 0 0 ± 0 9 6 0

.

.

(

4 0 0 0 ± 7 6 7 0

.

.

5 0 0 0 ± 2 7 6 0

.

.

(

4 0 0 0 ± 8 9 7 0

.

.

)

4 0 0 0 ± 7 8 6 0

.

(

3 0 0 0 ± 7 4 7 0

.

)

5 0 0 0 ± 4 5 5 0

.

.

(

5 0 0 0 ± 4 1 7 0

.

.

)

5 0 0 0 ± 1 8 6 0

.

.

(

5 0 0 0 ± 1 4 7 0

.

.

)

g v a

(

e g n S

l

i

2 0 0 0 ± 9 0 8 0

.

.

(

3 0 0 0 ± 2 5 8 0

.

.

1 0 0 0 ± 8 4 7 0

.

.

(

1 0 0 0 ± 4 4 8 0

.

.

)

0 0 0 0 ± 4 9 7 0

.

(

0 0 0 0 ± 5 2 8 0

.

)

6 0 0 0 ± 4 7 6 0

.

.

(

1 0 0 0 ± 6 9 7 0

.

.

) 1 0 0 0 ± 6 4 7 0 ( 3 0 0 0 ± 8 9 7 0

.

.

.

.

g v A d e F

. a s t n e m

i r e p x e d e t a e p e r e e r h t

r e v o n o i t a v e d d r a d n a t s d n a n a e m e h t

i

t n e s e r p e r

s e u a v d e t r o p e r e h T

l

. e r o c s e g a r e v a o r c a m e h t

t r o p e r e w

, s e i t i t n e e p i t l u m g n v o v n

l

i

l

s t e s a t a d r o F

.

d e n

i l r e d n u e r a s u p r o c h c a e r o f s e r o c s t s e h g h e h t d n a d e d o b e r a

i

l

l

e d o m e m a s e h t

f o g n n r a e

i

l

d e z

i l

a r t n e c e h t d e s s a p r u s

r o

) s a v r e t n

l

d e p p a l r e v o h t i

w

d e h c t a m

t a h t g v A d e F a

Article

3

https://doi.org/10.1038/s41746-024-01126-4

Article

Table 2 | Comparison of FedAvg with centralized learning and single-client learning on RE task measure by macro F1-score

Model

Method

2018 n2c2

EUADR

GAD

BERT

Centralized

0.947 ± 0.001

0.750 ± 0.040

0.738 ± 0.028

Single (avg)

0.892 ± 0.007

0.522 ± 0.111

0.642 ± 0.017

FedAvg

0.946 ± 0.002

0.527 ± 0.008

0.703 ± 0.021

BlueBERT

Centralized

0.950 ± 0.002

0.582 ± 0.109

0.755 ± 0.007

Single (avg)

0.898 ± 0.020

0.452 ± 0.039

0.616 ± 0.030

FedAvg

0.950 ± 0.002

0.548 ± 0.073

0.714 ± 0.018

BioBERT

Centralized

0.942 ± 0.002

0.737 ± 0.049

0.783 ± 0.007

Single (avg)

0.901 ± 0.006

0.525 ± 0.094

0.684 ± 0.015

FedAvg

0.942 ± 0.002

0.718 ± 0.037

0.750 ± 0.008

Bio_ClincialBERT Centralized

0.950 ± 0.001

0.741 ± 0.067

0.743 ± 0.014

Single (avg)

0.904 ± 0.006

0.514 ± 0.101

0.623 ± 0.018

FedAvg

0.946 ± 0.003

0.578 ± 0.057

0.695 ± 0.009

GPT-2

Centralized

0.951 ± 0.004

0.684 ± 0.097

0.709 ± 0.004

Single (avg)

0.899 ± 0.009

0.468 ± 0.105

0.630 ± 0.017

performanceusingcentralizedlearning,single-clientlearning,andfederated learning.Onalmostallthetasks,weshowedthatfederatedlearningachieved signiﬁcantimprovementcompared tosingle-client learningand oftentimes performed comparably to centralized learning without data sharing, demonstrating it as an effective approach for privacy-preserved learning withdistributeddata.TheonlyexceptionisinTable2,wherethebestsingle- clientlearningmodel(checkthestandarddeviation)outperformedFedAvg when using BERT and Bio_ClinicalBERT on EUADR datasets (theaverage performancewasstillleftbehind,though).Webelievethis isduetothelack of training data. As each client only owned 28 training sentences, the data distribution,althoughIID,washighlyunder-represented,makingithardfor FedAvg to ﬁnd the global optimal solutions. Surprisingly, FL achieved reasonablygoodperformanceevenwhenthetrainingdatawaslimited(284 total training sentences from all clients), conﬁrming that transfer learning from either the general text domain (e.g., BERT and GPT-2) or biomedical text domain (e.g., BlueBERT, BioBERT, Bio_ClinicalBERT) is beneﬁcial to thedownstreambiomedicalNLPtaskandpretrainingonmedicaldataoften gives afurther boost. Another interesting ﬁnding is thatGPT-2always gave inferiorresultscomparedtoBERT-basedmodels.Webelievethisisbecause GPT-2 is pre-trained on text generation tasks that only encode left-to-right attention for the next word prediction. However, this unidirectional nature prevents it from learning more about global context, which limits its ability to capture dependencies between words in a sentence.

FedAvg

0.946 ± 0.003

0.547 ± 0.086

0.721 ± 0.009

The reported values represent the mean and standard deviation over three repeated experimentsa. aFedAvg that matched (with overlapped intervals) or surpassed the centralized learning of the same model are bolded and the highest scores for each corpus are underlined.

In the sensitivity analysis of FL to client sizes, we found there is a monotonic trend that, with a ﬁxed number of training data, FL with fewer clients tends to perform better. For example, the classical BiLSTM-CRF model (20M), with a ﬁxed number of total training data, performs better withfewclients,butperformancedeteriorateswhenmoreclientsjoinin.Itis likely due to the increased learning complexity as FL models need to learn the inter-correlation of data across clients. Interestingly, the transformer- based model (≥108M), which is over 5 sizes larger compared to BiLSMT- CRF,ismoreresilienttothechangeoffederationscale,possiblyowingtoits increased learning capacity.

We analyzed the performance of FedProx in real-world non-IID sce- narios and compared it with FedAvg to study the behavior of different FL algorithms under data heterogeneity. Although the FedProx achieved slightly better performance than FedAvg when the data were non-IID dis- tributed, it is very sensitive to the hyper-parameter μ, which strikes to balance the local objective function and the proximal term. Speciﬁcally, when data was IID, and μ was set to a large value (e.g., μ=1), FedProx yielded a 2.4% lower lenient F1-score compared to FedAvg. When the data were non-IID, this performance gap further widened to 5.4%. It is also noteworthythatwhenμissetto0,andalltheclientsareforcedtoperforman equal number of local updates, FedProx essentially reverts to FedAvg.

Fig. 1 | Performance of FL models with varying numbers of clients. We tested models on 2018 n2c2 (NER) and evaluated them using the F1 score with lenient matching scheme.

We also investigated the impact of model size on the performance of FL. We observed that as the model size increased, the performance gap between centralized models and FL models narrowed. Interestingly, Bio- BERT, which shares the same model architecture and is similar in size to

Table 3 | Comparison of FedAvg with centralized learning and single-client learning using BioBERT

Method

µ

IID (2018 n2c2)

non-IID (BC2GM & JNLPBAS)

lenient

strict

lenient

strict

Centralized

–

0.884 ± 0.002

0.823 ± 0.002

0.964 ± 0.001

0.929 ± 0.000

FedAvg

–

0.879 ± 0.002

0.818 ± 0.003

0.934 ± 0.003

0.884 ± 0.003

FedProx

1

0.855 ± 0.003

0.790 ± 0.005

0.880 ± 0.001

0.772 ± 0.002

0.5

0.868 ± 0.001

0.809 ± 0.002

0.881 ± 0.002

0.777 ± 0.001

0.1

0.872 ± 0.003

0.814 ± 0.004

0.897 ± 0.002

0.817 ± 0.002

0.01

0.878 ± 0.003

0.819 ± 0.002

0.933 ± 0.002

0.884 ± 0.003

0.001

0.880 ± 0.002

0.820 ± 0.001

0.944 ± 0.002

0.901 ± 0.002

We select the value of μ (a hyper-parameter in FedProx) as suggested by the FedProx paper. The reported values represent the mean and standard deviation over three repeated experimentsa. aFedAvg that matched (with overlapped intervals) or surpassed the centralized learning of the same model are bolded and the highest scores for each corpus are underlined.

npj Digital Medicine|

(2024) 7:127

4

https://doi.org/10.1038/s41746-024-01126-4

Fig. 2 | Comparison of model performance with different sizes, measured by the number of train- ableparametersontheBC2GMdataset.Thesizeof the circle tells the number of model parameters, while the color indicates different learning methods. The x-axis represents the mean test F1-score with thelenientmatch(resultsareadaptedfromTable1).

Fig. 3 | Comparison of LLMs using few-shot prompting and small LMs (BlueBERT and GPT- 2) trained with FLon NER (upper) andRE (lower) tasks evaluated based on the F1-score (lenient matching for NER tasks). A complete evaluation, including the strict matching and running time analysis,canbefoundinSupplementaryTable1and Supplementary Table 2.

BERT and Bio_ClinicalBERT, performs comparably tolarger models (such as BlueBERT), highlighting the importance of pre-training for model per- formance.Overall,thesizeofthemodelisindicativeofitslearningcapacity; large models tend to perform better than smaller ones. However, large models require longer training time and more computation resources, which results in a natural trade-off between accuracy and efﬁciency.

Compared with LLMs, FL models were the clear winner regarding prediction accuracy. We hypothesize that LLMs are mostly pre-trained on the general text and may not guarantee performance when applied to the biomedical text data due to the domain disparity. As LLMs with few-shot promptingonlyreceivedlimitedinputs fromthetargettasks,theyarelikely to perform worse than models trained using FL, which are built with suf- ﬁcient training data. To close the gap, specialized LLMs pre-trained on medicaltextdata33ormodelﬁne-tuning34canbeusedtofurtherimprovethe LLMs’ performance. Another interesting fact is that with more input examples (e.g., 10-shot and 20-shot), LLMs often demonstrate increased prediction performance, which is intuitive as LLMs receive more knowl- edge, and the performance should be increased accordingly.

While seeing many promising results of FL for LMs, we acknowledge our study suffers from the following limitations: (1) most of our experi- ments, excluding the non-IID study, are conducted in a simulated envir- onment with synthetic data split, which may not perfectly align with the distribution patterns of real-world FL data. (2) we mostly focused on hor- izontalFLbuthavenotextendedtoverticalFL35.(3)wehavenotconsidered FL combined with privacy techniques such as differential privacy36 and homomorphic encryption37. To address these limitations and further advanceourunderstandingofFLforLMs,ourfuturestudywillfocusonthe real-world implementation of FL and explore the practical opportunities

npj Digital Medicine|

(2024) 7:127

Article

and challenges in FL, such as vertical FL and FL combined privacy tech- niques. We believe our study will offer comprehensive insights into the potential of FL for LMs, which can serve as a catalyst for future research to develop more effective AI systems by leveraging distributed clinical data in real-world scenarios.

Methods NLP tasks and corpora We compared FL with alternative training schemes on 8 biomedical NLP datasetswithafocusontwoNLPtasks:NER(5corpora)andRE(3corpora). The NER and RE are two established tasks for information extraction in biomedical NLP. Given an input sequence of tokens, the goal of NER is to identify and classify the named entities, such as diseases and genes, present in the sequence. RE is often the follow-up task that aims to discover the relations between pairs of named entities. For example, a gene-disease relation (BRCA1-breast cancer) can be identiﬁed in a sentence: “Mutations ofBRCA1geneareassociatedwithbreastcancer”.ForREtasks,wetakethe entity positions as given and formulate the problem as follows: given a sentence and the spans of two entities, the task is to determine the rela- tionship between the two entities.

We select the corpora using the following protocols: (1) Publicity. The corpora should be publicly available to ensure that the results obtained are reproducible. (2) Popularity. The corpora should be used in other well-cited papers so that the quality of the data is ensured. (3) Diversity. The corpora should represent as many as the real-world bio- medical NLP tasks. A summary of the selected datasets can be found in Table 4; we defer to Supplementary Methods for more detailed descrip- tions of each dataset.

5

https://doi.org/10.1038/s41746-024-01126-4

Article

Table 4 | List of corpora and their statistics

Corpus

Entity/ Relation Type

Corpora type

year

Task

Train

Dev

Test

2018 n2c241

8 entities1

discharge summaries

2018

NER

48727

6091

6091

BC2GM42

gene

Medline abstract

2008

NER

26006

3251

3251

BC4CHEMD43

drug/chem

PubMed abstract

2015

NER

94170

11772

11771

JNLPBA44

gene

GENIA version 3.02 corpus

2003

NER

29559

3695

3695

NCBI-disease45

disease

PubMed abstract

2014

NER

10125

1266

1266

2018 n2c241

disease

discharge summaries

2018

RE

72786

9099

9098

EUADR46

gene-disease

Medline abstracts

2012

RE

284

36

35

GAD21

gene-disease

genetic association studies

2004

RE

4097

513

512

The data splits are counted based on the number of sentences. 1A total of 8 entities are considered including reason, frequency, ADE, strength, duration, route, form, and dosage. Details about the 2018 n2c2 dataset can be found in Supplementary materials.

Federated learning algorithms FL represents a family of algorithms that aims to train models in a dis- tributedenvironmentinacollaborativemanner.Considerascenariowhere ;:::;Dkg, where there are K clients with distributed data D ¼ fD1 Di ¼ DXi , and Xi and Yi are the input and output space, respectively. The typical FL aims to solve the optimization problem as in Eq. (1)

;D2

×Yi

Algorithm 1. Federated learning algorithms (FedAvg/FedProx)

Notation:Xi indicatesdatafromclienti,Kisthetotalnumberofclients, T is the maximum training round, n is the sum of n1 to nk, pi is the weights for the ith client

Initialize server model weights w(1) Initialize client model weights wi 8i ¼ 1;2;...;K For each round t=1, 2, … T do

X K

i¼1

PiFi wð

ÞwhereFk ¼

X

Dkj j j¼1

(cid:2) Lw Xj

;Yj

(cid:3)

;

where w denote the weights of the model being learned, Fi is the local objective of the ith clients, and pi is the weight of the ith clients such that K i¼1pi ¼ 1.Theweightsareusually determinedbythequantity pi >0 and of clients’ training samples. For example, it equals 1 K when clients share the same amount of training data.

P

In an FL game, there are two types of players: server and client. The server is the compass that navigates the whole process of FL including signaling the start and end of federated learning, synchronizing the local model updates, and dispatching the updated models. The clients are responsibleforfetchingmodelsfromtheserver,updatingmodelsusingtheir local data, and sending the updated models back to the server.

Throughout the whole process, there are four steps: (1) the clients use their own data to optimize the local objectives—local updates, (2) local clients upload the updated model or gradients to the server, (3) the server acquires the local models and synchronize the updates—model aggrega- tion, and (4) server dispatch the models to the clients. While different FL algorithms may have specialized designs for local updates or model aggre- gation, they share the same training paradigm.

ð1Þ

Send server model weight wðtÞ to each client For each client k ¼ 1;2;...;K do Client k perform LocalUpdate ðXk End for w t þ 1

;Yk

;wkÞ ← Algorithm 2

P K i¼1 piwi

← model aggregation

ð End for

Þ ¼

Algorithm 2. Local model training using mini-batch stochastic gradient descent (LocalUpdate) (FedAvg/FedProx)

Notation:Risthelocalupdateround,Bisthenumberofbatches,f wr is theneuralnetworkparameterizedbywr,ηisthelearningrate,μisthehyper- parameter in FedProx

Foreachroundr ¼ 1;2;...;R do/Repeatuntilﬁndtheapproximate

μ

minimizer of w≈argminwLðf wr ðXbÞ;YbÞ þ shufﬂe Xk ;YBÞÞ ;Y2Þ;...;ðXB ches ððX1 ðXbÞ;YbÞ þ 2jjwk(cid:2)wk tð Þjj2 Lwr For each mini-batch b ¼ 1;2;...;B do wrþ1 ¼ wr (cid:2) η∇Lwr

2jjwk (cid:2) wk tð Þjj2 and

Randomly ;Y1Þ;ðX2 ¼ Lðf wr

create

B

μ

;YbÞ

ðXb

End for

bat-

We considered the two most popular FL algorithms called Federated Averaging (FedAvg)30 and another variant FedProx31. FedAvg is the most basicand standard FL algorithm thatuses stochasticgradientdescent (SGD) to progressively update the local model. More speciﬁcally, each client locally takesaﬁxednumberofgradientdescentstepsontheirlocalmodelusingtheir local training data. On another hand, the server will aggregate these local modelsbytakingtheweightedaverageastheresultingnewmodelforthenext round. However, in FedAvg, the number of local updates can be determined by the size of the data. When the size of the data varies, the local updates performed locally can be signiﬁcantly different. FedProx was introduced to tackle the issue of heterogeneous local updates in FedAvg. By adding a proximaltermtotheobjectiveofthelocalupdate,theimpactofvariablelocal updatesissuppressed.Morespeciﬁcally,atiterationt,theinnerlocalupdates aretryingtoﬁndthesolutionthatminimizestheobjective,asshowninEq.(2)

Minw

1 nk

X

nk i¼1

(cid:4) Lw Xi

;Yi

(cid:5)

þ

μ

2

(cid:6) (cid:6)

(cid:6) (cid:6)

w (cid:2) wt

(cid:6) (cid:6)

(cid:6) (cid:6);

where wt is the weights of the network from iteration t. A comparison of FedAvg and FedProx can be found in Algorithm 1 and Algorithm 2.

ð2Þ

Study design As shown in Fig. 4, we explored three learning methods: (1) federated learning, centralized learning, and single-client learning. To simulate the conventional learning scenario, we varied the data scale and conducted the following experiments: centralizing all client data to train a single model (centralized learning) and training separate models on each client’s local data (single-client learning).

Models. To better understand the effect of LMs on FL, we chose models with various sizes of parameters from 20 M to 334 M, including Bidir- ectional Encoder Representations from Transformer (BERT)1, and Generative Pre-trained Transformer (GPT)38, as well as classical RNN- based model like BiLSTM-CRF39. BERT-based models utilize a trans- former encoder and incorporate bi-directional information acquired through two unsupervised tasks as a pre-training step into its encoder. Different BERT models differ in their pre-training source dataset and model size, deriving many variants such as BlueBERT12, BioBERT8, and Bio_ClinicBERT40. BiLSTM-CRF is the only model in our study that is not built upon transformers. It is a bi-directional model designed to handle long-term dependencies, is used to be popular for NER, and uses

npj Digital Medicine|

(2024) 7:127

6

https://doi.org/10.1038/s41746-024-01126-4

Fig. 4 | A comparison of centralized learning, federated learning, and single-clientlearning. The arrows indicate the data ﬂow through the model training process.

Table 5 | List of LMs used for comparison

Model

Param

Backbone

BiLSTM-CRF39

20 M

LSTM

BERT1

109 M

Transformer encoder

BlueBERT12

334 M

Transformer encoder

BioBERT8

108 M

Transformer encoder

Bio_ClinicalBERT9

108 M

Transformer encoder

GPT-238

124 M

Transformer decoder

GPT-447

–

Transformer decoder

PaLM 248

–

Transformer

Gemini49

–

Transformer decoder

Fig. 5 | An example of applying few-shot prompting in an LLM to solve an NER task. We formulated the prompt to include a description of thetask,afewexamplesofinputs(i.e.,rawtexts)and outputs (i.e., annotated texts), and a query text at the end.

LSTM as its backbone. We selected this model in the interest of inves- tigating the effect of federation learning on models with smaller sets of parameters. For LLMs,weselected GPT-4, PaLM2(Bisonand Unicorn), and Gemini (Pro) for assessment as both can be publicly accessible for inference. A summary of the model can be found in Table 5, and details on the model description can be found in Supplementary Methods.

Training details Datapreprocessing.weadaptedmostofthedatasetsfromtheBioBERT paper with reasonable modiﬁcations by removing the duplicate entries and splitting the data into the non-overlapped train (80%), dev (10%), and test (10%) datasets. The maximum token limit was set at 512, with truncation—codedsentenceswithlengthslargerthan512weretrimmed.

npj Digital Medicine|

(2024) 7:127

Article

Pre-trained source

Year

–

2015

Wikipedia + BooksCorpus

2018

PubMed

2019

Wikipedia + BooksCorpus + PubMed + PMC

2020

Clinical notes

2019

Wikipedia +news+books

2019

–

2023

Web documents, books, code, mathematics, and conversational data

2023

Web documents, books, code, images, audio, and video data

2023

Federated learning simulation. We considered two different learning settings: learning from IID data and learning from non-IID data. For the ﬁrstsetting,werandomlysplitthedataintokfoldsuniformly.Formostof ourexperiments,kwaschosenas10,whilewealsovariedkfrom2to10to study the impact of the size of the federation. For the second setting, we considered learning from heterogeneous data collected from different sources. This represents the real-world scenario where complex and entangled heterogeneities are co-existed. We picked BC2GM and JNLPBA as two independent clients, both targeting the same gene entity recognition tasks but were collected from different sources. To show that they are non-IID distributed, we have conducted data distribution ana- lysis(i.e.,calculatethedistributiondistanceandplott-SNEonembedded features space), which can be found in Supplementary Discussions.

7

https://doi.org/10.1038/s41746-024-01126-4

LLMs with few-shot prompting. We followed a similar experiment protocolasinthepreviousstudy32.Figure5showsanexampleofapplying few-shot prompting in a LLM to solve an NER task. A RE task can be solvedsimilarlybychangingthetaskdescription,andinput-outputpairs. Notably, we simulate 1-/5-/10-/20-shot prompting by varying the number of input examples that are randomly selected from the training dataset. For model evaluation, we randomly selected 200 test samples in thetestdatasetandreportedthepredictionperformanceovertheselected samples.

Training models. For models that require training, we used Adam to optimizeourmodelswithaninitiallearningrateof0.001andmomentum linear_- rate was of scheduler_with_warmup. All experiments were performed on a system equipped with an NVIDIA A100 GPU and an AMD EPYC 7763 64-core Processor.

0.9.

The

learning

scheduled

by

Reported evaluation. For NER, we reported the performance of these metrics at the macro average level with both strict and lenient match criteria. Strict match considers the true positive when the boundary of entities exactly matches with the gold standard, while lenient considers true positives when the boundary of entities overlaps between model outputs and the gold standard. For all tasks, we repeated the experiments three times and reported the mean and standard deviation to account for randomness.

Reporting summary Further information on research design is available in the Nature Research Reporting Summary linked to this article.

Data availability All the datasets involved in this study are publicly available from the fol- lowing ofﬁcial websites: 2018 n2c2: https://portal.dbmi.hms.harvard.edu/ projects/n2c2-nlp/. BC2GM: https://biocreative.bioinformatics.udel.edu/ https://biocreative.bioinformatics.udel.edu/ tasks/. http://www. JNLPBA: resources/biocreative-iv/chemdner-corpus/. geniaproject.org/shared-tasks/bionlp-jnlpba-shared-task-2004. NCBI-dis- ease: https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/. EUADR: https://biosemantics.erasmusmc.nl/index.php/resources/euadr- corpus. GAD: https://maayanlab.cloud/Harmonizome/dataset/GAD +Gene-Disease+Associations.

BC4CHEMD:

Code availability Our project codes are publicly available on Github: Train and evaluate FL models: https://github.com/PL97/FedNLP. Texts preprocessing: https:// github.com/PL97/Brat2BIO. Evaluation: https://github.com/PL97/NER_ eval. LLMs evaluations: https://github.com/GaoxiangLuo/LLM-BioMed- NER-RE.

References 1. Devlin,J.etal.“BERT:Pre-trainingofDeepBidirectionalTransformers for Language Understanding.” North American Chapter of the Association for Computational Linguistics 4171–4186 (2019). 2. Radford, A., Narasimhan, K., Salimans, T. & Sutskever, I. Improving language understanding by generative pre-training. Preprint at arXiv https://arxiv.org/pdf/2012.11747 (2010).. Sun, C. et al. “How to Fine-Tune BERT for Text Classiﬁcation?” China National Conference on Chinese Computational Linguistics (2019). Xu,H.et al.“BERTPost-Trainingfor ReviewReadingComprehension and Aspect-based Sentiment Analysis.” North American Chapter of the Association for Computational Linguistics (2019).

3.

4.

npj Digital Medicine|

(2024) 7:127

Article

5. Dathathri, S. et al. Plug and play language models: a simple approach

6.

7.

8.

to controlled text generation. Findings of the Association for Computational Linguistics: EMNLP pp. 3973–3997 (2021). Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q. & Artzi, Y. BERTScore: evaluating text generation with BERT. International Conference on Learning Representations (2020). Shi, P. & Lin, J. Simple BERT models for relation extraction and semantic role labeling. Preprint at arXiv http://arxiv.org/abs/1904. 05255 (2019). Lee, J. et al. BioBERT: a pre-trained biomedical language representation model for biomedical text mining. Bioinformatics 36, 1234–1240 (2020).

9. Huang, K., Altosaar, J. & Ranganath, R. ClinicalBERT: modeling

clinical notes and predicting hospital readmission. Preprint at arXiv https://doi.org/10.48550/arXiv.1904.05342 (2020).

10. Yang, W. et al. End-to-end open-domain question answering with

BERTserini. In Proceedings of the 2019 Conference of the North 72–77. https://doi.org/10.18653/v1/N19-4013 (2019).

11. Qu, C. et al. BERT with history answer embedding for conversational

question answering. In Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval 1133–1136 (ACM, 2019). https://doi.org/10.1145/3331184. 3331341.

12. Peng, Y. et al. “Transfer Learning in Biomedical Natural Language Processing: An Evaluation of BERT and ELMo on Ten Benchmarking Datasets.” Proceedings of the 2019 Workshop on Biomedical Natural Language Processing (2019).

13. Tinn,R.etal.Fine-tuninglargeneurallanguagemodelsforbiomedical

natural language processing. Patterns 4, 100729 (2023).

14. A Study of Abbreviations in Clinical Notes—PMC. https://www.ncbi. nlm.nih.gov/pmc/articles/PMC2655910/.

15. Reisman, M. EHRs: the challenge of making electronic data usable and interoperable. Pharm. Ther. 42, 572–575 (2017).

16. Zhou, S., Wang, N., Wang, L., Liu, H. & Zhang, R. CancerBERT: a cancer domain-speciﬁc language model for extracting breast cancer phenotypes from electronic health records. J. Am. Med. Inform. Assoc. JAMIA 29, 1208–1216 (2022).

17. Gu, Y. et al. Domain-speciﬁc language model pretraining for biomedical natural language processing. ACM Trans. Comput. Healthc. 3, 1–23 (2022).

18. Johnson, A. E. W. et al. MIMIC-III, a freely accessible critical care

database. Sci. Data 3, 160035 (2016).

19. Lafferty, J. D., McCallum, A. & Pereira, F. C. N. Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data. In Proceedings of the Eighteenth International Conference on MachineLearning282–289(MorganKaufmannPublishersInc.,2001).

20. Hochreiter, S. & Schmidhuber, J. Long short-term memory. Neural Comput. 9, 1735–1780 (1997).

21. The genetic association database—PubMed. https://pubmed.ncbi. nlm.nih.gov/15118671/.

21. The genetic association database—PubMed. https://pubmed.ncbi. nlm.nih.gov/15118671/.

22. Konečný, J. et al. Federated learning: strategies for improving communication efﬁciency. NIPS Workshop on Private Multi-Party Machine Learning (2016).

23. Peng,L.etal.EvaluationoffederatedlearningvariationsforCOVID-19

diagnosis using chest radiographs from 42 US and European hospitals. J. Am. Med. Inform. Assoc. 30, 54–63 (2023).

24. Long, G, et al. "Federated learning for open banking." Federated Learning: Privacy and Incentive 240–254 (2020).

25. Nguyen,A. et al. “Deep FederatedLearning for Autonomous Driving.” 2022 IEEE Intelligent Vehicles Symposium (IV), 1824–1830 (2021). 26. Liu, M.et al.Federatedlearningmeetsnaturallanguageprocessing:a survey. Preprint at arXiv http://arxiv.org/abs/2107.12603 (2021). 27. Lin, B.Y. et al. “FedNLP:Benchmarking FederatedLearningMethods for Natural Language Processing Tasks.” NAACL-HLT (2021).

8

https://doi.org/10.1038/s41746-024-01126-4

28. Sui, D. et al. FedED: federated learning via ensemble distillation for

medicalrelationextraction.InProceedingsofthe2020Conferenceon Empirical Methods in Natural Language Processing (EMNLP) 2118–2128 (Association for Computational Linguistics, 2020) https:// doi.org/10.18653/v1/2020.emnlp-main.165.

29. Liu, D. & Miller,T. Federatedpretrainingandﬁnetuningof BERTusing clinicalnotesfrommultiplesilos.PreprintatarXivhttp://arxiv.org/abs/ 2002.08562 (2020).

30. McMahan, B., Moore, E., Ramage, D., Hampson, S. & Arcas, B. A. Y. Communication-efﬁcient learning of deep networks from decentralized data. In Proceedings of the 20th International Conference on Artiﬁcial Intelligence and Statistics 1273–1282 (PMLR, 2017).

31. Li, T. et al. "Federated optimization in heterogeneous networks." Proceedings of Machine Learning and Systems 2, 429–450 (2020). 32. Chen,Q.etal."Largelanguagemodelsinbiomedicalnaturallanguage processing:benchmarks,baselines,andrecommendations."Preprint at arXiv https://arxiv.org/pdf/2305.16326 (2023).

33. Yang, X. et al. A large language model for electronic health records. Npj Digit. Med. 5, 1–9 (2022).

34. Large language models encode clinical knowledge. Nature. https://

www.nature.com/articles/s41586-023-06291-2.

35. Yang, Q., Liu, Y., Chen, T. & Tong, Y. Federated machine learning: concept and applications. ACM Trans. Intell. Syst. Technol. 10, 1–19 (2019).

36. Federated Learning With Differential Privacy: Algorithms and

Performance Analysis. IEEE J. Mag. https://ieeexplore.ieee.org/ document/9069945.

37. Zhang, C. et al. “BatchCrypt: Efﬁcient Homomorphic Encryption for Cross-Silo Federated Learning.” USENIX Annual Technical Conference (2020).

38. Radford, A. et al. "Language models are unsupervised multitask

39.

learners." OpenAI blog 1.8 9 (2019). [1508.01991]BidirectionalLSTM-CRFModelsforSequenceTagging. https://arxiv.org/abs/1508.01991.

40. Alsentzer, E. et al. Publicly available clinical BERT embeddings.

Preprint at arXiv http://arxiv.org/abs/1904.03323 (2019).

41. Henry, S., Buchan, K., Filannino, M., Stubbs, A. & Uzuner, O. 2018

n2c2sharedtaskonadversedrugeventsandmedicationextractionin electronic healthrecords. J. Am.Med.Inform.Assoc.27, 3–12(2020). 42. Smith, L. et al. Overview of BioCreative II gene mention recognition.

Genome Biol. 9, S2 (2008).

43. Krallinger, M. et al. The CHEMDNER corpus of chemicals and drugs and its annotation principles. J. Cheminformatics 7, S2 (2015). 44. Collier, N., Ohta, T., Tsuruoka, Y., Tateisi, Y. & Kim, J.-D. Introduction to the bio-entity recognition task at JNLPBA. In Proceedings of the International Joint Workshop on Natural Language Processing in Biomedicine and its Applications (NLPBA/BioNLP) 73–78 (COLING, 2004).

45. Doğan, R. I., Leaman, R. & Lu, Z. NCBI disease corpus: a resource for disease name recognition and concept normalization. J. Biomed. Inform. 47, 1–10 (2014).

46. van Mulligen, E. M. et al. The EU-ADR corpus: annotated drugs, diseases, targets, and their relationships. J. Biomed. Inform. 45, 879–884 (2012).

npj Digital Medicine|

(2024) 7:127

Article

47. OpenAI. GPT-4 Technical Report. Preprint at arXiv http://arxiv.org/

abs/2303.08774 (2023).

48. Anil, R. et al. PaLM 2 Technical Report. Preprint at arXiv https://doi.

org/10.48550/arXiv.2305.10403 (2023).

49. Gemini Team et al. Gemini: a family of highly capable multimodal models. Preprint at arXiv http://arxiv.org/abs/2312.11805 (2023).

Acknowledgements This work was in part supported by Cisco Research under award number 1085646POUSA000EP390223and the National Cancer Institutewithinthe NationalInstitutionsofHealthunderawardnumber1R01CA287413-01.The authors acknowledge the Minnesota Supercomputing Institute (MSI) at the University of Minnesota for providing resources that contributed to the researchresultsreportedinthispaper. Thestudywasalsosupportedbythe UMN’s Center for Learning Health System Sciences.

Author contributions L.P. was responsible for the overall experimental design, F.L. implementation, and writing of the paper. G.L. was responsible for the LLM prompt design, LLM experiment, evaluation, and editing of the paper. S.Z. andR.Z.contributedtothedatacollectionandeditingofthepaper.J.C.,Z.X. and J.S. contributed to the editing of the paper and idea discussion.

Competing interests The authors declare no competing interests.

Additional information Supplementary information The online version contains supplementary material available at https://doi.org/10.1038/s41746-024-01126-4.

CorrespondenceandrequestsformaterialsshouldbeaddressedtoJuSun or Rui Zhang.

Reprints and permissions information is available at http://www.nature.com/reprints

Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional afﬁliations.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distributionand reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’sCreativeCommonslicenceandyourintendeduseis notpermitted by statutory regulation or exceeds the permitted use, you will need to obtainpermissiondirectly fromthe copyrightholder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.

© The Author(s) 2024

9