0 2 0 2

r a

M 3 1

] L P . s c [

1 v 4 2 3 6 0 . 3 0 0 2 : v i X r a

Fireiron: A Scheduling Language for High-Performance Linear Algebra on GPUs

Bastian Hagedorn† University of Münster b.hagedorn@wwu.de

Archibald Samuel Elliott† lowRISC sam@lenary.co.uk

Henrik Barthels† AICES, RWTH Aachen University barthels@aices.rwth-aachen.de

Rastislav Bodik† University of Washington bodik@cs.washington.edu

Vinod Grover NVIDIA vgrover@nvidia.com

Abstract Achieving high-performance GPU kernels requires optimiz- ing algorithm implementations to the targeted GPU architec- ture. It is of utmost importance to fully use the compute and memory hierarchy, as well as available specialised hardware. Currently, vendor libraries like cuBLAS and cuDNN pro- videthebestperformingimplementationsofGPUalgorithms. However the task of the library programmer is incredibly challenging: for each provided algorithm, high-performance implementations have to be developed for all commonly used architectures, input sizes, and different storage formats. These implementations are generally provided as optimized assembly code because performance-critical architectural features are only exposed at this level. This prevents reuse be- tween different implementations of even the same algorithm, as simple differences can have major effects on low-level implementation details.

In this paper we introduce Fireiron, a DSL and compiler which allows the specification of high-performance GPU implementations as compositions of simple and reusable building blocks. We show how to use Fireiron to optimize matrix multiplication implementations, achieving perfor- mance matching hand-coded CUDA kernels, even when us- ing specialised hardware such as NIVIDA Tensor Cores, and outperforming state-of-the-art implementations provided by cuBLAS by more than 2×.

specialization, swizzling, or the exploitation of special built- in instructions like NVIDIA’s WMMA (warp-level matrix multiply accumulate).

Figuring out which optimizations lead to the best perfor- mance is a tedious task. Today, kernels are either written in low-level programming languages such as CUDA or PTX- assembly, or they are generated using high-level frameworks such as Halide [15, 16] or TVM [6]. In the first case, low-level implementation details are interwoven with and obscure the intended functionality. This makes it hard to try out different optimizations as it usually requires rewriting large parts of the existing code. To mitigate this, high-level frameworks such as Halide separate the description of the computation (algorithm) from its optimizations (schedule) using a sepa- rate scheduling language that describes the optimizations to apply. Here, however, users are still limited to the set of opti- mizations and application the specific framework supports. In this paper, we propose Fireiron, a framework for grad- ual forging of high-performance GPU kernels. Fireiron is a language and compiler which, similar to Halide and TVM, provides a small set of decompositions which a programmer uses to design implementations of specifications. In Fireiron, important implementation concerns such as the mapping of data to threads are first-class concepts of the language and are specified before less important decisions are made. This allows, for instance, for a programmer to decide how matrices are stored across the GPU, with the remainder of the implementation following these prior constraints.

1 Introduction Implementing high-performance kernels for GPUs is incred- ibly challenging. Achieving performance close to the the- oretical peak requires the careful application of a plethora of optimizations to optimally use the compute and memory hierarchy of the target architecture. In order to maximize available memory bandwidth, one needs to make use of vectorized loads and stores, padding to avoid shared mem- ory bank conflicts, or storage layout transformations. Op- timizations affecting the compute hierarchy include warp

Similar to Halide, a specification represents the computa- tion to implement (algorithms in Halide) and a decomposition describes how to (partially) implement a given specification (schedule in Halide). Our decompositions are composable and modular, so programmers can start an implementation with a simple decomposition and then gradually refine it in order to specialize it for the current target hardware. This modu- larity allows decompositions to be reused when targeting different architectures.

When implementing high-performance applications, GPU programmers usually rely extensively on libraries of fine- tuned routines such as cuBLAS and cuDNN. One limitation

†This work was done while the authors were at NVIDIA.

is that inputs to these routines must be passed in address- ible storage such as global memory or shared memory. This prevents programmers from reusing values stored in, for ex- ample registers or FMA argument collectors, whose address cannot be taken. This means existing implementations can- not be decomposed into smaller, flexible components from which new, efficient implementations could be composed by library users.

Consider the case when the input matrices are distributed across the registers of the threads of a cooperative thread array (CTA). Ideally, we want to specify the location of the matrix(inregisters)whencallingthelibraryprocedure.How- ever, today, the procedure needs to be compiled for a partic- ular size of the matrix and a particular number of threads in the CTA. Additionally, the implementation of the producers of the matrices needs to be coordinated so that the matri- ces are placed in the registers expected by the consumers. This coordination prevents independent development and reuse of implementations. Fireiron is a language and com- piler architecture that allows efficient library procedures to be broken into reusable pieces.

Since every DSL is only as good as the abstractions it pro- vides, experts often struggle to break out of restrictions in situations where they need to make use of optimizations for which suitable abstractions cannot be defined easily. In con- trast to existing high-level frameworks like Halide, Fireiron allows the programmer to regain full control and provide custom implementations (e.g., handwritten inline assembly), for arbitrary specifications at any point in a decomposition. This allows performance experts to fine-tune specific parts of their implementations using hand-crafted solutions to specifications.

To summarize, Fireiron is a framework for simplifying the development of high-performance GPU kernels, targeted towards experts. We achieve this by achieving a balance between high-level abstractions and control, as well as by providing novel mechanisms to faciliate reuse of optimized implementations that go beyond reusing tuned library rou- tines. In this paper, we make the following contributions:

1. We introduce Fireiron, a high-level language and com- piler providing easy-to-use Decompositions to imple- ment Specifications of GPU computations.

2. We enable rapid prototyping of complex optimizations by introducing Refinements for decompositions which allow gradual improvement of an existing implementa- tion with minimal effort. We illustrate these concepts using the example of matrix multiplication.

3. We show how to use and extend Fireiron’s basic de- compositions to make use of the TensorCores in newer NVIDIA architectures, and show how to define and reuse optimizations as first-class objects in Fireiron. 4. We evaluate our approach by comparing against hand- written CUDA code targeting different architectures. 2

We express the same optimizations in Fireiron and show that our generated code achieves the same per- formance as the hand-tuned kernels. Additionally we compare our approach to cuBLAS and show that by using Fireiron, in combination with mma.sync assem- bly instructions and carefully chosen tile sizes, we are able to outperform high-performance library imple- mentations by up to 2x.

2 Motivation Fireiron’s design is based upon four main goals, and the mechanisms we used to achieve them.

2.1 Control: Fine-grained Level of Control over the

Implementation Strategy.

Every domain-specific language is only as good as the ab- stractions it provides to its user. When striving for opti- mal performance, there will always be implementations for which no suitable abstractions are available in high-level DSLs. In order to avoid fighting restrictive abstractions, Fire- iron offers kernel programmers the ability to regain full control at any point and for any part of the implementation. By allowing the programmer to insert their own specialized code as micro-kernels for matching specifications, we achieve a balance between leveraging high-level abstractions and maximizing productivity and performance.

Mechanism: The programmer specifies the implementation strategy using a decomposition language. This language con- trols the decomposition of the computation, the placement of data into memory, the communication of data between levels of the memory hierarchy, as well as the mapping of computation onto the compute elements. Decomposing a specification yields a new sub-specification which describes the problem left to implement. A programmer decomposes a specification until it is executable, that is it matches ei- ther the specification of a built-in instruction such as fused- multiply-add (FMA), or the specification of a user-provided micro-kernel for which they have provided an implementa- tion. During code generation we then either emit the built-in instruction or the provided code snippet.

2.2 Reusability: Reuse of Implementation

Decompositions.

We offer the kernel programmer the reuse of previously de- veloped high-performance decompositions, including those that result in generated code which typically cannot be im- plemented as a traditional library procedure.

Mechanism: The implementation of a kernel is hierarchical and each fragment of the implementation can be described with a concise specification. Specifications are implemented with decompositions that are stored as first-class objects and can therefore be reused. Essentially, a decomposition

breaks existing efficient library procedures (such as a kernel- level GEMM computation) into reusable pieces which can be stored as first-class objects. This allows the extraction and reuse of specific parts of an efficient implementation such as a tiled warp-level GEMM whose operands are stored in shared memory or registers.

In more detail, the implementation is a decomposition tree whose leaves are specifications (representing the remaining sub-computations to implement). In a final implementation, theleafspecificationsareexecutable,e.g.built-ininstructions such as FMA or user-provided micro-kernels. In a partial implementation, the leaves can be specifications that still need to be implemented.

2.3 Flexibility: Target (Specialized) Instructions

with Arbitrary Granularity.

The architecture of GPUs changes rapidly and significantly. For example, the recent NVIDIA Volta and Turing archi- tectures contain specialized MMA (Matrix-Multiply Accu- mulate) units, so-called TensorCores, which are able to effi- ciently compute matrix multiplications using small groups of cooperating threads. Currently, this functionality is ex- posed in two ways: as 8-thread HMMA instructions in PTX (mma.sync),andaswarp-wideWMMAinstructionsinCUDA. The decomposition language must be able to express imple- mentations which make use of these specialized instructions despite the varying granularity of their cooperating threads.

Mechanism: In Fireiron, kernels, micro-kernels, and built- in instructions are described using the same concept: specifi- cations. Once a programmer decomposes a problem into a specification that is executable, i.e., a specification for which we know how to generate code, they can decide to stop decomposing the specification and instead pass the imple- mentation to the code generator.

Imagine we decompose a kernel-level M×N×K-matrix multiplication kernel to a warp-level 16×16×16 matrix mul- tiplication computation. We can either decompose this spec- ification further into several thread-level FMA instructions or stop decomposing here and generate a single WMMA invocation. This mechanism allows us to adapt to future architectures as we can simply add new built-in instructions and their specifications to Fireiron, which is exactly what we did for both HMMA and WMMA.

2.4 Cooperation: Data Types for Parallel

Cooperation.

In parallel programs, multiple threads cooperate to (1) load arrays, (2) compute new values, and (3) store them back. In advanced implementations, the mapping of the array ele- ments to threads may change between these three phases. To simplify programming such implementations, we want to abstract away from the mapping as long as possible, specify- ing it only at lower levels of the decomposition. This makes

3

higher-level specifications more general, permitting more possible implementations.

Mechanism: Distributed arrays are data types that the pro- grammer can distribute over private memories. Fireiron pro- vides the illusion that a distributed array is indivisibly stored across, say, the registers of multiple warps; here, registers are memories that are private to each thread. The Fireiron compiler automatically divides the array and distributes the pieces onto registers of threads of the involved warps. This is especially useful for the epilog of a kernel implementations where a CTA needs to move computed results (usually resid- ing in registers spread across all its threads) back to global memory.

3 Specs and Decompositions Most high-performance kernels for GPUs are written in a hierarchical style. The original problem to be computed is decomposable into smaller sub-problems of the same kind. These sub-problems are then assigned to and computed by the different levels of the compute hierarchy. Figure 1 visu- alizes this observation using a simple matrix multiplication kernel. Step by step, the matrix multiplication is decomposed into a hierarchy of tiles and data is transferred to lower levels of the memory hierarchy until eventually every thread com- putes a single FMA instruction. Here, FMA can be viewed as a matrix multiplication of matrices which only contain a single element.

Fireiron introduces two main concepts: Specifications and Decompositions. These two concepts allow to describe im- plementations, such as the one shown in Figure 1, and their mapping to the hardware in a natural way.

3.1 Specifications

A Specification (spec) is a data-structure describing the com- putation to implement. A spec contains enough information such that a programmer would be able to manually write an implementation. This especially entails that a spec keeps track of the shapes, locations and storage layouts of its input and output tensors, as well as which level of the compute hierarchy (i.e., Kernel, Block, Warp or Thread) is responsible for computing this operation. Currently, Fireiron supports two main classes of specs: Matrix Multiplication (MatMul), and data movement (Move). The following listing shows a kernel-level matrix multiplication spec:

MatMul(ComputeHierarchy: Kernel ,

A: Matrix((M x K), float , GL, ColMajor), B: Matrix((K x N), float , GL, ColMajor), C: Matrix((M x N), float , GL, ColMajor))

At the beginning of every GPU kernel, inputs are stored in global memory (GL). For matrices, Fireiron supports both static shapes (compile-time constants) and symbolic shapes denoted as simple arithmetic expressions e.g., M = ((x + y) % z) where x, y and z are only known at runtime. If not

Figure 1. Visualization of the hierarchical structure of GPU programs using a matrix multiplication kernel as example. Within a typical GPU kernel we gradually descend the compute and memory hierarchy while computing smaller instances of the original problem.

further specified, we assume that all matrices are stored in column-major format and contain elements of type float and write MatMul(M,N,K)(GL,GL,GL)(Kernel) as a short form representing the spec in the listing above.

Givena spec, onecan performone ofthe followingactions: 1. Arrive at an executable spec; or 2. Decompose it into a smaller sub-spec.

Micro-Kernels At any time when decomposing specs with Fireiron, the user can provide a handwritten micro-kernel which implements the current spec. This allows the Fireiron user to break out of the DSL and use custom implementa- tions, potentially written in low-level assembly, for which we cannot yet provide good abstractions.

3.3 Decompositions

3.2 Executable Specifications

A specification is called executable when it matches the specification of a user-provided micro-kernel, or a built-in instruction. Fireiron, contains a built-in collection of ex- ecutable specs matching different instructions like FFMA and HFMA. For example, the FMA instruction has the spec MatMul(1,1,1)(RF,RF,RF)(Thread). When a final imple- mentation contains executable leaf specs, Fireiron will emit the matching built-in instruction or chosen micro-kernel when generating the implementation.

A Decomposition describes how to (partially) implement a given spec. More specifically, a decomposition is a function Spec → Spec which, given a spec, returns a new spec that represents the smaller decomposed sub-problem. Fireiron provides two main decompositions, tile and load, which allow implementations to use the compute and memory hi- erarchy of a GPU.

spec.tile(r,c)createsr×c shapedtilesintheoutput matrix. Input matrices are tiled accordingly. In order to assign tiles to a level of the compute hierarchy, we can furtherrefine thetilingbyapplying.to(level)which

4

MKNK.to(Block)Block

Figure 2. Tiling a MatMul spec results in a decomposed sub- spec with adjusted dimensions and optionally adjusted com- pute hierarchy to indicate parallel execution.

.load(A,SH,decomposition)

Figure 3. Applying load to a MatMul spec results in a new spec in which the memory location of the specified operand has changed. The load will be implemented as specified in the load-decomposition.

changes the responsible compute hierarchy level for the resulting tiled spec. Figure 2 shows the effect of tiling a MatMul spec.

spec.load(M,l,d) loads the matrix M to the level l of the memory hierarchy with an implementation describedasdecompositiond.Figure3showstheeffect of loading a MatMul spec. The memory hierarchy has three levels: global memory (GL), shared memory (SH) and registers (RF).

Fireiron is implemented as a domain-specific language, em- bedded in Scala, which generates CUDA. We allow the user to define custom decompositions to allow them to implement advanced optimisations, as described later.

3.4 Decomposing Matrix Multiplication Listing 1 shows an example decomposition of a MatMul spec using only tile, and load. The done operator marks the end of the decomposition and invokes the code generator. This example can already be compiled into a simple, correct

5

mm = MatMul(M,N,K)(GL,GL,GL)(Kernel) mm .tile(128,128) .to(Block)

// resulting intermediate specs below // MatMul(128,128,K)(GL,GL,GL)(Kernel) // MatMul(128,128,K)(GL,GL,GL)(Block ) .load(A, SH, _) // MatMul(128,128,K)(SH,GL,GL)(Block ) .load(A, SH, _) // MatMul(128,128,K)(SH,SH,GL)(Block ) // MatMul(64, 32, K)(SH,SH,GL)(Block ) .tile(64,32) ) // MatMul(64, 32, K)(SH,SH,GL)(Warp .to(Warp) K)(SH,SH,GL)(Warp // MatMul(8, ) K)(SH,SH,GL)(Thread) // MatMul(8, K)(RF,SH,GL)(Thread) .load(A, RF, _) // MatMul(8, K)(RF,RF,GL)(Thread) .load(B, RF, _) // MatMul(8, K)(RF,RF,GL)(Thread) // MatMul(1, .tile(1,1) // invoke codegen , emit dot micro -kernel .done(dot.cu)

.tile(8,8)

8, 8, 8, 8, 1,

.to(Thread)

Listing1.AsimpledecompositionfortheMatMulspec:Each decomposition yields a smaller sub-specification which is further implemented by the subsequent decompositions.

implementation. Here, the load decompositions, which de- scribe how to implement the data movement, are omitted for brevity (denoted _) .

Note that unlike in the implementation shown in Fig- ure 1, the K-dimension remains unchanged and the loca- tion of the C-matrix has not changed. The residual spec (MatMul(1,1,K)(RF,RF,GL)(Thread))isnotexecutable,but instead describes a simple dot-product which is implemented in the micro-kernel dot.cu, and passed as an optional argu- ment to done.

This simple decomposition already establishes major de- sign decisions for implementing matrix multiplication: it de- fines 1) how many elements each level of the compute hierar- chywillcomputeand,2)howmanyelementsofeachoperand are stored at which layer of the memory hierarchy, (which determines the overall memory consumption). Further de- compositions will preserve this mapping, which emphasizes Fireiron’s methodology for developing high-performance GPU kernels: Fireiron allows programmers to focus on one thing at a time and then to gradually improve unspecified or sub-optimal parts of the decomposition.

Every decomposition needs to specify three things which also need to be specified when adding new decompositions to Fireiron:

a. Given the current spec, how to compute a new spec; b. The code to emit during code generation when pro-

cessing this decomposition; and

c. How to update the view into the current slices of the spec’s operands to be able to generate correct indexing expressions.

a.ComputingtheSub-Spec Everyapplicationofadecom- position yields a new spec. Listing 1 shows the intermediate specs after applying tile and load. When applying tile, only the M and N dimension of all operands change. Con- versely, when applying load, only the memory location of the specified matrix changes.

b. Code Generation During code generation, we process thecurrentdecompositiontreefromtoptobottom,andinsert code for every decomposition, until we reach the residual spec. Generally, every decomposition represents one or more (potentially parallel) loop-nests whose body is defined by the subsequent decompositions. For example in case of tile, two for-loops are generated which iterate over the created tiles:

// .tile(mBlock , nBlock) emits: for( int row = 0; row < mBlock; i++ ) {

for( int col = 0; col < nBlock; j++ ) { // implementation of resulting spec subspec.codegen(); }}

If a level of the compute hierarchy has been assigned (using the .to(level) refinement), instead of emitting sequential for-loops, we use the unique compute hierarchy indexes for the specified level to assign a tile to each unit at that level:

// .tile(mBlock , nBlock).to(Block) emits: if(blockIdx.x < mBlock) {

if( blockIdx.y < nBlock ) { subspec.codegen(); }}

For the load decomposition, we allocate a temporary array in the required memory hierarchy level at the beginning of the kernel and emit loops to copy the data to the new memory region:

// .load(A, SH, d) emits: for( /* iterate over A */ ) {

// copy elements as specified in d A_SH[...] = A[...] // implementing: Move(A, GL->SH)

} __syncthreads(); subspec.codegen(); // implementation of resulting spec

// if location == SH

Finally, if the residual spec is executable, we emit the associ- ated built-in instruction or micro-kernel (e.g. FMA or dot.cu in Listing 1, respectively).

c. Index Computation Almost every optimization affects the computation of indexes in some way. In Fireiron, index computations for accessing all matrices are calculated and emitted when required. Every application of a decomposition returns a new spec in which we either sliced the operands or moved them to a new memory location. In both cases, these changes need to be considered when generating index expressions for accessing the array elements. For example, when applying tile to the MatMul spec, the following in- dices are computed as expected:

// .tile(mBlock , nBlock) for MatMul: C.rowIndex += rowVar * mBlock; C.colIndex += colVar * nBlock; A.rowIndex += rowVar * mBlock; B.colIndex += colVar * nBlock;

When applying load, a fresh indexing expression for the newly allocated array is generated.

6

4 Expressing Advanced Optimizations In this section, we show how to express advanced optimized strategies by refining the strategy shown in Listing 1.

4.1 Extending Specialized Decompositions

Fireiron’s existing decompositions can easily be extended by the user to express custom ways to decompose a given spec. In this section, we introduce two matrix multiplication specific decompositions (split and epilog). To add a new decomposition to Fireiron, we need to explain how to: a) compute a new sub-spec; b) generate a partial implemen- tation; c) update the index computations for the involved operands.

SplittingtheK-Dimension Formatrixmultiplications,we need to be able to create tiles in the K-dimension. This allows the best use of shared memory, especially for large matrices, where a whole row of the A matrix (or column of B) might not fit into the limited shared memory.

Since the split decomposition is specific for matrix mul- tiplication, it can only be applied to the MatMul spec, and its behavior is described as follows:

mm1 = MatMul(M,N,K)(locA,locB,locC)(level) mm2 = mm1.split(kBlock) // mm2 == MatMul(M,N,kBlock)(locA,locB,locC)(level)

The following partial implementation will be emitted when processing split during code generation:

// .split(kBlock) emits: for(int k = 0; k < kBlock; k++) {

subspec.codegen(); //implementation of sub-spec }

Finally, the index computations are updated as follows:

A.colIndex += k * kBlock; B.rowIndex += k * kBlock;

SpecifyingEfficientEpilogues Thedecompositionshown in Listing 1 did not change the memory location of C. This is because without split, we write only once to C, namely after computing the dot-product of a whole row of A and column of B. In an efficient implementation however, the K-dimension is split into chunks and outer-products are ac- cumulated in registers. Once we finish iterating over the chunks of the K-dimension, every CTA contains the final re- sults of its assigned tile in registers spread across its threads. In the simplest case, every thread stores its results to the required position in global memory. However, depending on the memory layout of the operand matrices, it can be more efficient to cooperate with other threads of the same CTA to accumulate partial results in shared memory, before storing them to global memory.

Fireiron supports the concept of distributed arrays and provides the illusion that we have an indivisible CTA-level matrix C, even though the actual matrix is distributed across

mm = MatMul(M,N,K)(GL,GL,GL)(Kernel) mm .tile(128,128) .to(Block) .epilog(RF,_,_) .split(8) .load(A, SH, _) .load(A, SH, _) .tile(64,32) .to(Warp)

// resulting intermediate specs below // MatMul(128,128,K)(GL,GL,GL)(Kernel) // MatMul(128,128,K)(GL,GL,GL)(Block ) // MatMul(128,128,8)(GL,GL,RF)(Block ) // MatMul(128,128,8)(GL,GL,RF)(Block ) // MatMul(128,128,8)(SH,GL,RF)(Block ) // MatMul(128,128,8)(SH,SH,RF)(Block ) // MatMul(64, 32, 8)(SH,SH,RF)(Block ) ) // MatMul(64, 32, 8)(SH,SH,RF)(Warp 8)(SH,SH,RF)(Warp // MatMul(8, ) 8)(SH,SH,RF)(Thread) // MatMul(8, 1)(SH,SH,RF)(Thread) // MatMul(8, 1)(RF,SH,RF)(Thread) // MatMul(8, 1)(RF,RF,RF)(Thread) // MatMul(8, // MatMul(1, 1)(RF,RF,RF)(Thread) // codegen emits FMA for residual spec

8, 8, 8, 8, 8, 1,

.tile(8,8)

.to(Thread)

.split(1) .load(A, RF, _) .load(B, RF, _) .tile(1,1) .done

Listing 2. Fireiron Decomposition which represents the implementation shown in Figure 1

registers private to each thread. This allows separate decom- positions for storing back the computed results from regis- ters to global memory to implement, for example, the more efficient cooperation via shared memory. Typical libraries cannot offer this kind of composability since we cannot pass this distributed CTA-level matrix to a procedure which im- plements the store because the location of the accumulation registers cannot be taken.

Epilog In order to express advanced decompositions for storing computed results, as well as accumulating interme- diate results in registers, we introduce a new decomposition .epilog(l,i,d). Similar to load, i and d are decomposi- tions. Here, i describes the initialization of a new buffer in location l (usually in registers) used for accumulating the re- sults. The decomposition d describes the implementation of the Move spec which represents storing the results from l to C’s original location (usually global memory). The behavior of epilog is described as:

mm1 = MatMul(M,N,K)(locA,locB,locC)(level) mm2 = mm1.epilog(l,i,d) // mm2 == MatMul(M,N,K)(locA,locB,l)(level)

Since Fireiron’s decomposition language is hierarchical, the subsequent decompositions only need to know the new loca- tion of C. Similar to computing index expressions for load, westartwithafreshindexexpressionforaccessingthenewly allocated buffer. The emitted code snippet for epilog is as follows:

for( /* iterate over M,N */ ) { // init

C_l[...] = 0; }

// initialize buffer in location l

subspec.codegen(); // impl (storing results in C_l) for( /* iterate over M,N */ ) { // store

C[...] = C_l[...]; } // copy elements as specified in d

7

4.2 Advanced Optimization using Refinements

Listing 2 shows how to use the decompositions to express the implementation from Figure 1. A strategy like this al- ready establishes the sizes of data assigned to all levels of the compute and memory hierarchy. In order to generate high-performance kernels, however, we need to specialize all parts of the decomposition to optimally make use of the target hardware.

This is where the traditional approach of optimizing GPU kernelsquicklybecomestedious.Conceptuallytrivialchanges, like changing storage layouts during loads or using inline PTX rather than CUDA, require disproportionate amounts of work since a large fraction of the kernel will need to be rewritten. Fireiron provides easy-to-use refinements to liberate the programmer from these tedious tasks and al- lows them productively focus on achieving the best possible performance.

Refinements are optional modifications to decompositions whichenableadvancedoptimizations.Forexample,to(level) is a refinement we’ve already seen for the tile decomposi- tion. Without this refinement, we generate sequential for- loops; with it however, we assign a specific level of the com- pute hierarchy to the newly created tiles, effectively com- puting them in parallel. In this fashion, Fireiron provides multiple easy-to-use refinements which allow kernels to be gradually fine-tuned to achieve optimal performance.

Tile Refinements The following refinements are available for tile decompositions:

.to(level) assigns the created tiles to the specified level of the compute hierarchy.

.unroll unrolls the generated for-loops. • .layout(l) assigns the tiles to elements of the com- pute hierarchy in either column- or row-major order. This allows the programmer to match the storage lay- out so array accesses are coalesced..

.swizzle(perm) introduces the use of advanced swiz- zle expressions to further optimize the mapping of tiles to elements of the current level of the compute hierarchy.

The layout and swizzle refinments enable changing the mapping of tiles to blocks, warps and threads. They allow the programmer to use different tile shapes for different operations at the same level of the compute hierarchy (such as independent loads of the A and B matrices). This allows advanced optimisations where the assignment of data to threads is more complex than merely column- or row-major.

Load Refinements Fireiron contains the following refine- ments for load decompositions:

.noSyncavoidsemitting__syncthreads()whenload- ing to shared memory, to avoid potentially unneces- sary synchronization.

.storageLayout(l) stores the elements in the desti- nation buffer using either row- or column-major stor- age layout.

.pad(n) allocates n extra columns in the destination buffer, to avoid memory bank conflicts.

.align(n)ensuresaspecificalignmentforthecreated destination buffer.

.reuseBuffer reuses a previously allocated buffer in the same memory location if it is no longer used, to reduce memory usage.

Split Refinements Fireiron also allows the user to define refinements for custom decompositions. This is done by reg- istering the new refinements, including their required code snippets, in the code generator. For the split decomposition, for example, we add two refinements:

.unroll unrolls the created for-loop, like the equiva- lent refinement on tile.

.sync emits __syncthreads() as the last statement in the body of the created for-loop. This may be re- quired depending on how shared memory is used in a particular implementation.

We are aware that some refinements, especially noSync and sync, can allow incorrect implementations due to race con- ditions. However, a decomposition without refinements will always generate correct code. Until now these issues have notcausedproblemsasFireironhasonlybeenusedbyperfor- mance experts. However, we intend to improve the analyses within Fireiron to ensure these refinements cannot cause correctness issues.

4.3 Instructions with varying Granularity

In order to support tensor cores on newer GPUs, we have added new executable specs to Fireiron which represent the specialized MMA (Matrix Multiply Accumulate) operations.

Supporting WMMA The new WMMA-API in CUDA 10.0 introduces warp-wide matrix multiply operations which op- erate on warp-wide register collections called fragments. In order to generate kernels which use the new WMMA API, we extend Fireiron in two ways: First, we extend Fireiron’s memory hierarchy and add a new level Fragment<M,N,K> (parameterized due to the CUDA API) in between shared memory and registers. This allows data to be loaded into the fragments required by the new WMMA operation:

MatMul(16,16,16)(SH,SH,SH)(Warp).load(A, FR<16,16,16>, d) // == MatMul(16,16,16)(FR<16,16,16>,SH,SH)(Warp)

Second, we add three new built-in instructions to Fireiron:

// wmma:mma_sync == MatMul(16,16,16)(FR,FR,FR)(Warp) // using FP16 // wmma::load_matrix_sync == Move(level: Warp,

src: Matrix((M x N), FP16, _, _) dst: Matrix((M x N), FP16, FR _))

1 2 3 4 5 6 7 8 9 10 11 12 13 14

8

val fragment = FR<16,16,16> ///// MATMUL -KERNEL ///////////////////////////////// val simpleWMMA = MatMul ///// BLOCK -LEVEL ///////////////////////////////////

.tile(64, 64).to(Block) .epilog(fragment , Float ,

Move.tile(16, 16).to(Warp).done, // init Move.tile(16, 16).to(Warp).done) // store

.split(16)

///// WARP-LEVEL ////////////////////////////////////

.tile(16, 16).to(Warp) .load(MatMul.a, fragment , Move.done) .load(MatMul.b, fragment , Move.done) .done // => MatMul(16,16,16)(FR,FR,FR)(Warp)

Listing 3. Simple WMMA decomposition describing the implementation of the first cudaTensorCoreGemm kernel shown in the CUDA samples.

// wmma::store_matrix_sync == Move(level: Warp,

src: Matrix((M x N), FP16, FR, _) dst: Matrix((M x N), FP16, _, _))

These small additions allow us to write a simple Fireiron decomposition which uses the WMMA API, as shown in Listing 3. Note that this code does not apply any further decompositions. It computes the matrix multiplication as follows: 1) Assign 64 × 64 elements to a CTA (line 5); 2) Initialize 16 (4 × 4) accumulator fragments (line 7); 3) fill operand fragments (lines 12-13); compute the result (line 14); and store results from fragments to global memory (line 8). Note that we only need to decompose the computation until we reach the warp level because we can generate code for the residual executable spec (line 14) using the built-in wmma::mma_sync instruction.

SupportingHMMA UsingtheHMMAinstructionsexposed via PTX 1 allows even more fine-grained control over how the tensor cores are used. In order to support these instruc- tions,weextendFireironwithexecutablespecswhichexactly describe their semantics:

// HMMA.884.F16.TN exectuable spec MatMul(ComputeHierarchy: Thread ,

A: Matrix((1x4), FP16, RF, RowMajor), B: Matrix((4x1), FP16, RF, ColMajor), C: Matrix((1x8), FP16, RF, ColMajor))

Note the unusal shapes of the operands which are dictated by the semantics of the HMMA instruction.

None of the existing decompositions can be used to create such slices of operands. In order decompose a spec into this executable spec, we need to add an additional mma- specific decomposition. The mmaTile decomposition expects a contiguous 16×16 warp-level MatMul spec and returns an executable HMMA spec.

1https://docs.nvidia.com/cuda/parallel-thread- execution/index.html#warp-level-matrix-instructions-mma

5 Evaluation ToevaluateFireiron,wecomparetheperformanceofourgen- eratedcodeagainstthreereferences:1)amanually-tunedker- nel targeting the Maxwell architecture written by NVIDIA’s GPU performance experts, 2) the publicly available CUDA sample cudaTensorCoreGemm kernel2 targeting the WMMA API, which exploits NVIDIA’s TensorCores on Volta and Turing architectures, and 3) the high-performance GEMM implementations provided in cuBLAS which are written in low-level assembly and are the fastest GEMM implementa- tions available for NVIDIA GPUs today.

We chose this set of comparisons to highlight Fireiron’s capability to generate efficient code for different GPU archi- tectures ranging from older, such as Maxwell, up to state-of- the-art, such as Turing. Furthermore, this set of references includes a wide variety of optimizations which are all ex- pressible using Fireiron. These range from simple tiling and shared memory padding (to avoid bank conflicts), as used in the CUDA sample code, to carefully-tuned swizzles [14] and inline PTX assembly which achieves the highest perfor- mance possible.

We expressed all reference algorithms using decompo- sitions in Fireiron and compare the achieved performance of our generated code on different architectures. Specifi- cally, we used three different GPUs: GeForce GTX 750 Ti (Maxwell), Quadro GV100 (Volta) and GeForce RTX 2080 Ti (Turing), CUDA-10.0, Driver Version 425.00 and compiled all kernels using -O3 --use_fast_math -arch=sm_XX where XX = 52,70, and 75 for Maxwell, Volta, and Turing respec- tively. We locked the clocks to fixed frequencies, report the minimum kernel runtime of 1000 runs using nvprof and omit data transfer time because we are only interested in the quality of our generated kernel code.

5.1 Targeting the Maxwell Architecture

The first kernel we compare against is manually tuned for larger input sizes (M,N,K >= 1024) and optimized to run effi- ciently on the Maxwell architecture. Listing 4 shows the decomposition used to express this specific implementa- tion. Note that we express two different load strategies for prefetching operands A (lines 22–27) and B (lines 29–34) to shared memory. This is due to computing GEMM_NT where one operand is transposed and in order to perform efficient loads, we need to consider the storage layout for both operands such that global memory loads are coalesced. We use advanced swizzle expressions (line 2) shuffling the mapping of data to threads to avoid shared memory load conflicts. Furthermore, we make heavy use of refinements to explicitly specify which loops to unroll and where to add or avoid synchronization. This decomposition also uses vector- ized loads (lines 45 and 48), sparse-thread tiles (line 38) and

2https://github.com/NVIDIA/cuda-samples/blob/master/Samples/ cudaTensorCoreGemm/cudaTensorCoreGemm.cu

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51

9

val swizz: Swizzle = id => // permutation of thread -ids ((id >> 1) & 0x07) | (id & 0x30) | ((id & 0x01) << 3)

// microkernel for epilog -store RF => GL // implements spec: Move(128x128:RF => 128x128:GL) val storeCUDA: String = //* CUDA code snippet *// // MATMUL -KERNEL //////////////////////////////////////// val maxwellOptimized = MatMul ///// BLOCK -LEVEL ///////////////////////////////////////

.tile(128, 128).to(Block)

.layout(ColMajor)

//--- epilog: store results RF => GL ------------------//

.epilog(RF,

Move // init 64 registers per thread

.tile(64, 32).to(Warp) .tile(8, 8).to(Lane) .tile(1, 1).unroll .done,

Move // store results using microkernel

.done(storeCUDA))

.split(8).sync

//--- load A to SH ------------------------------------//

.load(MatMul.a, SH, Move .tile(128, 1).to(Warp) .tile(64, 1).unroll .tile(2, 1).to(Lane) .layout(ColMajor)

.done).toColMajor.noSync

//--- load B to SH ------------------------------------//

.load(MatMul.b, SH, Move .tile(8, 16).to(Warp) .tile(8, 4).unroll .tile(1, 1).to(Lane) .layout(ColMajor)

.done).toRowMajor.pad(4)

///// WARP-LEVEL ////////////////////////////////////////

.tile(64, 32).to(Warp)

///// THREAD -LEVEL //////////////////////////////////////

.tile(Strided((4, 32), (4, 16)))

.to(Lane) .layout(ColMajor) .swizzle(swizz)

.split(1).unroll

//--- load A to RF ------------------------------------//

.load(MatMul.a, RF,

Move.tile(4, 1).unroll.done)

//--- load B to RF ------------------------------------//

.load(MatMul.b, RF,

Move.tile(1, 4).unroll.done)

//--- perform computation -----------------------------//

.tile(1, 1).unroll .done // residual = MatMul(1,1,1)(RF,RF,RF)(Thread)

Listing 4. Efficient decomposition for large input sizes on Maxwell. Optimizations expressed include: vectorized loads, sparse thread-tiles, swizzling, custom epilog micro-kernel.

a custom epilog (line 12) which swizzles the data via shared memory, using an unconventional data-layout, to achieve efficient stores to global memory.

Figure 4 shows the achieved performance relative to the reference kernels (higher is better). We executed both the referenceandtheFireiron-generatedkernels,ontheMaxwell, Volta, and Turing architectures. Our automatically generated code achieves 94.4% of the available performance compared to the manually written CUDA code on Maxwell, as well as 98% and 99% on Volta and Turing respectively. Due to automatic index expression generation, our loops and array indices look slightly different to the hand-written CUDA

Handwritten

00.250.50.751MaxwellVoltaTuring

Fireiron

Figure 4. Comparing Fireiron generated kernel to manually tuned kernel targeting the Maxwell architecture. (computing HGEMM_NT, M=1536, N=1024, K=2048)

code we compared against, and can be further optimised, which explains the remaining gap in performance.

However,duetothetensorcoresintroducedwiththeVolta architecture, this implementation is now only of limited in- terest. The Volta architecture supports the MMA instruction which has an 8× higher theoretical peak performance than the FMA instruction. In fact, we are able to significantly out- perform this specific implementation (up to 5×) by avoiding the FMA instruction and using Fireiron decompositions bet- ter suited to the newer architectures. Similarly, this GEMM implementation only achieves 37% of the performance on Volta and 19% of the performance on Turing when compar- ing to cuBLAS. Still, this comparison highlights Fireiron’s ability to express the exact same optimizations as manual implementations which nonetheless achieve the same per- formance.

5.2 Targeting TensorCores using WMMA

The NVIDIA CUDA samples contain two kernels which use WMMAtoputtheTensorCorestouse.Thefirstkernelsimply introduces the API calls and is not optimized. In fact, the decomposition shown in Section 4.3 generates exactly this kernel. The second kernel is slightly optimized, using tiling and padded shared memory buffers to avoid bank conflicts. Listing 5 shows this implementation expressed as a Fireiron decomposition.

Figure 5 shows the achieved performance for the opti- mized decomposition on both Volta and Turing. Again, our decomposition expresses exactly the optimizations imple- mented by hand in the reference kernel. Therefore, the gener- ated kernel achieves the same performance as the manually written kernel, but the decomposition is much more con- cise than the optimized CUDA code. In order to develop this decomposition, we able to start with the unoptimized de- composition and gradually refine it, focusing on adding one optimization at a time.

Compared to cuBLAS this implementation however still only achieves 61% of the performance on Volta and 68% of the performance on Turing. This is because the memory and compute hierarchy need to be used more efficiently. In particular, using PTX’s mma.sync instruction, instead of the

10

// In the following: FR == WMMA-Fragment // MATMUL -KERNEL ////////////////////////////////////////

val impl = MatMul

///// BLOCK -LEVEL ///////////////////////////////////////

.tile(128, 128).to(Block)

//--- distributed store: FR => GL ---------------------//

.epilog(FR,

Move// init: WMMA-Fragment for C

.tile(64, 32).to(Warp) .tile(16, 16).unroll.done,

Move// store: FR => GL

// FR => SH (first step) .load(Move.src, SH, Move .tile(64, 32).to(Warp) .tile(16, 16).unroll.done

).reuseBuffer // SH => GL (second step) .tile(16, 128).to(Warp) .tile(1, 128).unroll .tile(1, 4).to(Lane) .done)

.split(128).sync.unroll

//--- load A to SH ------------------------------------//

.load(MatMul.a, SH, Move

.tile(16, 128).to(Warp) .tile(2, 128).unroll .tile(1, 8).to(Lane) .done).noSync.pad(8)

//--- load B to SH ------------------------------------//

.load(MatMul.b, SH, Move

.tile(128, 16).to(Warp) .tile(128, 2).unroll .tile(8, 1).to(Lane).layout(ColMajor) .done).pad(8)

///// WARP-LEVEL ////////////////////////////////////////

.tile(64, 32).to(Warp) .split(16).unroll

//--- fill WMMA fragments for A -----------------------//

.load(MatMul.a, FR, Move

.tile(16, 16).unroll.done)

//--- fill WMMA fragments for B -----------------------//

.load(MatMul.b, FR, Move

.tile(16, 16).unroll.done)

//--- perform WMMA computation ------------------------//

.tile(16, 16).unroll .done // MatMul(16,16,16)(FR,FR,FR)(Warp)

Listing 5. Fireiron WMMA Decomposition. Note that we do not descend down to the thread-level as the WMMA- instruction is a warp-wide instruction.

more coarse grained WMMA API, enables delicate control over the TensorCores computation.

5.3 High-Performance HMMA Inline PTX

Finally, we focus on achieving the highest performance pos- sible and compare against cuBLAS, which provides the most efficient GEMM implementations for several architectures and input sizes (written in optimized SASS assembly). We compare against the cublasGemmEx routine using half preci- sion floating-point, so the mma instruction is used on archi- tectures with TensorCores.

We express the implementations by composing Fireiron’s decompositions to use the mmaTile decomposition to target the executable spec for HMMA. cuBLAS uses different CTA- tile sizes depending on the input size. We parameterized our decompositions which allows us to choose different sizes.

Speedup compared to andwritten00.250.50.751VoltaTuring

Fireiron

Handwritten

Figure 5. Comparing Fireiron generated Kernel to the op- timized kernel in the CUDA SDK Samples (cudaTensor- CoreGemm)

FireironcuBLAS

Input Size (M x N x K)Speedup compared to cuBLAS

Figure 6. Relative Performance of Fireiron’s inline PTX De- composition compared to cuBLAS for large input matrices.

Since we are interested in seeing whether Fireiron can ex- press all optimizations required to achieve state-of-the-art performance on new architectures, we explore several input sizes in this experiment. Specifically, we run two separate experiments where we explore small (M,N,K ≤ 1024) and large matrices (1024 ≤ M,N,K ≤ 4096). The optimizations required to achieve high performance on small and large in- put sizes differ significantly, as the small input sizes expose less parallelism opportunities. cuBLAS provides multiple op- timized implementations and chooses a specific one based on internal heuristics. In order to have a fair comparison, instead of only generating one Fireiron kernel, we wrote two parameterized decompositions (one generally more suited for smaller and one for larger input sizes), exhaustively ex- plored CTA-tile sizes (powers of two: 24–28), and report the best performance. Figure 6 shows the achieved performance compared to cuBLAS for the large input matrices (higher is

11

better), and Figure 7 shows the achieved performance for small matrices.

Generally, we are able to significantly increase the per- formance compared to the previous Maxwell- and WMMA- implementations. For large matrices, we exactly match the performance of the carefully tuned SASS kernels used in cuBLAS in three cases. On average, we achieve 93.1% of the cuBLASperformancewithminimumof88.3%inonecaseand a maximum of 101% in two cases. These results show that Fireiron can produce state-of-the-art CUDA kernels which achieve performance very close to the practical peak perfor- mance. This is emphasized by the fact that cuBLAS kernels are provided as optimized SASS assembly, which exposes further optimization opportunities unavailable to Fireiron’s generated CUDA kernels. We left out the decompositions for this experiment for brevity, but none made use of any micro-kernels. Instead, we used mmaTile and the library of executable HMMA specs to inject inline PTX for appropriate residual specs.

For small input sizes (< 1024) cuBLAS typically uses im- plementations where the reduction of the K-dimension is additionally parallelized across warps (usually referred to as in-CTA-split-k). This creates a three dimensional warp ar- rangement and exposes more parallelism in the cases where two dimensional tiles are not enough to saturate all cores. The speedups we achieve for the smallest input sizes are due to the tile sizes we found to work best for this particular setup. We generally found a tile size 16 × 16 in the M and N dimensions and 64 in the K dimension, computed by two warps per CTA, to perform best. The heuristics of cuBLAS also chose 64 for the K dimension, but larger sizes for the M and N dimensions, which reduces the available parallelism required to achieve even better performance.

Developing high-performance kernels in Fireiron allows comfortable experimentation with optimizations. With Fire- iron, developers can solely focus on expressing optimizations while the compiler automates tedious tasks like computing array indices which are easy to get wrong and often need to change throughout the whole kernel. This significantly increases programmer productivity and leads to high-quality GPU code.

6 Related Work Schedule-based Compilers Fireiron is heavily inspired by Halide [15, 16] and TVM [6] in using decompostitions (i.e., scheduling primitives) to express optimizations for specs. Similar frameworks include Tiramisu [3], CHiLL [5], and for graph algorithms GraphIt [25]. Some frameworks also use C’s pragmas and other annotations to create DSLs for manualloopoptimisations[8,11,13].Noneofthese,however, provides neither the same flexibility nor do they allow to decompose existing efficient library routines into reusable components.

Fireiron

cuBLASInput Size (M x N x K)Speedup compared to cuBLAS

Figure 7. Relative Performance of Fireiron’s inline PTX Decomposition compared to cuBLAS for small input matrices

Strategy languages [4, 20, 24] which orchestrate the appli- cation of rewrite rules in term rewriting systems can be seen as predecessors to today’s schedule-based compilers. How- ever, to the best of our knowledge, these languages have not been used in the context of generating efficient GPU code which implements state-of-the-art optimizations and which can compete with the performance of vendor-tuned libraries. Similar analogies can also be drawn between Fireiron and the use of tactics in theorem provers to manually decom- pose proofs into sub-goals [7], though our schedule DSL is not turing-complete and does not allow the same levels of reflection found in these tactic languages.

Auto-Tuning and Program Synthesis Auto-Tuning ap- proachesincludingHalide’sauto-tuners[1,16],OpenTuner[2], ATF [17] and MD-Hom [18], and program synthesis tech- niques such as SwizzleInventor [14] aim to automatically develop optimized implementations by navigating a search space of possible implementations. We see potential for a similar automatic search space exploration for Fireiron‘s de- compositions, however as of today, Fireiron is designed as a tool for performance experts, simplifying the development of optimizations rather than automatically searching for highly optimized implementations.

High-Performance Code Generation Currently, Fireiron providesoptimizedimplementationsforasetofspecs.Lift[10, 19], TensorComprehension [21] and Futhark [12] are frame- works also aiming at high-performance code generation. In contrast to fixed specifications encoding the computations as used in Fireiron, these frameworks allow to specify compu- tations using a flexible high-level (functional) programming language. Rather than simply extending the set of available Fireiron specs we can imagine expressing computations in a similar pattern-based high-level programming language in the future.

PolyhedralCompilers Diesel[9],NOVA[9]andPPCG[23] are compilers making heavy use of optimization via the poly- hedral model. Since most of our decompositions eventually result in nested loops with affine accesses, Fireiron could potentially profit from using polyhedral techniques too, espe- cially as the resulting implementation has a representation similar to Schedule Trees [22]. In contrast to polyhedral optimization techniques however, Fireiron’s decomposition operate on a higher-level of abstraction. Fireiron’s decompo- sitions directly modify specifications which later compile to low-level loops implemented in CUDA.

7 Conclusion In this paper we introduced Fireiron, a scheduling language for high-performance linear algebra on GPUs. We introduced the concept of specifications, which represent a computation to optimize, and decompositions which partially implement them. Defining low-level PTX assembly as well as marco- instructions like WMMA as executable specs allows us to flexibly target new architectures including TensorCores.

Using matrix multiplication as a case study, we showed how to develop high-performance implementations using Fireiron’s specs, decompositions and refinements. Fireiron is expressive enough to support all optimizations typically used in hand-tuned kernels and flexible enough to allow the insertion of micro-kernels when no suitable high-level abstractions can be built easily. Our experimental evalua- tion shows that Fireiron generates code with performance competitive to vendor-tuned high-performance libraries. Fi- nally, all Fireiron programs are composed of building blocks which can be reused in future implementations targeting new hardware architectures, allowing these optimisations to be applied more widely.

12

References [1] Andrew Adams, Karima Ma, Luke Anderson, Riyadh Baghdadi, Tzu- Mao Li, Michaël Gharbi, Benoit Steiner, Steven Johnson, Kayvon Fata- halian, Frédo Durand, and Jonathan Ragan-Kelley. 2019. Learning to optimize halide with tree search and random programs. ACM Trans. Graph. 38, 4 (2019), 121:1–121:12. https://doi.org/10.1145/3306346. 3322967

[2] Jason Ansel, Shoaib Kamil, Kalyan Veeramachaneni, Jonathan Ragan- Kelley,JeffreyBosboom,Una-MayO’Reilly,andSamanP.Amarasinghe. 2014. OpenTuner: an extensible framework for program autotuning. In International Conference on Parallel Architectures and Compilation, PACT ’14, Edmonton, AB, Canada, August 24-27, 2014. 303–316. https: //doi.org/10.1145/2628071.2628092

[3] Riyadh Baghdadi, Jessica Ray, Malek Ben Romdhane, Emanuele Del Sozzo, Abdurrahman Akkas, Yunming Zhang, Patricia Suriana, Shoaib Kamil, and Saman P. Amarasinghe. 2019. Tiramisu: A Polyhedral Compiler for Expressing Fast and Portable Code. In IEEE/ACM In- ternational Symposium on Code Generation and Optimization, CGO 2019, Washington, DC, USA, February 16-20, 2019. 193–205. https: //doi.org/10.1109/CGO.2019.8661197

[4] Peter Borovanský, Claude Kirchner, Hélène Kirchner, and Christophe Ringeissen. 2001. Rewriting with Strategies in ELAN: A Functional Semantics. Int. J. Found. Comput. Sci. 12, 1 (2001), 69–95. https: //doi.org/10.1142/S0129054101000412

[5] Chun Chen, Jacqueline Chame, and Mary Hall. 2008. CHiLL: A frame- work for composing high-level loop transformations. Technical Report. Citeseer.

[6] Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Q. Yan, Haichen Shen, Meghan Cowan, Leyuan Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin, and Arvind Krishnamurthy. 2018. TVM: An Automated End-to-End Optimizing Compiler for Deep Learning. In 13th USENIX Symposium on Operating Systems Design and Implemen- tation, OSDI 2018, Carlsbad, CA, USA, October 8-10, 2018. 578–594. https://www.usenix.org/conference/osdi18/presentation/chen

[7] David Delahaye. 2000. A Tactic Language for the System Coq. In Logic for Programming and Automated Reasoning, 7th International Conference, LPAR 2000, Reunion Island, France, November 11-12, 2000, Proceedings. 85–95. https://doi.org/10.1007/3-540-44404-1_7

[8] Sébastien Donadio, James C. Brodman, Thomas Roeder, Kamen Yotov, Denis Barthou, Albert Cohen, María Jesús Garzarán, David A. Padua, and Keshav Pingali. 2005. A Language for the Compact Representation of Multiple Program Versions. In Languages and Compilers for Parallel Computing, 18th International Workshop, LCPC 2005, Hawthorne, NY, USA, October 20-22, 2005, Revised Selected Papers. 136–151. https: //doi.org/10.1007/978-3-540-69330-7_10

[9] Venmugil Elango, Norm Rubin, Mahesh Ravishankar, Hariharan San- danagobalane, and Vinod Grover. 2018. Diesel: DSL for linear algebra and neural net computations on GPUs. In Proceedings of the 2nd ACM SIGPLAN International Workshop on Machine Learning and Program- ming Languages, MAPL@PLDI 2018, Philadelphia, PA, USA, June 18-22, 2018. 42–51. https://doi.org/10.1145/3211346.3211354

[10] Bastian Hagedorn, Larisa Stoltzfus, Michel Steuwer, Sergei Gorlatch, and Christophe Dubach. 2018. High performance stencil code gen- eration with lift. In Proceedings of the 2018 International Symposium on Code Generation and Optimization, CGO 2018, Vösendorf / Vienna, Austria, February 24-28, 2018. 100–112. https://doi.org/10.1145/3168824 [11] Albert Hartono, Boyana Norris, and Ponnuswamy Sadayappan. 2009. Annotation-based empirical performance tuning using Orio. In 23rd IEEE International Symposium on Parallel and Distributed Processing, IPDPS 2009, Rome, Italy, May 23-29, 2009. 1–11. https://doi.org/10.1109/ IPDPS.2009.5161004

[12] Troels Henriksen, Niels G. W. Serup, Martin Elsman, Fritz Hen- glein, and Cosmin E. Oancea. 2017. Futhark: purely functional GPU- programming with nested parallelism and in-place array updates. In

13

Proceedings of the 38th ACM SIGPLAN Conference on Programming Lan- guage Design and Implementation, PLDI 2017, Barcelona, Spain, June 18-23, 2017. 556–571. https://doi.org/10.1145/3062341.3062354

[13] Michael Kruse and Hal Finkel. 2018.

A Proposal for Loop- Transformation Pragmas. In Evolving OpenMP for Evolving Architec- tures - 14th International Workshop on OpenMP, IWOMP 2018, Barcelona, Spain, September 26-28, 2018, Proceedings. 37–52. https://doi.org/10. 1007/978-3-319-98521-3_3

[14] Phitchaya Mangpo Phothilimthana, Archibald Samuel Elliott, An Wang, Abhinav Jangda, Bastian Hagedorn, Henrik Barthels, Samuel J. Kaufman, Vinod Grover, Emina Torlak, and Rastislav Bodík. 2019. Swizzle Inventor: Data Movement Synthesis for GPU Kernels. In Proceedings of the Twenty-Fourth International Conference on Archi- tectural Support for Programming Languages and Operating Systems, ASPLOS 2019, Providence, RI, USA, April 13-17, 2019. 65–78. https: //doi.org/10.1145/3297858.3304059

[15] Jonathan Ragan-Kelley, Andrew Adams, Sylvain Paris, Marc Levoy, Saman P. Amarasinghe, and Frédo Durand. 2012. Decoupling al- gorithms from schedules for easy optimization of image process- ing pipelines. ACM Trans. Graph. 31, 4 (2012), 32:1–32:12. https: //doi.org/10.1145/2185520.2185528

[16] Jonathan Ragan-Kelley, Connelly Barnes, Andrew Adams, Sylvain Paris, Frédo Durand, and Saman P. Amarasinghe. 2013. Halide: a language and compiler for optimizing parallelism, locality, and recom- putation in image processing pipelines. In ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI ’13, Seattle, WA, USA, June 16-19, 2013. 519–530. https://doi.org/10.1145/2491956. 2462176

[17] Ari Rasch, Michael Haidl, and Sergei Gorlatch. 2017. ATF: A Generic Auto-Tuning Framework. In 19th IEEE International Conference on High Performance Computing and Communications; 15th IEEE Interna- tional Conference on Smart City; 3rd IEEE International Conference on Data Science and Systems, HPCC/SmartCity/DSS 2017, Bangkok, Thailand, December 18-20, 2017. 64–71. https://doi.org/10.1109/ HPCC-SmartCity-DSS.2017.9

[18] Ari Rasch, Richard Schulze, and Sergei Gorlatch. 2019. Developing High-Performance, Portable OpenCL Code via Multi-Dimensional Homomorphisms. In Proceedings of the International Workshop on OpenCL, IWOCL 2019, Boston, MA, USA, May 13-15, 2019. 4:1. https: //doi.org/10.1145/3318170.3318171

[19] Michel Steuwer, Toomas Remmelg, and Christophe Dubach. 2017. Lift: a functional data-parallel IR for high-performance GPU code generation. In Proceedings of the 2017 International Symposium on Code Generation and Optimization, CGO 2017, Austin, TX, USA, February 4-8, 2017. 74–85.

[20] Mark van den Brand, Arie van Deursen, Jan Heering, H. A. de Jong, Merijn de Jonge, Tobias Kuipers, Paul Klint, Leon Moonen, Pieter A. Olivier, Jeroen Scheerder, Jurgen J. Vinju, Eelco Visser, and Joost Visser. 2001. The ASF+SDF Meta-environment: A Component-Based Lan- guage Development Environment. In Compiler Construction, 10th In- ternational Conference, CC 2001 Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2001 Genova, Italy, April 2-6, 2001, Proceedings. 365–370. https://doi.org/10.1007/ 3-540-45306-7_26

[21] Nicolas Vasilache, Oleksandr Zinenko, Theodoros Theodoridis, Priya Goyal, Zachary DeVito, William S. Moses, Sven Verdoolaege, Andrew Adams, and Albert Cohen. 2018. Tensor Comprehensions: Framework- Agnostic High-Performance Machine Learning Abstractions. CoRR abs/1802.04730 (2018). arXiv:1802.04730 http://arxiv.org/abs/1802. 04730

[22] Sven Verdoolaege, Serge Guelton, Tobias Grosser, and Albert Cohen. 2014. Schedule Trees. In Proceedings of the 4th International Workshop on Polyhedral Compilation Techniques, Sanjay Rajopadhye and Sven Verdoolaege (Eds.). Vienna, Austria.

[23] Sven Verdoolaege, Juan Carlos Juega, Albert Cohen, José Ignacio Gómez, Christian Tenllado, and Francky Catthoor. 2013. Polyhedral parallel code generation for CUDA. TACO 9, 4 (2013), 54:1–54:23. https://doi.org/10.1145/2400682.2400713

[24] Eelco Visser, Zine-El-Abidine Benaissa, and Andrew P. Tolmach. 1998. Building Program Optimizers with Rewriting Strategies. In Proceed- ings of the third ACM SIGPLAN International Conference on Functional Programming (ICFP ’98), Baltimore, Maryland, USA, September 27-29, 1998. 13–26. https://doi.org/10.1145/289423.289425

[25] Yunming Zhang, Mengjiao Yang, Riyadh Baghdadi, Shoaib Kamil, Julian Shun, and Saman P. Amarasinghe. 2018. GraphIt: a high- performance graph DSL. PACMPL 2, OOPSLA (2018), 121:1–121:30. https://doi.org/10.1145/3276491

14