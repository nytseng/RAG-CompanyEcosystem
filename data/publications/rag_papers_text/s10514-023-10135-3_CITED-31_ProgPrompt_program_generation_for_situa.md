Autonomous Robots (2023) 47:999–1012 https://doi.org/10.1007/s10514-023-10135-3

PROGPROMPT: program generation for situated robot task planning using large language models

Ishika Singh1 · Valts Blukis2 · Arsalan Mousavian2 · Ankit Goyal2 · Danfei Xu2 · Jonathan Tremblay2 · Dieter Fox2,3 · Jesse Thomason1 · Animesh Garg2,4

Received: 1 May 2023 / Accepted: 3 August 2023 / Published online: 28 August 2023 © The Author(s) 2023

Abstract Task planning can require deﬁning myriad domain knowledge about the world in which a robot needs to act. To ameliorate that effort, large language models (LLMs) can be used to score potential next actions during task planning, and even generate action sequences directly, given an instruction in natural language with no additional domain information. However, such methods either require enumerating all possible next steps for scoring, or generate free-form text that may contain actions not possible on a given robot in its current context. We present a programmatic LLM prompt structure that enables plan generation functional across situated environments, robot capabilities, and tasks. Our key insight is to prompt the LLM with program-like speciﬁcations of the available actions and objects in an environment, as well as with example programs that can be executed. We make concrete recommendations about prompt structure and generation constraints through ablation experiments, demonstrate state of the art success rates in VirtualHome household tasks, and deploy our method on a physical robot arm for tabletop tasks. Website and code at progprompt.github.io

Keywords Robot task planning · LLM code generation · Planning domain generalization · Symbolic planning

1 Introduction

B Ishika Singh

ishikasi@usc.edu

Valts Blukis vblukis@nvidia.com

Arsalan Mousavian amousavian@nvidia.com

Ankit Goyal angoyal@nvidia.com

Danfei Xu danfeix@nvidia.com

Jonathan Tremblay jtremblay@nvidia.com

Everyday householdtasksrequireboth commonsenseunder- standing of the world and situated knowledge about the current environment. To create a task plan for “Make din- ner,” an agent needs common sense: object affordances, such as that the stove and microwave can be used for heating; logical sequences of actions, such as an oven must be pre- heated before food is added; and task relevance of objects and actions, such as heating and food are actions related to “dinner” in the ﬁrst place. However, this reasoning is infea- sible without state feedback. The agent needs to know what food is available in the current environment, such as whether the freezer contains ﬁsh or the fridge contains chicken.

Dieter Fox dieterf@nvidia.com

Jesse Thomason jessetho@usc.edu

Autoregressive large language models (LLMs) trained on large corpora to generate text sequences conditioned on input prompts have remarkable multi-task generalization. This ability has recently been leveraged to generate plau-

Animesh Garg animeshg@nvidia.com

3 Computer Science and Engineering, University of

1 Computer Science, University of Southern California, Los

Washington, Seattle, WA 98195, USA

2

Angeles, CA 90089, USA

Seattle Robotics Lab, NVIDIA, Seattle, WA 98105, USA

4

School of Interactive Computing, Georgia Institute of Technology, Atlanta, GA 30308, USA

123

1000

Fig. 1 ProgPrompt leverages LLMs’ strengths in both world knowl- edge and programming language understanding to generate situated task plans that can be directly executed

sible action plans in context of robotic task planning (Ahn et al., 2022; Huang et al., 2022b,a; Zeng et al., 2022) by either scoringnextstepsorgeneratingnewstepsdirectly.Inscoring mode,theLLMevaluatesanenumerationofactionsandtheir arguments from the space of what’s possible. For instance, given a goal to “Make dinner” with ﬁrst action being “open the fridge”, the LLM could score a list of possible actions: “pick up the chicken”, “pick up the soda”, “close the fridge”, ..., “turn on the lightswitch.” In text-generation mode, the LLM can produce the next few words, which then need to be mapped to actions and world objects available to the agent. For example, if the LLM produced “reach in and pick up the jar of pickles,” that string would have to neatly map to an executable action like “pick up jar.” A key component missing in LLM-based task planning is state feedback from the environment. The fridge in the house might not contain chicken, soda, or pickles, but a high-level instruction “Make dinner” doesn’t give us that world state information. Our workintroducessituated-awarenessinLLM-basedrobot task planning.

We introduce ProgPrompt, a prompting scheme that goes beyond conditioning LLMs in natural language. Prog- Prompt utilizes programming language structures, leverag- ing the fact that LLMs are trained on vast web corpora that includes many programming tutorials and code documen- tation (Fig. 1). ProgPrompt provides an LLM a Pythonic program header with an import statement for available actions and their expected parameters, a list of environ- ment objects, and function deﬁnitions like make_dinner whose bodies are sequences of actions operating on objects. We incorporate situated state feedback from the environment by asserting preconditions of our plan, such as being close to the fridge before attempting to open it, and responding to failed assertions with recovery actions. What’s more, we

123

Autonomous Robots (2023) 47:999–1012

show that including natural language comments in Prog- Promptprograms toexplain thegoal oftheupcoming action improves task success of generated plan programs.

2 Background and related work

2.1 Task planning

For high-level planning, most works in robotics use search in a pre-deﬁned domain (Fikes and Nilsson, 1971; Jiang et al., 2018; Garrett et al., 2020). Unconditional search can be hard to scale in environments with many feasible actions and objects (Puig et al., 2018; Shridhar et al., 2020) due to large branching factors. Heuristics are often used to guide the search (Baier et al., 2007; Hoffmann, 2001; Helmert, 2006; Bryce and Kambhampati, 2007). Recent works have exploredlearning-basedtask&motionplanning,usingmeth- ods such as representation learning, hierarchical learning, language as planning space, learning compositional skills and more(Akakzia et al.,2021; Eysenbach et al.,2019; Jiang et al., 2019; Kurutach et al., 2018; Mirchandani et al., 2021; Nair and Finn, 2020; Shah et al., 2022; Sharma et al., 2022; Silveretal.,2022;Srinivasetal.,2018;Xuetal.,2018, 2019; Zhu et al., 2020). Our method sidesteps search to directly generateaplanthatincludesconditionalreasoninganderror- correction.

Weformulatetaskplanningasthetuple(cid:2)O,P,A,T ,I,G, t(cid:3).O isasetofalltheobjectsavailableintheenvironment, P is a set of properties of the objects which also informs object affordances, A is a set of executable actions that changes depending on the current environment state deﬁned as s ∈ S. A state s is a speciﬁc assignment of all object properties, and S is a set of all possible assignments. T represents the tran- sition model T : S × A → S, I and G are the initial and goal states. The agent does not have access to the goal state g ∈ G, but only a high-level task description t.

Consider the task t = “microwave salmon”. Task rele- vant objects microwave, salmon ∈ O will have properties modiﬁed during action execution. For example, action a = open(microwave) will change the state from closed (microwave) ∈ s to ¬closed(microwave) ∈ s(cid:6) if a is admissible, i.e., ∃(a,s,s(cid:6)) s.t. a ∈ A∧s,s(cid:6) ∈ S ∧T (s,a) = s(cid:6). In this example a goal state g ∈ G could contain the con- ditions heated(salmon) ∈ g, ¬closed(microwave) ∈ g and ¬switchedOn(microwave) ∈ g.

2.2 Planning with LLMs

A Large Language Model (LLM) is a neural network with many parameters—currently hundreds of billions (Brown et al., 2020; Chen et al., 2021)—trained on unsupervised learning objectives such as next-token prediction or masked-

Autonomous Robots (2023) 47:999–1012

language modelling. An autoregressive LLM is trained with a maximum likelihood loss to model the probability of a sequence of tokens y conditioned on an input sequence x, i.e. θ = argmaxθ P(y|x;θ), where θ are model param- eters. The trained LLM is then used for prediction ˆy = argmaxy∈S P(y|x;θ),whereSisthesetofalltextsequences. Since search space S is huge, approximate decoding strate- gies are used for tractability (Holtzman et al., 2020; Luong et al., 2015; Wiseman et al., 2017).

LLMs are trained on large text corpora, and exhibit multi- task generalization when provided with a relevant prompt input x. Prompting LLMs to generate text useful for robot task planning is a nascent topic (Ahn et al., 2022; Jansen, 2020;Huangetal.,2022a,b;Lietal.,2022;PatelandPavlick, 2022). Prompt design is challenging given the lack of paired natural language instruction text with executable plans or robot action sequences (Liu et al., 2021). Devising a prompt for task plan prediction can be broken down into a prompting function and an answer search strategy (Liu et al., 2021). A prompting function, fprompt(.) transforms the input state observation s into a textual prompt. Answer search is the generation step, in which the LLM outputs from the entire LLM vocabulary or scores a predeﬁned set of options.

Closest to our work, Huang et al. (2022a) generates open- domain plans using LLMs. In that work, planning proceeds by:1)selectingasimilartaskinthepromptexample( fprompt); 2) open-ended task plan generation (answer search); and 3) 1:1 prediction to action matching. The entire plan is generated open-loop without any environment interaction, and later tested for executability of matched actions. How- ever, action matching based on generated text doesn’t ensure the action is admissible in the current situation. Inner- Monologue (Huang et al., 2022b) introduces environment feedback and state monitoring, but still found that LLM planners proposed actions involving objects not present in the scene. Our work shows that a programming language- inspired prompt generator can inform the LLM of both situatedenvironmentstateandavailablerobotactions,ensur- ing output compatibility to robot actions.

The related SayCan (Ahn et al., 2022) uses natural lan- guage prompting with LLMs to generate a set of feasible planning steps, re-scoring matched admissible actions using alearnedvaluefunction.SayCanconstructsasetofalladmis- sible actions expressed in natural language and scores them using an LLM. This is challenging to do in environments with combinatorial action spaces. Concurrent with our work are Socratic models (Zeng et al., 2022), which also use code- completion to generate robot plans. We go beyond (Zeng et al., 2022) by leveraging additional, familiar features of pro- gramming languages in our prompts. We deﬁne an fprompt that includes import statements to model robot capabilities, natural language comments to elicit common sense reason- ing,andassertionstotrackexecutionstate.Ouranswersearch

1001

is performed by allowing the LLM to generate an entire, exe- cutable plan program directly.

2.3 Recent developments following PROGPROMPT

Vemprala et al. (2023) further explores API-based planning withChatGPT1 indomainssuchasaerialrobotics,manipula- tionandvisualnavigation.Theydiscussthedesignprinciples for constructing interaction APIs, for action and perception, and prompts that can be used to generate code for robotic applications. Huang et al. (2023) builds on SayCan (Ahn et al., 2022) and generates planning steps token-by-token while scoring the tokens using both the LLM and the grounded pretrained value function. Cao and Lee (2023) explores gen- erating behavior trees to study hierarchical task planning using LLMs. Skreta et al. (2023) proposes iterative error correction via a syntax veriﬁer that repeatedly prompts the LLM with previous query appended with a list of errors. Mai et al. (2023), similar in approach as Zeng et al. (2022), Huangetal.(2022b),integratespretrainedmodelsforpercep- tion, planning, control, memory, and dialogue zero-shot, for active exploration and embodied question answering tasks. Gupta and Kembhavi (2022) extends the LLM code gen- eration and API-based perceptual interaction approach for a varietyofvision-langaugetasks.SomerecentworksXieetal. (2023a), Capitanelli and Mastrogiovanni (2023) use PDDL as the translation language instead of code, and use the LLM to generate either a PDDL plan or the goal. A classical plan- ner then plans for the PDDL goal or executes the generated plan. This approach ablated the need to generate precondi- tions using the LLM, however, needs the domain rules to be speciﬁed for the planner.

3 Our method: PROGPROMPT

We represent robot plans as pythonic programs. Following the paradigm of LLM prompting, we create a prompt struc- tured as pythonic code and use an LLM to complete the code (Fig. 2). We use features available in Python to construct prompts that elicit an LLM to generate situated robot task plans, conditioned on a natural language instruction.

3.1 Representing robot plans as pythonic functions

Plan functions consist of API calls to action primitives, comments to summarize actions, and assertions for tracking execution(Fig.3).Primitiveactionsuseobjectsasarguments. Forexample,the“putsalmoninthemicrowave”taskincludes API calls like find(salmon).

1 https://openai.com/blog/chatgpt/

123

1002

Fig. 2 Our ProgPrompts include import statement, object list, and example tasks (PROMPT for Planning). The Generated Plan is for microwave salmon. We highlight prompt comments, actions as imported function calls with objects as arguments, and assertions with recovery steps. PROMPT for State Feedback represents example asser-

Fig.3 Pythonic ProgPrompt plan for “put salmon in the microwave”

We utilize comments in the code to provide natural language summaries for subsequent sequences of actions. Comments help break down the high-level task into logi- cal sub-tasks. For example, in Fig. 3, the “put salmon in microwave” task is broken down into sub-tasks using com- ments “# grab salmon” and “# put salmon in microwave”. This partitioning could help the LLM to express its knowl- edge about tasks and sub-tasks in natural language and aid planning. Comments also inform the LLM about immedi- ate goals, reducing the possibility of incoherent, divergent, or repetitive outputs. Prior work Wei et al. (2022) has also shown the efﬁcacy of similar intermediate summaries called

123

Autonomous Robots (2023) 47:999–1012

tion checks. We further illustrate the execution of the program via a scenario where an assertion succeeds or fails, and how the generated plan corrects the error before executing the next step. Full Execution is shown in bottom-right. ‘...’ used for brevity

‘chain of thought’ for improving performance of LLMs on a range of arithmetic, commonsense, and symbolic reasoning tasks.Weempiricallyverifytheutilityofcomments(Table1; column Comments).

Assertions provide an environment feedback mechanism that encourages preconditions to be met, and allow error recovery possibility when they are not. For example, in Fig. 3, before the grab(salmon) action, the plan asserts the agent is close to salmon. If not, the agent ﬁrst exe- cutes find(salmon). In Table 1, we show that such assert statements (column Feedback) beneﬁt plan generation, and improve success rates.

3.2 Constructing programming language prompts

We provide information about the environment and primitive actions to the LLM through prompt construction. As done in few-shot LLM prompting, we also provide the LLM with examples of sample tasks and plans. Figure2 illustrates our prompt function fprompt which takes in all the information (observations, action primitives, examples) and produces a Pythonic prompt for the LLM to complete. The LLM then predicts the <next_task>(.) as an executable function (microwave_salmon in Fig. 2).

In the task microwave_salmon, a reasonable ﬁrst step that an LLM could generate is take_out(salmon, grocery

Autonomous Robots (2023) 47:999–1012

bag). However, the agent responsible for executing the plan might not have a primitive action to take_out. To inform theLLMabouttheagent’sactionprimitives,weprovidethem as Pythonic import statements. These encourage the LLM to restrict its output to only functions that are available in the current context. To change agents, ProgPrompt just needs a new list of imported functions representing agent actions. A grocery bag object might also not exist in the environment. We provide the available objects in the environment as a list of strings. Since our prompting scheme explicitly lists out the set of functions and objects available to the model, the generated plans typically contain actions an agent can take and objects available in the environment.

ProgPrompt also includes a few example tasks—fully executable program plans. Each example task demonstrates how to complete a given task using available actions and objects in the given environment. These examples demon- strate the relationship between task name, given as the functionhandle,andactionstotake,aswellastherestrictions on actions and objects to involve.

3.3 Task plan generation and execution

The given task is fully inferred by the LLM based on the ProgPrompt prompt. Generated plans are executed on a virtual agent or a physical robot system using an interpreter that executes each action command against the environment. Assertion checking is done in a closed-loop manner during execution, providing current environment state feedback.

4 Experiments

We evaluate our method with experiments in a virtual house- hold environment and on a physical robot manipulator.

4.1 Simulation experiments

We evaluate our method in the Virtual Home (VH) Environ- ment (Puig et al., 2018), a deterministic simulation platform fortypicalhouseholdactivities.AVHstatesisasetofobjects O and properties P. P encodes information like in(salmon, microwave) and agent_close_to(salmon). The action space is A = {grab, putin, putback, walk, find, open, close, switchon, switchoff, sit, standup}. We experiment with 3 VH environments. Each environ- mentcontains115uniqueobjectinstances(Fig.2),including class-levelduplicates.Eachobjecthaspropertiescorrespond- ingtoitsactionaffordances.Someobjectsalsohaveaseman- tic state like heated, washed, or used. For example, an object in the Food category can become heated whenever in(object,microwave) ∧ switched_on(microwave).

1003

Wecreateadataset of 70household tasks.Tasks areposed with high-level instructions like “microwave salmon”. We collect a ground-truth sequence of actions that completes the task from an initial state, and record the ﬁnal state g that deﬁnes a set of symbolic goal conditions, g ∈ P.

When executing generated programs, we incorporate environment state feedback in response to assertions. VH provides observations in the form of state graph with object properties and relations. To check assertions in this environ- ment, we extract information about the relevant object from the state graph and prompt the LLM to return whether the assertion holds or not given the state graph and assertion as a text prompt (Fig. 2 Prompt for State Feedback). We choose thisdesignoverarule-basedcheckingsinceit’smoregeneral.

4.2 Real-robot experiments

WeuseaFranka-EmikaPandarobotwithaparallel-jawgrip- per. We assume access to a pick-and-place policy. The policy takes as input two pointclouds of a target object and a tar- get container, and performs a pick-and-place operation to place the object on or inside the container. We use the sys- tem of Danielczuk et al. (2021) to implement the policy, and useMPPIformotiongeneration,SceneCollisionNet(Daniel- czuketal.,2021)toavoidcollisions,andgenerategraspposes with Contact-GraspNet (Sundermeyer et al., 2021).

We specify a single import statement for the action grab_and_putin(obj1, obj2)forProgPrompt.We use ViLD (Gu et al., 2022), an open-vocabulary object detec- tion model, to identify and segment objects in the scene and constructtheavailableobjectlistfortheprompt.Unlikeinthe virtualenvironment,whereobjectlistwasaglobalvariablein commonforalltasks,heretheobjectlistisalocalvariablefor each plan function, which allows greater ﬂexibility to adapt to new objects. The LLM outputs a plan containing function calls of form grab_and_putin(obj1, obj2). Here, objectsobj1and obj2aretextstringsthatwemaptopoint- cloudsusingViLDsegmentationmasksandthedepthimage. Duetorealworlduncertainty,wedonotimplementassertion- based closed loop options on the tabletop plans.

4.3 Evaluation metrics

We use three metrics to evaluate system performance: suc- cess rate (SR), executability (Exec), and goal conditions recall (GCR). The task-relevant goal-conditions are the set of goal-conditions that changed between the initial and ﬁnal state in the demonstration. SR is the fraction of executions that achieved all task-relevant goal-conditions. Exec is the fraction of actions in the plan that are executable in the envi- ronment, even if they are not relevant for the task. GCR is measured using the set difference between ground truth ﬁnal state conditions g and the ﬁnal state achieved g(cid:6) with the

123

1004

Autonomous Robots (2023) 47:999–1012

Table 1 Evaluation of generated programs on Virtual Home

#

Format

— Prompt Format and Parameters —

Comments

Feedback

LLM Backbone

SR

Exec

GCR





1

2

3

4

5

6

7

8

ProgPrompt

✓

ProgPrompt

✓

ProgPrompt

✓

ProgPrompt

✓

ProgPrompt

✓

ProgPrompt

✓

ProgPrompt

✗

ProgPrompt

✗

LangPrompt Baseline from Huang et al.

–

✓

✓

✓

✓

✓

✗

✓

✗

–

GPT4

Davinci- 003

Codex

Davinci

GPT3

GPT3

GPT3

GPT3

GPT3

GPT3

0.37 ± 0.06 0.470.470.47±0.15 0.40 ± 0.11 0.22 ± 0.04 0.34±0.08 0.28 ± 0.04 0.30 ± 0.00 0.18 ± 0.04 0.00 ± 0.00 0.00 ± 0.00

0.87 ± 0.01 0.85 ± 0.02 0.900.900.90±0.05 0.60 ± 0.04 0.84±0.01 0.82 ± 0.01 0.65 ± 0.01 0.68 ± 0.01 0.36 ± 0.00 0.45 ± 0.03

0.64 ± 0.02 0.740.740.74±0.07 0.72 ± 0.09 0.46 ± 0.04 0.65 ±0.05 0.56 ± 0.02 0.58 ± 0.02 0.42 ± 0.02 0.42 ± 0.02 0.21 ± 0.03

ProgPrompt uses 3 ﬁxed example programs, except the Davinci backbone which can ﬁt only 2 in the available API. Huang et al. (2022a) use 1 dynamically selected example, as described in their paper. LangPrompt uses 3 natural language text examples. Best performing model with a GPT3 backbone is shown in italic (used for our ablation studies); best performing model overall shown in bold. ProgPrompt signiﬁcantly outperforms the baseline Huang et al. (2022a) and LangPrompt. We also showcase how each ProgPrompt feature adds to the performance of the method

Table 2 ProgPrompt performance on the VH test-time tasks and their ground truth actions sequence lengths |A|

Task desc

watch tv

turn off light

brush teeth

throw away apple

make toast

eat chips on the sofa

put salmon in the fridge

wash the plate

bring coffeepot and cupcake to the coffee table

microwave salmon Avg: 0 ≤ |A| ≤ 5 Avg: 6 ≤ |A| ≤ 10 Avg: 11 ≤ |A| ≤ 18

|A|

3

3

8

8

8

5

8

18

8

11

SR

0.20 ± 0.40 0.40 ± 0.49 0.80 ± 0.40 1.00 ± 0.00 0.00 ± 0.00 0.00 ± 0.00 1.00 ± 0.00 0.00 ± 0.00 0.00 ± 0.00 0.00 ± 0.00 0.20 ± 0.40 0.60 ± 0.50 0.00 ± 0.00

Exec

0.42 ± 0.13 1.00 ± 0.00 0.74 ± 0.09 1.00 ± 0.00 1.00 ± 0.00 0.40 ± 0.00 1.00 ± 0.00 0.97 ± 0.04 1.00 ± 0.00 0.76 ± 0.13 0.61 ± 0.29 0.95 ± 0.11 0.87 ± 0.14

GCR

0.63 ± 0.28 0.65 ± 0.30 0.87 ± 0.26 1.00 ± 0.00 0.54 ± 0.33 0.53 ± 0.09 1.00 ± 0.00 0.48 ± 0.11 0.52 ± 0.14 0.24 ± 0.09 0.60 ± 0.25 0.79 ± 0.29 0.36 ± 0.16

generated plan, divided by the number of task-speciﬁc goal- conditions; SR= 1 only if GCR= 1.

5 Results

We show that ProgPrompt is an effective method for prompting LLMs to generate task plans for both virtual and physical agents.

Each result is averaged over 5 runs in a single VH envi- ronment across 10 tasks. The variability in performance across runs arises from sampling LLM output. We include 3 Pythonic task plan examples per prompt after evaluating performance on VH for between 1 prompt and 7 prompts and ﬁnding that 2 or more prompts result in roughly equal performance for GPT3. The plan examples are ﬁxed to be: “put the wine glass in the kitchen cabinet”, “throw away the lime”, and “wash mug”.

5.1 Virtual experiment results

Table 1 summarizes the performance of our task plan gen- eration and execution system in the seen environment of VirtualHome. We utilize a GPT3 as a language model back- bone to receive ProgPrompt prompts and generate plans.

We also include results on the recent GPT4 backbone. Unlike the GPT3 language model, GPT4 is a chat-bot model trained with reinforcement learning with human feedback (RLHF) to act as a helpful digital assistant OpenAI (2023). GPT4takesasinputasystempromptfollowedbyoneormore user prompts. Instead of simply auto-completing the code in the prompt, GPT4 interprets user prompts as questions

123

Autonomous Robots (2023) 47:999–1012

and generates answers as an assistant. To make GPT4 auto- complete our prompt, we used the following system prompt: You are a helpful assistant.. The user prompt is the same fprompt as shown in Fig. 2.

We can draw several conclusions from Table 1. First, ProgPrompt (rows 3–6) outperforms prior work (Huang et al., 2022a) (row 8) by a substantial margin on all metrics using the same large language model backbone. Second, we observe that the Codex (Chen et al., 2021) and Davinci models (Brown et al., 2020)—themselves GPT3 variants— show mixed success at the task. In particular, Davinci, the original GPT3 version, does not match base GPT3 perfor- mance (row 2 versus row 3), possibly because its prompt length constraints limit it to 2 task examples versus the 3 available to other rows. Additionally, Codex exceeds GPT3 performance on every metric (row 1 versus row 3), likely because Codex is explicitly trained on programming lan- guage data. However, Codex has limited access in terms of number of queries per minute, so we continue to use GPT3 as our main LLM backbone in the following ablation experi- ments. Our recommendation to the community is to utilize a program-like prompt for LLM-based task planning and exe- cution, for which base GPT3 works well, and we note that an LLMﬁne-tunedfurtheronprogramminglanguagedata,such as Codex, can do even better. We additionally report results onDavinci- 003and GPT4(row*),whichisthelatestGPT3 variant and the latest GPT variant in the series respectively at the time of this submission. Davinci- 003 has a better SR and GCR, indicating it might have an improved common- sense understanding, but lower Exec compared to Codex. The newest model, GPT- 4 does not seem to be better than latest GPT3 variant, on our tasks. Most of our results use the Davinci- 002 variant (that we refer to as GPT3 in this paper), which was the latest model available when this study was conducted.

We explore several ablations of ProgPrompt. First, we ﬁnd that Feedback mechanisms in the example programs, namely the assertions and recovery actions, improve perfor- mance (rows 3 versus 4 and 5 versus 6) across metrics, the sole exception being that Exec improves a bit without Feed- back when there are no Comments in the prompt example code. Second, we observe that removing Comments from the prompt code substantially reduces performance on all metrics (rows 3 versus 5 and 4 versus 6), highlighting the usefulness of the natural language guidance within the pro- gramming language structure.

We also evaluate LangPrompt, an alternative to Prog- Prompt that builds prompts from natural language text description of objects available and example task plans (row 7). LangPrompt is similar to the prompts built by Huang et al. (2022a). The outputs of LangPrompt are generated action sequences, rather than our proposed, program-like structures. Thus, we ﬁnetune GPT2 to learn a

1005

Table3 ProgPromptresultsonVirtualHomeinadditionalscenes.We evaluate on 10 tasks each in two additional VH scenes beyond scene Env- 0 where other reported results take place

VH scene

SR

Exec

GCR

Env- 0

Env- 1

Env- 2

Average

0.34 ± 0.08 0.56 ± 0.08 0.56 ± 0.05 0.48 ± 0.13

0.84 ± 0.01 0.85 ± 0.02 0.85 ± 0.03 0.85 ± 0.02

0.65 ± 0.05 0.81 ± 0.07 0.72 ± 0.09 0.73 ± 0.10

policy P(at|st,GPT3 step,a1:t−1) to map those generated sequences to executable actions in the simulation environ- ment. We use the 35 tasks in the training set, and annotate the text steps and the corresponding action sequence to get 400 data points for training and validation of this policy. We ﬁnd that while this method achieves reasonable partial suc- cess through GCR, it does not match (Huang et al., 2022a) for program executability Exec and does not generate any fully successful task executions. Task-by-Task Performance ProgPrompt performance for each task in the test set is shown in Table 2. We observe that tasks that are similar to prompt examples, such as throw away apple versus wash the plate have higher GCR since the ground truth prompt examples hint about good stop- ping points. Even with high Exec, some task GCR are low, becausesometaskshavemultipleappropriategoalstates,but we only evaluate against a single “true” goal. For example, after microwaving and plating salmon, the agent may put the salmon on a table or a countertop. Other Environments We evaluate ProgPrompt in two additional VH environments (Table 3). For each, we append a new object list representing the new environment after the example tasks in the prompt, followed by the task to be com- pleted in the new scene. The action primitives and other ProgPrompt settings remain unchanged. We evaluate on 10 tasks with 5 runs each. For new tasks like wash the cutlery in dishwasher, ProgPrompt is able to infer that cutlery refers to spoons and forks in the new scenes, despite that cutlery always refers to knives in example prompts.

5.2 Qualitative analysis and limitations

Wemanuallyinspectgeneratedprogramsandtheirexecution traces from ProgPrompt and characterize common fail- ure modes. Many failures stem from the decision to make ProgPrompt agnostic to the deployed environment and its peculiarities, which may be resolved through explicitly com- municating, for example, object affordances of the target environment as part of the ProgPrompt prompt.

Environment artifacts: the VH agent cannot ﬁnd or inter- act with objects nearby when sitting, and some

123

1006

Fig. 4 Robot plan execution rollout example on the sorting task show- ing relevant objects banana, strawberry, bottle, plate and box, and a distractor object drill. The LLM recognizes that banana and straw-

common sense actions for objects, such as open tvs- tand’s cabinets, are not available in VH.

Environment complexities: when an object is not acces- sible, the generated assertions might not be enough. For example, if the agent ﬁnds an object in a cabinet, it may not plan to open the cabinet to grab the object.

Action success feedback is not provided to the agent, which may lead to failure of the subsequent actions. Assertion recovery modules in the plan can help, but aren’t generated to cover all possibilities.

Incompletegeneration:SomeplansarecutshortbyLLM API caps. One possibility is to query the LLM again with the prompt and partially generated plan.

In addition to these failure modes, our strict ﬁnal state checking means if the agent completes the task and some, we may infer failure, because the environment goal state will not match our precomputed ground truth ﬁnal goal state. For example, after making coffee, the agent may take the cof- feepot to another table. Similarly, some task descriptions are ambiguous and have multiple plausible correct programs. For example, “make dinner” can have multiple possible solutions. ProgPrompt generates plans that cooks salmon using the fryingpan and stove, and sometimes the agent adds bellpepper orlime,orsometimeswithasideoffruit,orserved in a plate with cutlery. When run in a different VH environ- ment, the agent cooks chicken instead. ProgPrompt is able to generate plans for such complex tasks as well while using the objects available in the scene and not explicitly men- tioned in the task. However, automated evaluation of such tasks requires enumerating all valid and invalid possibilities or introducing human veriﬁcation.

Furthermore,wenotethatwhilethereasoningcapabilities of current state LLMs are impressive, our proposed method does not make any claims of providing guarantees. However, the evaluations reported in Table 1 offer insights into the capabilitiesofdifferentLLMswithinourtasksettings.While our method effectively prevents the LLM from generating unavailableactionsorobjects,itisworthacknowledging that depending on the LLM’s generation quality and reasoning capabilities, there is still a possibility of hallucination.

123

Autonomous Robots (2023) 47:999–1012

berry are fruits, and generates plan steps to place them on the plate, while placing the bottle in the box. The LLM ignores the distractor object drill. See Fig.1 for the prompt structure used

Table 4 Results on the physical robot by task type

Task description

Distractors

SR

Plan SR

GCR

put the banana in the bowl

0

1

1

1/1

4

1

1

1/1

put the pear on the plate

0

1

1

1/1

4

1

1

1/1

put the banana on the plate

0

1

1

2/2

and the pear in the bowl

3

1

1

2/2

sort the fruits on the plate

0

0

1

2/3

and the bottles in the box

1

1

1

3/3

2

0

0

2/3

5.3 Physical robot results

The physical robot results are shown in Table 4. We evaluate on 4 tasks of increasing difﬁculty listed in Table 4. For each task we perform two experiments: one in a scene that only containsthenecessaryobjects,andwithonetofourdistractor objects added.

All results shown use ProgPrompt with comments, but not feedback. Our physical robot setup did not allow reliably tracking system state and checking assertions, and is prone to random failures due to things like grasps slipping. The real world introduces randomness that complicates a quan- titative comparison between systems. Therefore, we intend the physical results to serve as a qualitative demonstration of the ease with which our prompting approach allows con- straining and grounding LLM-generated plans to a physical robot system. We report an additional metric Plan SR, which refers to whether the plan would have likely succeeded, pro- vided successful pick-and-place execution without gripper failures.

Across tasks, with and without distractor objects, the sys- tem almost always succeeds, failing only on the sort task. The run without distractors failed due to a random gripper failure. The run with 2 distractors failed because the model mistakenly considered a soup can to be a bottle. The exe-

Autonomous Robots (2023) 47:999–1012

cutability for the generated plans was always Exec=1. An execution rollout example is illustrated in Fig. 4.

Afterthisstudywasconducted,were-attemptedplangen- eration of the failed plan with GPT- 4, using the same system prompt as in Sect.5.1. GPT- 4 was able to successfully pre- dict thecorrect planand not confusethesoupcanforabottle.

6 Conclusions and future work

We present an LLM prompting scheme for robot task planning that brings together the two strengths of LLMs: commonsense reasoning and code understanding. We con- struct prompts that include situated understanding of the world and robot capabilities, enabling LLMs to directly gen- erate executable plans as programs. Our experiments show that ProgPrompt programming language features improve task performance across a range of metrics. Our method is intuitive and ﬂexible, and generalizes widely to new scenes, agents and tasks, including a real-robot deployment.

Asacommunity,weareonlyscratchingthesurfaceoftask planningasrobotplangenerationandcompletion.Wehopeto studybroaderuseofprogramminglanguagefeatures,includ- ing real-valued numbers to represent measurements, nested dictionaries to represent scene graphs, and more complex control ﬂow. Several works from the NLP community show that LLMs can do arithmetic and understand numbers, yet their capabilities for complex robot behavior generation are still relatively under-explored.

7 FAQs and discussion

Question 1 How does this approach compare with end- to-end robot learning models, and what are the current limitations?

ProgPrompt is a hierarchical solution to task planning where the abstract task descriptions leverage LLM’s reason- ing and maps the task plan to the grounded environment labels. On the other hand, in end-to-end approaches, gen- erally the model implicitly learns reasoning, planning, and grounding,whilemappingtheabstracttaskdescriptiontothe action space directly.

Pros:

LLMscandolong-horizonplanningfromanabstracttask description.

Decoupling the LLM planner from the environment makes generalization to new tasks and environments fea- sible.

ProgPromptenablesLLMstointelligentlycombinethe robot capabilities with the environment and their own

1007

reasoning ability to generate an executable and valid task plan.

The precondition checking helps recover from some fail- ure modes that can happen if actions are generated in the wrong order or are missed by the base plan.

Cons:

Requires action space discretization, formalization of environments and objects.

Plangenerationisopen-loop,withcommonsenseprecon- dition checking-based environment interaction.

Plan generation doesn’t consider low-level continuous aspects of the environment state, and only reasons with the semantic state for planning as well as precondition checking.

The amount of information exchange between language models and other modules such as the robot’s perceptual or proprioceptive state encoders is limited, since API- based access to these recent LLMs only allows textual queries. However, this is still promising as it indicates the need for a multimodal encoder that can work with input such as vision, touch, force, temperature, etc.

Question 2 How does it compare with the concurrent work: Code-as-Policies (CaP) (Liang et al., 2023)?

We believe that the general approach is quite similar to ours. CaP deﬁnes Hints and Examples which may corre- spond to Imports/Object lists and Task Plan examples in ProgPrompt .

CaP uses actions as API calls with certain parameters for the calls such as robot arm pose, velocity, etc. We use actions as API calls with objects as parameters.

CaP uses APIs to obtain environment information as well, like object pose or segmentation, for the pur- poseofplangeneration.However,ProgPromptextracts environment information via precondition checking on current environment state, to ensure plan executability. ProgPrompt also generates the prompt conditioned on information from perception models.

Question 3 During“PROMPTforStateFeedback”,itseems that the prompt already includes all information about the environmentstate.IsitnecessarytoprompttheLLMagainfor the assertion (compared to a simple rule-based algorithm)?

The environment state input to the model is not the full state for brevity. Thus, checking pre-conditions with the full state separately helps, as shown in Table 1.

The environment state could change during execution.

123

1008

Using LLM as opposed to a rule-based algorithm is a design choice made to keep the approach more general, instead of using a hand-coded rule-based algorithm. The assertion checking may also be replaced with a visual state conditioned module, when a semantic state is not available, such as in the real-world scenario. However, we leave these aspects to be addressed in future research.

Question 4 Is it possible that the generated code might lead the robot to be stuck in an inﬁnite loop?

LLM code generation could lead to loops by predicting the same actions repeatedly as a generation artifact. LLMs used to suffer from such degeneration, but with latest LLMs (i.e. GPT-3) we have not encountered it at all.

Question 5 Whyarereal-robotexperimentssimplerthanvir- tual experiments?

The real-robot experiments were done as a demonstration of the approach on a real-robot, while studying the method in depth in a virtual simulator, for the sake of simplicity and efﬁciency.

Question 6 What’s the difference between various GPT3 model versions used in this project?

We name GPT3, which is the latest available version of GPT3 model on OpenAI at the time the paper was written: text- davinci- 002. We name davinci as the original ver- sion of GPT3 released: text- davinci.2

Question 7 Why not a planning language like PDDL (or other planning languages) be used to construct Prog- Prompt? Any advantages of using a pythonic structure?

GPT-3 has been trained on data from the internet. There is a lot of python code on the internet, while PDDL is a language of much more narrow interest. Thus, we expect the LLM to better understand python syntax.

Python is a general purpose language, so it has more featuresthanPDDL.Furthermore,wewanttoavoidspec- ifying the full planning domain, instead relying on the knowledge learned by the LLM to make common-sense inferences. A recent work Xie et al. (2023b) uses LLMs to generate PDDL goals, however, it requires full domain speciﬁcation for a given environment.

Python isanaccessible language that alarger community is familiar with.

Question 8 How to handle multiple instances of the same object type in the scene?

2 More info on GPT3 models variations and naming can be found here: https://platform.openai.com/docs/models/overview

123

Autonomous Robots (2023) 47:999–1012

ProgPrompt doesn’t tackle the issue, however, Xie et al. (2023b)showsthatmultipleinstancesofthesameobjectscan be handled by using labels with object IDs such as “book_1, book_2”.

Question 9 Whydoesn’tthepapercomparetheperformance of the proposed method to InnerMonologue, SAYCAN, or Socratic models?

At the time of writing, the dataset or model from the above papers were not public. However, we do compare with a proxy approach, similar in underlying idea to the above approaches, in the VirtualHome environment. LangPlan in our baselines, uses GPT3 to get textual plan steps, which are then executed using a GPT-2 based trained policy.

Question 10 So the next step in this direction of research is to create highly structured inputs and outputs that could be compiled, since eventually we want something that compiles on robotic machines?

The disconnect and information bottleneck between LLM planning module and skill execution module might make it less concrete on “how much” and “what” information should be passed through the LLM during planning. That said, we think that this would be an interesting direction topursue and testthelimitsofLLM’shighlystructuredinputunderstanding and generation.

Question 11 How does it compare to a classical planner?

Classical planners require concrete goal condition speci- ﬁcation.AnLLMplannerreasonsoutafeasiblegoalstate from a high level task description, such as “microwave salmon”. From a user’s perspective, it is desirable to not have to specify a concrete semantic goal state of the envi- ronment and just be able to give an instruction to act on. • The search space would also be huge without common sense priors that an LLM planner leverages as opposed to a classical planner. Moreover, we also bypass the need to specify the domain knowledge needed for the search to roll out.

Moreover,thedomainspeciﬁcationandsearchspacewill grow non-linearly with the complexity of the environ- ment.

Question 12 Is it possible to decouple high-level language planning from low-level perceptual planning?

It may be feasible to an extent, however we believe that a clean decoupling might not be “all we need”. For instance, imagine an agent being stuck at an action that needs to be resolved at semantic level of reasoning, and probably very hard for the visual module to ﬁgure out. For instance, while placing a dish on an oven tray, the robot may need to pull the dish rack out of the oven to be successful in the task.

Autonomous Robots (2023) 47:999–1012

Question 13 What are the kinds of failures that can happen with ProgPrompt-like 2 stage decoupled pipeline?

A few broad failure categories could be:

Generation of a semantically wrong action. • Robotmightfailtoexecutetheactionatperception/action /skill level.

Robotneedstorecoverfromafailurebytakingadifferent high-levelaction,i.e.,apreconditionneedstobesatisﬁed. The challenge is to identify that precondition from the current state of the environment and the agent. the

Robotneedstorecoverfromafailurebytakingadifferent high-levelaction,i.e.,apreconditionneedstobesatisﬁed. The challenge is to identify that precondition from the current state of the environment and the agent. the

We assume a set of available action APIs that are imple- mented on the robot, without assuming the implementation method (e.g. motion planning or reinforcement learning). ProgPrompt abstracts over and complements other research on developing ﬂexible robot skills. This assumption is sim- ilar to those made in classical TAMP planners, where the planning space is restricted by the available robot skills.

Question 15 Can the ProgPrompt planner handle more expressive situations when “the embodied agent has to grasp an object in a speciﬁc way in order to complete an aspect of the task”?

This is possible, provided the deployed robot is capable of handling the requested action. For example, one can specify ‘how’ along with ‘what’ parameters for an action as function arguments, which may be discrete semantic grounded labels affecting the low-level skill execution, e.g. to select between different modes of grasping intended for different task pur- poses. However, it is an open question as to what the right level of abstraction is between high-level task speciﬁcation and continuous control space actions, and the answer might depend on the application domain.

AuthorContributions ISleadtheresearch,conductedexperiments,and drafted the manuscript; VB provided feedback, conducted experiments, drafted and reviewed the manuscript; JT and AG provided feedback, draftedandreviewedthemanuscript;AM,AG,DX,JT,andDFprovided feedback and reviewed the manuscript.

Funding Open access funding provided by SCELC, Statewide Califor- nia Electronic Library Consortium. This project was conducted at and funded by NVIDIA.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adap- tation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indi- cate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material

1009

is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitteduse,youwillneedtoobtainpermissiondirectlyfromthecopy- right holder. To view a copy of this licence, visit http://creativecomm ons.org/licenses/by/4.0/.

References

Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., & Yan, M. (2022). Do as i can, not as i say: Grounding language in robotic affordances. arXiv.

Akakzia, A., Colas, C., Oudeyer, P. Y., Chetouani, M., & Sigaud, O. (2021). Grounding language to autonomously-acquired skills via goal generation. In International conference on learning represen- tations.

Baier, J. A., Bacchus, F., & McIlraith, S. A. (2007). A heuristic search approach to planning with temporally extended preferences. In Proceedings of the 20th international joint conference on artiﬁcal intelligence (pp. 1808–1815). Morgan Kaufmann Publishers Inc. Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., & Amodei, D. (2020). Language models are few-shot learners. arXiv.

Bryce, D., & Kambhampati, S. (2007). A tutorial on planning graph

based reachability heuristics. AI Magazine, 28(1), 47.

Cao, Y., & Lee, C. (2023). Robot behavior-tree-based task generation with large language models. arXiv preprint arXiv:2302.12927 Capitanelli, A., & Mastrogiovanni, F. (2023). A framework to gen- erate neurosymbolic pddl-compliant planners. arXiv preprint arXiv:2303.00438

Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. D. O., Kaplan, J., & Zaremba, W. (2021). Evaluating large language models trained on code. arXiv.

Danielczuk, M., Mousavian, A., Eppner, C.,& Fox, D. (2021). Object rearrangement using learned implicit collision functions. In IEEE international conference on robotics and automation (ICRA). Eysenbach,B.,Salakhutdinov,R.R.,&Levine,S.(2019).Searchonthe replay buffer: Bridging planning and reinforcement learning. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d’ Alché-Buc, E. Fox, & R. Garnett (Eds.), Advances in neural information processing systems (vol. 32). Curran Associates, Inc.

Fikes, R. E., & Nilsson, N. J. (1971). Strips: A new approach to the applicationoftheoremprovingtoproblemsolving.InProceedings of the 2nd international joint conference on artiﬁcial intelligence (pp. 608–620). Morgan Kaufmann Publishers Inc.

Garrett, C. R., Lozano-Pérez, T., & Kaelbling, L. P. (2020). Pddl- stream: Integrating symbolic planners and blackbox samplers via optimistic adaptive planning. Proceedings of the International Conference on Automated Planning and Scheduling, 30(1), 440– 448.

Gu, X., Lin, T. Y., Kuo, W., & Cui, Y. (2022). Open-vocabulary object detection via vision and language knowledge distillation. In Inter- national conference on learning representations.

Gupta, T., & Kembhavi, A. (2022). Visual programming: Com- training. arXiv preprint

positional visual arXiv:2211.11559

reasoning without

Helmert, M. (2006). The fast downward planning system. Journal of

Artiﬁcial Intelligence Research, 26(1), 191–246.

Hoffmann, J. (2001). Ff: The fast-forward planning system. AI Maga-

zine, 22(3), 57.

Holtzman,A.,Buys, J.,Du,L.,Forbes, M., &Choi,Y.(2020). The curi- ous case of neural text degeneration. In International conference on learning representations.

123

1010

Huang, W., Abbeel, P., Pathak, D., & Mordatch, I. (2022). Language modelsaszero-shotplanners:Extractingactionableknowledgefor embodied agents. arXiv preprint arXiv:2201.07207

Huang,W.,Xia,F.,Shah,D.,Driess,D.,Zeng,A.,Lu,Y.,others(2023). Grounded decoding: Guiding text generation with grounded mod- els for robot control. arXiv preprint arXiv:2303.00855

Huang, W., Xia, F., Xiao, T., Chan, H., Liang, J., Florence, P., & Ichter, B. (2022). Inner monologue: Embodied reasoning through plan- ning with language models. arxiv preprint arxiv:2207.05608. Jansen, P. (2020). Visually-grounded planning without vision: Lan- guage models infer detailed plans from high-level instructions. In Findings of the association for computational linguistics: Emnlp 2020 (pp. 4412–4417). Online: Association for Computational Linguistics.

Jiang, Y., Gu, S. S., Murphy, K. P., & Finn, C. (2019). Language as an abstraction for hierarchical deep reinforcement learning. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d’ Alché-Buc, E. Fox, & R. Garnett (Eds.), Advances in neural information processing systems. (vol. 32). Curran Associates, Inc.

Jiang, Y., Zhang, S., Khandelwal, P., & Stone, P. (2018). Task planning in robotics: An empirical comparison of pddl-based and asp-based systems. arXiv.

Kurutach, T., Tamar, A., Yang, G., Russell, S. J., & Abbeel, P. (2018). Learningplannablerepresentationswithcausalinfogan.InS.Ben- gio, H. Wallach, H. Larochelle, K. Grauman, N. Cesa-Bianchi, & R. Garnett (Eds.), Advances in neural information processing sys- tems (vol. 31). Curran Associates, Inc.

Li, S., Puig, X., Paxton, C., Du, Y., Wang, C., Fan, L., & Zhu, Y. (2022). Pre-trained language models for interactive decision- making. arXiv.

Liang,J.,Huang,W.,Xia,F.,Xu,P.,Hausman,K.,Ichter,B.,&Zeng,A. (2023). Code as policies: Language model programs for embodied control.

Liu, P., Yuan, W., Fu, J., Jiang, Z., Hayashi, H., & Neubig, G. (2021). Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing. arXiv.

Luong, T., Pham, H., & Manning, C. D. (2015). Effective approaches to attention-based neural machine translation. In Proceedings of the 2015 conference on empirical methods in natural language processing (pp. 1412–1421). Association for Computational Lin- guistics.

Mai, J., Chen, J., Li, B., Qian, G., Elhoseiny, M., & Ghanem, B. (2023). Llm as a robotic brain: Unifying egocentric memory and control. arXiv preprint arXiv:2304.09349

Mirchandani,S.,Karamcheti,S.,&Sadigh,D.(2021).Ella:Exploration through learned language abstraction. In M. Ranzato, A. Beygelz- imer, Y. Dauphin, P. Liang, J. W. Vaughan (Eds.), Advances in neuralinformationprocessingsystems(vol.34,pp.29529–29540). Curran Associates, Inc.

Nair, S., & Finn, C. (2020). Hierarchical foresight: Self-supervised learning of long-horizon tasks via visual subgoal generation. In International conference on learning representations.

OpenAI (2023). Gpt-4 technical report. arXiv. Patel, R., & Pavlick, E. (2022). Mapping language models to grounded conceptual spaces. In International conference on learning repre- sentations.

Puig, X., Ra, K., Boben, M., Li, J., Wang, T., Fidler, S., & Tor- ralba, A. (2018). Virtualhome: Simulating household activities via programs. In 2018 IEEE/cvf conference on computer vision and pattern recognition (pp. 8494–8502).

Shah,D.,Toshev,A.T.,Levine,S.,&brianichter.(2022).Valuefunction spaces: Skill-centric state abstractions for long-horizon reasoning. In International conference on learning representations.

Sharma, P., Torralba, A., & Andreas, J. (2022). Skill induction and planning with latent language. In Proceedings of the 60th annual meeting of the association for computational linguistics (volume

123

Autonomous Robots (2023) 47:999–1012

1: Long papers) (pp. 1713–1726). Association for Computational Linguistics.

Shridhar, M., Thomason, J., Gordon, D., Bisk, Y., Han, W., Mottaghi, R., & Fox, D. (2020). ALFRED: A Benchmark for Interpreting Grounded Instructions for Everyday Tasks. In The IEEE confer- ence on computer vision and pattern recognition (cvpr).

Silver, T., Chitnis, R., Kumar, N., McClinton, W., Lozano-Perez, T., Kaelbling,L.P.,&Tenenbaum,J.(2022).Inventingrelationalstate and action abstractions for effective and efﬁcient bilevel planning. In The multi-disciplinary conference on reinforcement learning and decision making (rldm).

Skreta, M., Yoshikawa, N., Arellano-Rubach, S., Ji, Z., Kristensen, L. B., Darvish, K., & Garg, A. (2023). Errors are useful prompts: Instruction guided task programming with veriﬁer-assisted itera- tive prompting. arXiv preprint arXiv:2303.14100

Srinivas, A., Jabri, A., Abbeel, P., Levine, S., & Finn, C. (2018). Uni- versal planning networks: Learning generalizable representations for visuomotor control. In J. Dy, & A. Krause (Eds.), Proceedings of the 35th international conference on machine learning (vol. 80, pp. 4732–4741). PMLR.

Sundermeyer, M., Mousavian, A., Triebel, R., & Fox, D. (2021). Contact-graspnet: Efﬁcient 6-dof grasp generation in cluttered scenes. In 2021 IEEE international conference on robotics and automation (icra) (pp. 13438–13444).

Vemprala, S., Bonatti, R., Bucker, A., & Kapoor, A. (2023). Chatgpt

for robotics: Design principles and model abilities. 2023

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., & Zhou, D. (2022). Chain of thought prompting elicits reasoning in large language models. arXiv.

Wiseman, S., Shieber, S., & Rush, A. (2017). Challenges in data- to-document generation. In Proceedings of the 2017 conference on empirical methods in natural language processing (pp. 2253– 2263). Association for Computational Linguistics.

Xie,Y.,Yu,C.,Zhu,T.,Bai,J.,Gong,Z.,&Soh,H.(2023a).Translating natural language to planning goals with large-language models. arXiv preprint arXiv:2302.05128

Xie,Y.,Yu,C.,Zhu,T.,Bai,J.,Gong,Z.,&Soh,H.(2023b).Translating

natural language to planning goals with large-language models.

Xu, D., Martín-Martín, R., Huang, D. A., Zhu, Y., Savarese, S., & Fei- Fei, L. F. (2019). Regression planning networks. In H. Wallach, H. Larochelle,A.Beygelzimer,F.d’Alché-Buc,E.Fox,&R.Garnett (Eds.), Advances in neural information processing systems (vol. 32). Curran Associates, Inc.

Xu, D., Nair, S., Zhu, Y., Gao, J., Garg, A., Fei-Fei, L., & Savarese, S. (2018). Neural task programming: Learning to generalize across hierarchical tasks. In 2018 IEEE international conference on robotics and automation (icra) (pp. 3795–3802).

Zeng, A., Attarian, M., Ichter, B., Choromanski, K., Wong, A., Welker, S., & Florence, P. (2022). Socratic models: Composing zero-shot multimodal reasoning with language. arXiv

Zhu, Y., Tremblay, J., Birchﬁeld, S., & Zhu, Y. (2020). Hierarchical planning for long-horizon manipulation with geometric and sym- bolic scene graphs. arXiv.

Publisher’s Note Springer Nature remains neutral with regard to juris- dictional claims in published maps and institutional afﬁliations.

Autonomous Robots (2023) 47:999–1012

Ishika Singh is a 3rd year PhD student advised by Professor Jesse Thomason in the Computer Sci- ence department at the Univer- sity of Southern California. Her research focuses on problems in language-conditioned robot learn- ing such as vision-language nav- igation, manipulation and task plan- ning. Previously, she was an under- grad at IIT Kanpur.

Valts Blukis is a research scien- tist at NVIDIA. His research goal is creating scalable and generaliz- able machine learning algorithms and models that enable robots to interact with people through nat- ural language while observing the unstructured world through ﬁrst- person sensor observations. He received his PhD from Cornell University and Cornell Tech.

Arsalan Mousavian s a senior research scientist at NVIDIA Seat- tle Robotics Lab. He is interested in using computer vision and 3D vision for robotics tasks such as object manipulation. Prior to NVIDIA, he ﬁnished his PhD in the Com- puter Science department at George Mason University.

AnkitGoyalis a Research Scientist in Robotics at NVIDIA. He did his Ph.D. in Computer Science at Princeton University. I com- pleted Masters from University of Michigan and Bachelors from IIT Kanpur. He is interested in under- standing various aspects of intel- ligence, especially reasoning and common sense. In particular, he wants to develop computation mod- els for various reasoning skills that humans possess.

1011

Danfei Xu is an Assistant Pro- fessor at the School of Interac- tive Computing at Georgia Tech and a (part-time) Research Sci- entist at NVIDIA AI. His cur- rent research focuses on visuo- motor skill learning, long-horizon manipulation planning, and data- driven approaches to human-robot collaboration. He received his Ph.D. in CS from Stanford University.

Jonathan Tremblay is a research scientist at NVIDIA. His research interests are in computer vision, synthetic data, and reinforcement learning for robotics applications. At NVIDIA, Jonathan has focused on using synthetic data to train object detectors, object pose esti- mation, few shot learning, etc. Jonathan’s goal is to create robust and acces- sible computer vision systems for roboticists to use on their sys- tem. Prior to joining NVIDIA, Jonathan received Ph.D. in com- puter science from McGill Uni-

versity.

Dieter Fox is Senior Director of Robotics Research at Nvidia. His research is in robotics, with strong connections to artiﬁcial intelligence, computer vision, and machine learn- ing. He is currently on partial leave from the University of Wash- ington, where he is a Professor in the Paul G. Allen School of Computer Science & Engineer- ing. At UW, he also heads the UW Robotics and State Estima- tion Lab. From 2009 to 2011, he was Director of the Intel Research Labs Seattle. Dieter obtained his

Ph.D. from the University of Bonn, Germany.

Jesse Thomason is an Assis- tant Professor at USC leading the Grounding Language in Multimodal Observations, Actions, and Robots (GLAMOR) lab. GLAMOR brings together natural language process- ing and robotics (RoboNLP). Jesse joined USC in 2021 and received his PhD from the University of Texas at Austin in 2018.

123

1012

Animesh Garg is an Stephen Fleming Early Career Professor in Computer Science at Georgia Tech. Previously, he was an Assis- tant Professor of Computer Sci- ence at University of Toronto and a Faculty Member at the Vector Institute. He is also a Sr. Research Scientist at Nvidia. He earned his Ph.D. in Operations Research from UC Berkeley and postdoc at Stan- ford. His group focuses on multi- modal object-centric and spatiotem- poral event representations, self- supervised pre-training for rein- forcement learning & control, principle of efﬁcient dexterous skill learning.

123

Autonomous Robots (2023) 47:999–1012