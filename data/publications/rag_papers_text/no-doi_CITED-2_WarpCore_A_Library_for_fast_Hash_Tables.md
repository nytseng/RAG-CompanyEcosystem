0 2 0 2

v o N 1 1

]

C D . s c [

2 v 4 1 9 7 0 . 9 0 0 2 : v i X r a

© 2020 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes,creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.

WarpCore: A Library for fast Hash Tables on GPUs

Daniel Jünger∗, Robin Kobus∗, André Müller∗, Christian Hundt†, Kai Xu‡, Weiguo Liu‡, Bertil Schmidt∗ ∗ Institute of Computer Science, Johannes Gutenberg University, Mainz, Germany Email: {juenger, kobus, muellan, bertil.schmidt}@uni-mainz.de † NVIDIA AI Technology Center, Luxembourg, Luxembourg, Email: chundt@nvidia.com ‡ School of Software, Shandong University, Jinan, China, Email: {xukai16@mail., weiguo.liu@}sdu.edu.cn

Abstract—Hash tables are ubiquitous. Properties such as an amortized constant time complexity for insertion and querying as well as a compact mem- ory layout make them versatile associative data struc- tures with manifold applications. The rapidly growing amount of data emerging in many ﬁelds motivated the need for accelerated hash tables designed for mod- ern parallel architectures. In this work, we exploit the fast memory interface of modern GPUs together with a parallel hashing scheme tailored to improve global memory access patterns, to design WarpCore – a versatile library of hash table data structures. Unique device-sided operations allow for building high performance data processing pipelines entirely on the GPU. Our implementation achieves up to 1.6 billion inserts and up to 4.3 billion retrievals per second on a single GV100 GPU thereby outperforming the state- of-the-art solutions cuDPP, SlabHash, and NVIDIA RAPIDS cuDF. This performance advantage becomes even more pronounced for high load factors of over 90%. To overcome the memory limitation of a single GPU, we scale our approach over a dense NVLink topology which gives us close-to-optimal weak scaling on DGX servers. We further show how WarpCore can be used for accelerating a real world bioinformatics application (metagenomic classiﬁcation) with speedups of over two orders-of-magnitude against state-of-the- art CPU-based solutions. We plan to make our library publicly available upon acceptance of the paper.

Garcia et al. [6], and StadiumHash [7] were among the ﬁrst to investigate hash map construction on GPUs proposing static implementations (i.e., no pairs can be added/deleted to an already constructed table) using one thread per key- value pair. More recent approaches including cuDF [8] (part of NVIDIA’s RAPIDS framework), SlabHash [9], and HashGraph [10] are more ﬂexible but are often limited in terms of performance or memory overhead.

We propose WarpCore (WC), a highly eﬃcient yet ﬂexible library of hash data structures and algorithms that can achieve high performance for a variety of use cases. Our approach can achieve robust and often superior runtime performance even for very high load factors and storage densities. The probing scheme is based on our previous WarpDrive method [11] but eliminates its limita- tion to 32-bit single-value hash-tables. This is achieved by introducing a number of novel GPU-based data structures and associated algorithms within a versatile framework. Our detailed contributions are:

1) The design of 32-bit and 64-bit massively-parallel single-value and multi-value hash table implementa- tions with associated insertion/retrieval/deletion al- gorithms that allow for the ﬂexible exchange of un- derlying data layouts.

Index Terms—GPUs, hash tables, bioinformatics

I. Introduction

Hash tables are frequently used for storing key-value pairs in-memory because of their compact data layout and expected constant time complexity for insertion and re- trieval. They are key data structures for bioinformatics [1], computational geometry [2], and deep learning [3]. This motivates the need for developing optimized implementa- tions to support hash tables on modern architectures.

2) Host-sided and device-sided interfaces which enable high-throughput batch operations as well as concur- rent processing of individual elements inside CUDA kernels.

3) We propose a novel memory-compact bucket list hash table with an associated dynamic growth scheme. 4) We present techniques for concurrent execution of hash table operations and for the eﬃcient usage of multiple GPUs.

Common CPU-based hash table implementations such as tbb::concurrent_hash_map from the Thread Build- ing Blocks (TBB) library or std::unordered_map from the C++ standard library suﬀer from poor throughput induced by highly irregular memory access patterns during probing. State-of-the-art accelerators may overcome this limitation by virtue of their fast high bandwidth memory (HBM2) and massive parallelism.

5) We show how WC can be used for bioinformatics (metagenomic classiﬁcation).

The rest of this paper is organized as follows. Section II provides some necessary background information. Related work is reviewed in Section III. The design of WC is presented in Section IV. Performance is evaluated in Sec- tion V. Section VI concludes the paper.

II. Background

Consequently, a number of approaches have been de- signed for GPU-accelerated hashing using various probing schemes and memory access techniques. cuDPP [4], [5],

Hash maps are a class of data structures, that given a key k from a sparse domain K, enable constant-time lookup of value v ∈ V associated with that key thereby

modelling functional dependencies f : K → V , k 7→ f(k) := v. They avoid the memory overhead associated with dense look-up tables which hold memory for values associated with every possible key k ∈ K by using a hash function h : K → I , k 7→ h(k) := i, mapping each key to a distinct memory index i ∈ I.

The complete set of keys K is usually not known in advance which precludes the construction of a bijective mapping between K and I, e.g., by using minimal perfect hash functions. For that reason and also due to perfor- mance considerations, a hash function h is usually chosen to be non-injective thereby introducing potential index collisions h(k) = h(k0) for two distinct keys k,k0 ∈ K. The most prevalent strategies for resolving such hash collisions are Separate Chaining (SC) and Open Addressing (OA). SC stores keys that map to the same hash h(k) = i in a data structure tied to index i. This can either be a ﬁxed array, a dynamic array, a linked list of contiguous chunks or a linked list of single elements. However, chain- ing shows several characteristics that are undesirable in the context of parallelization. Linked lists usually involve cache-ineﬃcient random access and require extra memory for pointers while using ﬁxed-size arrays may lead to substantial memory over-subscription due to unused slots. Furthermore, lock-free insertion and deletion of nodes in linked lists can be error-prone due to pitfalls like the ABA problem and priority inversion.

With OA colliding keys are stored in select locations taken from a sequence of candidate positions which are computed by a deterministic probing scheme. This ap- proach is in general better suited for realizing eﬃcient, lock-free updates and also for reasoning about their cor- rectness. It is therefore often preferred for implementing concurrent hash tables. We also opted for OA as hash conﬂict resolution technique for the same reasons.

A deterministic probing scheme generates a sequence s(k,l) of candidate positions for storing a key k, where l denotes the number of probing attempts. Probing starts at the initial position s(k,0) = h(k) and continues as long as the candidate position is already occupied by another key or some abort criterion is met (e.g., all slots of the table have been visited). The probing sequences of three prevalent schemes can be given as follows (c = |I| denotes the capacity of the hash table):

Linear Probing (LP): s(k,l) = (cid:0)h(k) + l(cid:1)modc • Quadratic Probing (QP): s(k,l) = (cid:0)h(k) + l2(cid:1)modc • Double Hashing (DH): s(k,l) = (cid:0)h(k)+l·g(k)(cid:1)modc While LP is cache-eﬃcient, it tends to produce densely occupied regions that lead to a high variance in re- quired probing length per key. This becomes especially pronounced when the number of inserted elements n approaches the hash map capacity, i.e., its load factor α = n c is high. QP and DH avoid this so-called primary clustering using larger step sizes at the cost of more cache misses. Extensions of these probing schemes have been

proposed, among others Cuckoo Hashing [4] and Robin Hood Hashing [12].

Fully featured CPU-based hash map implementations such as std::unordered_map from the C++11 standard library support on-demand resizing in case the number of inserted elements n exceeds the capacity c. A common strategy is to reinsert all data into a new hash map instance if the load factor reaches a critical threshold, e.g. α > 90%. These implementations typically also allow for the insertion of keys and values of arbitrary sizes. In case of concurrent table updates, modiﬁcations of each individual slot have to be serialized either by locking them with slow global mutexes or more eﬃcient compare-and-swap (CAS) operations. We focus on the latter. While this allows to issue concurrent inserts and queries without violating the integrity of the hash map, the outcome may depend on the actual execution order of the operations.

While x86_64 CPUs support CAS instructions for up to 128 consecutively stored bits, CUDA-enabled devices are limited to 64-bit words. Thus, packing key-value pairs (k,v) into 64 bits enables the eﬃcient use of CAS op- erations on an Array of Structs (AOS) memory layout. For larger keys and values, one can limit the CAS to the key slot of the struct or alternatively store keys K and values V separately as Struct of Arrays (SOA). These variants use relaxed reads and writes to the value slots which might introduce priority inversion in case of simultaneously inserting distinct values for the same key. Whereas an AOS layout provides relatively high cache locality if both key and value of a slot are accessed, the eﬀect reverses if we only access the key of each slot. In this case the values stored next to each key reduce the eﬀective cache line size. This is especially critical if the value type is large compared to the key type.

III. Related Work

Several data-parallel GPU hash table implementations have been proposed which aim to leverage the fast memory bandwidth provided by modern GPUs. Lessley et al. [13] provide a comprehensive survey of these approaches and highlight the respective concepts and techniques used.

Alcantara et al. [4] were among the ﬁrst GPU hash table implementations as part of the cuDPP library. Their initial approach employs a two-stage table construction where keys are initially hashed into buckets of equal size residing in global memory. Collisions are resolved with a third degree cuckoo hashing scheme. Subsequently, the same authors proposed a single-pass variant [5] based on fourth degree cuckoo hashing which supports load factors of roughly 80% achieving an insertion performance of up to 250 million inserts per seconds on a GTX 470. cuDPP is limited to 32-bit wide types for both key and value. Also, tables are static, i.e., adding new key-value pairs to an already constructed table requires rebuilding the whole data structure.

CoherentHash [6] introduces a data-parallel implemen- tation of an OA single-value hash table using Robin Hood hashing by augmenting each key with an additional 4-bit age indicator which trades the additional memory over- head with a lower on-average probing length. It uses one thread for the lock-free insertion of a key-value pair using atomic CAS intrinsics and achieves comparable speed to cuDPP.

StadiumHash [7] employs an OA strategy where the hash table itself may either reside in the GPU’s global memory or inside host memory. A so-called ticket board residing in video memory is used to track slot occupation. It maintains a single bit indicating the slot’s availabil- ity together with a small number of optional bits used as a signature of the key stored inside the slot. If the full hash map can be kept in GPU global memory the performance of StadiumHash is between 1.04x to 1.19x faster than cuDPP on a GTX780 GPU at an average load factor of 80%. In the case that the hash table is stored in host memory, i.e., out-of-core, the performance drops to around 100 million inserts per second restricted by the PCIe interconnect. In order to better ﬁt the GPU’s SIMT execution model, StadiumHash employs a warp- cooperative work-sharing strategy, utilizing idling threads to cooperate in queued table operations. Since only the ticket board has to be updated atomically, StadiumHash technically imposes no restrictions on the respective data types for keys and values. However, the auxiliary ticket board implies additional memory overhead as well as additional random memory accesses per operation. Phase- concurrent operations are guarded via exceptionally slow global device- or even system-wide barriers.

cuDF [8] is part of NVIDIA’s RAPIDS framework [14] for manipulating columnar data frames on CUDA-enabled accelerators and also provides a data-parallel hash table implementations. Similar to cuDPP, table construction is static and does not allow for subsequent or phase- concurrent insertions of new key-value pairs. To the best of our knowledge, cuDF employs the only available multi- value GPU hash table. However, their chosen linear prob- ing scheme suﬀers from primary and secondary clustering eﬀects for input distributions featuring many values per key, degrading performance signiﬁcantly for these cases.

introduces a dynamic GPU hash table which follows the concept of SC as its collision resolution strategy. The table consists of an array of linked lists, each of which represents a chain of equally sized memory units, called slabs, that store collided keys during insertion. Each slab has a size roughly corresponding to that of a single cache line (128 bytes) and consists of multiple consecutive key-value slots and a single pointer to its successor slab. SlabHash provides bulk operations which are executed us- ing a warp-cooperative work-sharing strategy, where each CUDA thread inside a warp is assigned a distinct table operation such as insertion, retrieval, or deletion, which are then, one-by-one, executed cooperatively by all lanes

SlabHash [9]

inside the warp, ensuring memory coalescing. Dynamic slab allocation during execution is realized through a specialized memory pool. For bulk operations, they report 512 (937) million operations per second for insertion (re- trieval) on a Tesla K40c GPU, respectively. Compared to cuDPP, SlabHash consistently achieves a lower throughput of insertions per second. SlabHash achieves higher query throughput only when the average number of slabs per list is less than one. Over all conﬁgurations, cuDPP attains the better query throughput. However, on a newer Tesla V100 GPU, they consistently outperform cuDPP. As stated in the corresponding manuscript, SlabHash supports single- value, as well as multi-value scenarios. However, we found that the building blocks provided by the corresponding code repository [15], were not suﬃcient to implement a multi-value retrieve operation.

HashGraph [10] handles hash-collisions with neither OA nor SC, but proposes a table construction method that is highly similar to a compressed sparse row matrix layout. HashGraph currently only supports static table builds, which again implies a lack of support for phase-concurrent workﬂows. Furthermore, the approach has high memory overhead since it requires 3n auxiliary memory during table construction with n input key-value pairs.

Note that none of the above mentioned implementations feature out-of-the-box multi-GPU support. With WC we introduce a framework for constructing GPU hash tables that can overcome the aforementioned shortcomings of existing solutions while outperforming the state-of-the-art.

IV. Implementation

Our aim is the design of a versatile library for creating accelerated hash table data structures on CUDA-enabled GPUs. WC provides optimized GPU implementations for the following data structures:

HashSet: stores set of keys; each key occurs only once • SingleValueHashTable: stores key-value pairs; each key occurs only once

MultiValueHashTable: stores key-value pairs; same key may occur multiple times (with diﬀerent values) • BucketListHashTable: stores all values associated with the same key in a linked list of buckets

CountingHashTable: counts distinct key occurrences • BloomFilter: answers set membership queries In this paper, we focus on the three highlighted types. The remaining types are built based on the same underly- ing principles. We now discuss some general library design features (IV-A), single-value and multi-value hash table layout, parallel probing scheme, and associated operations (IV-B), our memory-compact bucket list (IV-C), concur- rent execution (IV-D), and multi-GPU support (IV-E), A. General Library Design Features

1) Modularity: We provide building blocks that can be used to customize the basic data structures mentioned above and to create completely new one. Interchangeable

kckeysvalues

k2

k1

AoS…

k1v1

memoryadressing

k1v1

packedAoS…

v2

v1

SoA…:atomicwrite(≤ 8bytes)pairs

:relaxedwrite

k2v2

kcvc

k2v2

kcvc

vc…pairs

Fig. 1: SOA, AOS, and packed AOS memory layout of a key-value store with c slots.

parts include memory layout abstractions for switching between AOS and SOA, diﬀerent hash functions and probing schemes.

2) Host-sided and Device-sided Interfaces: The data structures in our library provide host-callable table op- erations which take input batches, enabling billions of independent table operations per second. We complement them with device-sided counterparts that work on single table elements. This enables the building of pipelines where emitting key-value pairs, inserting them into a hash table and/or querying can be fused into monolithic CUDA kernels, avoiding costly global memory operations for intermediate results. B. Open Addressing Hash Table

1) Memory Layout: Our basic OA hash table consists of contiguous arrays residing in global GPU memory in either AOS or SOA layout, i.e., one array for holding aggregates composed of a key and a value member, or alternatively two arrays of the same length where the ﬁrst holds the keys and the second holds the corresponding values. The array size determines the maximum number of key-value pairs (capacity) the hash table can hold. We initialize each key slot with an empty-indicator ke in order to distinguish empty slots from occupied ones during probing. For the case that both key and value data types do not exceed a width of 32 bits, we provide a packed AOS layout, where a key-value pair is bit-packed into a single 64-bit unsigned integer. This allows for storing both key and value by using a single atomic CAS operation instead of an initial atomic swap of the key into its target slot followed by a relaxed store of the value. Figure 1 illustrates the three supported memory layouts.

2) Parallel Probing Scheme: A naïve approach assigns each key to its own CUDA thread. However, since each key typically follows a diﬀerent probing sequence this would lead to non-coalesced global memory accesses. An alternative approach could use an entire warp of 32 threads per input key k, such that each thread with lane ID t probes a diﬀerent hash table position h(k,t) mod c. If any

thread ﬁnds a matching slot it can signal the other threads in the warp to terminate probing via fast register vote intrinsics. However, this approach is only beneﬁcial if the hash table positions {h(k,0) mod c,...,h(k,31) mod c} fall within the same memory region, enabling threads in a warp to share the same cache line. The only known probing scheme that meets this constraint is LP which suﬀers from primary clustering.

Thus, we rely on a hybrid approach, called Cooperative Probing Scheme (COPS) consisting of an inner intra- warp probing scheme combined with outer probing based on DH. The inner scheme is based on LP and ensures data locality between threads inside a warp. The outer probing scheme determines the starting index oﬀset for the inner scheme. The resulting local probing sequence of a 32c) + 0(cid:1) mod warp for the ith probing attempt is {(cid:0)h(k,b i 32c) + 31(cid:1) mod c}. DH features both low c,...,(cid:0)h(k,b i probing lengths and fairly uniform slot occupation pat- terns within the table. Additionally, we maintain DH’s property of cycle-freeness by selecting c = p · 32, where p is prime whilst ensuring that the second hash function generates step sizes as multiples of 32.

Assuming a uniform distribution of populated slots and a load factor of 90%, every tenth slot would be empty on average. Thus, it would be likely that an empty slot can be found by a group of less than 32 threads at the ﬁrst probing attempt. This motivates the usage of sub-warp tiling based on CUDA’s Cooperative Group (CG) feature which enables us to use thread groups of sizes 1, 2, 4, 8, 16, or 32.

Figure 2 depicts the insertion of a key-value pair (k,v) into a hash table with a CG size of 4 based on seven steps:

(1) The outer probing scheme is used to determine the

initial probing index.

(2) Each thread in a CG loads one key slot from global

memory in coalesced fashion.

(3) Each thread checks whether its assigned slot is a potential candidate for inserting (k,v) and commu- nicates its result via a fast in-register group vote. (4) The thread associated with the lowest candidate slot

index is selected.

(5) If there are no candidate slots (left column in Fig- ure 2) steps 1 to 4 are repeated until a suitable one is found.

(6) We try an atomic CAS of the key into the selected candidate slot. If it fails (due to a collision with a successful insertion by another thread), we repeat steps 4 and 6 until the CG has no candidate slots left. In this case we start from Step 5.

(7) If the key was inserted successfully in Step 6, a relaxed

store operation is issued to write the value.

Probing with variable CG sizes inside the same table can be accomplished by setting the inner probing window to a ﬁxed size, e.g. 32. Smaller groups iterate over said window in a linear fashion before continuing with the outer

k

keysvaluescooperativegroup

h(k,[0-3])modch(k,[4-7])modc

hit

coalescedload

0

0

0

0

groupvoting

0

0

0

0

determineleader

0

0

1

1

0

0

1

0

0

0

1

1

0

0

0

1

atomicCASk

atomicCASkfail

failsuccess!nohit!hit

1

2

5

7

6storev

3

4

success!

storev

Fig. 2: Insertion of a key-value pair (k,v) into a hash table with capacity c using COPS with an outer probing scheme h, an inner probing window size of 4 and a CG size of 4.

probing scheme, which ensures probing consistency for all group sizes.

3) Insertion: Inserting a new key-value pair is accom- plished by using COPS for both single-value and multi- value context. For a single-value hash table, an additional warning is issued if the key currently being probed for is already present. While the device-sided function inserts a single key-value pair into the table and is executed inside a CG, the host-callable batch operation consists of a data-parallel CUDA kernel. For a batch insertion of n key-value pairs we start a kernel consisting of n · g many threads, where g denotes the CG size each query is executed in. Each CG in the grid is assigned to a single pair and calls the corresponding device-sided insert function, implementing a data-parallel scheme over the input batch. 4) Retrieval: Retrieval relies on the same scheme but instead of probing for an empty slot, we look for slots that hold the queried key. Search can terminate when we encounter an empty slot before ﬁnding the queried key, since COPS guarantees that any key is inserted at its lowest possible index in the probing sequence. The device-sided retrieval function takes a query along with a CG in which the operation should be executed. The host-sided function reads a batch of keys from global memory and writes the retrieved values to a user-allocated output array on the device. In the single-value case, the number of returned values cannot exceed the number of queried keys and probing can stop after the ﬁrst value of a query is found. In the multi-value case the number of values associated with a query is not known in advance. Thus, if all retrieved values should be written to memory, the size of the output array has to be determined in a separate counting pass beforehand. The retrieval of all values associated with a batch of n queries requires an additional temporary array of size n+1 storing the oﬀsets

of the per-key value segments in the output array. The oﬀset array is computed using a preﬁx sum over the number of values per query.

In some cases it is suﬃcient to process the val- ues associated with each key one-at-a-time on the de- vice instead of copying the retrieved values of a host- sided batch query into a distinct new location in global device memory. WC’s data structures provide higher- order member functions for_each(keys,callback) and for_all(callback) which take a device-sided callback function (object), e.g., a device-sided lambda function. The callback is invoked in parallel for each query found in the table during probing and receives the corresponding key-value pair and the key’s index.

5) Deletion: Deleting keys is accomplished by overwrit- 6= ke. During ing the table slot with a tombstone kt insertion, a slot with a tombstone is treated as a regular empty slot which can be re-populated with a new key-value pair. During retrieval, it is interpreted as a populated slot. C. Bucket List Hash Table

Due to the relatively small amount of available video memory, eﬀective memory utilization often plays a cru- cial role. We deﬁne the storage density ρ of a container data structure holding data elements, as the amount of stored information bits over the total amount of memory allocated by the container. For single-value OA hash table designs ρ is equivalent to the table’s load factor α, i.e. the number of occupied key-value slots over the number of allocated slots. However, if the same key occurs more than once it is stored multiple times, thereby degrading storage density. For use cases where this is undesirable, like in Section V-C, we provide an alternative multi-value hash table which links all values to a single instance of the corresponding key.

Our bucket list hash table uses a single-value hash table with a primary list handle as value. Actual values are stored in linked lists of contiguous memory chunks called buckets. The list handle is a 64-bit packed, atom- ically updatable data structure consisting of three ﬁelds: a pointer to the last list node associated with a key, the total number of values per key and 2 bits indicating one of four possible states (uninitialized, blocked, ready, full). Transitions between states are guarded by atomic CAS operations on the primary list handle ensuring that list operations are linearizable.

The leading slot of each but the ﬁrst bucket consists of a reference that points to the previous bucket in the list, followed by the actual value slots. Since the exact distribution of values per key is usually unknown in ad- vance, we propose the following growth strategy. When a key is inserted into the hash table for the ﬁrst time, its initial value bucket of size s0 is allocated. Subsequent bucket sizes are set to si = dλ·si−1e where λ ≥ 1 denotes the bucket growth factor. Figure 3 shows an example using growth parameters s0 = 1 and λ = 2. If the input data

6

v6

hashtable

v4

v5

k…………

bucketlists

v3values

keyshandles

v1

v2

Fig. 3: Example of a bucket list storing six values asso- ciated with key k. Keys are stored in a single-value hash table together with a handle to the associated bucket list that holds a reference to the last bucket and the total number of values inside the list.

distribution is known both parameters can be used to adapt the growth strategy for improved memory eﬃciency. Since global memory allocations would act as a device- wide barrier, memory for buckets is pre-allocated as a single contiguous array which serves as a memory pool.

Inserting a key-value pair starts with probing for the key in the single-value hash table. If the key is not already present, we insert it into the hash table and allocate its ﬁrst value bucket. One thread atomically marks the associated list handle as blocked, thereby ensuring that is has exclusive access to the value list, and subsequently requests a new bucket from the memory pool. If successful, the value is appended to the list and the list’s handle is unblocked. Other threads that encounter a blocked handle implement a busy waiting strategy with exponential back- oﬀ until the handle has been unblocked. In case the key is already present in the table, we check if the current tail bucket has any empty value slots available. If true, we try to reserve a slot inside the bucket by an atomic increment of the list handle’s value counter. If the atomic CAS operation is successful, we write the value to the reserved slot and terminate. However, if this operation fails due to another thread successfully inserting a new value concurrently, we reload the altered handle from memory and repeat until insertion has succeeded. If the current tail bucket is full, we attempt to block the handle and request a new bucket from the memory pool.

As shown in Figure 4 retrieval of a batch of keys is done by probing for each key in parallel. If a key is found, threads in the current CG begin following the bucket list references until reaching the initial bucket. Values are read from the buckets using as many threads from the current CG as possible, thereby enabling coalesced access for suﬃciently large buckets. In case the CG size exceeds the current bucket size, remaining threads diverge and proceed to the next bucket.

D. Concurrency

All device-sided table operations can be overlapped and only synchronize with the CG they are executed in. The majority of hash table operations in WC can

a

h

h

1

g

p

i

n

e

s

4

hashtable

2

k

keyshandles

n

o

k2:[o,n]

p

e

e

k

freeslots

k1:[k,e,e,p]

4

7

k3:[h,a,s,h,i,n,g]

h

h

a

s

COPS →

inparallelhit!hit!hit!

retrieve(k1):retrieve(k2):retrieve(k3):

k3

k1

k2

7

coalescedaccess015

g

n

e

k

n

valuelists

2

o

bucketheaderindexofpreviousbucket

4

totalvaluecountbucketlisthandle

197

101619indexoflastbucket

i

Fig. 4: Example of retrieving all associated values for a batch of keys {k1,k2,k3} from the bucket list hash table.

be executed asynchronously (with respect to both host CPU and GPU). Only operations that use function return values to return data back to the host block until the return parameter is available. By default, all operations are executed in the default stream of the GPU making them blocking function calls. However, when called with a non-default stream, operations are issued asynchronously with respect to other streams, CUDA-devices, as well as the host system. This is a crucial feature for employing multiple hash tables residing on diﬀerent devices in a multi-GPU environment.

Note that not all operations on the same hash table can be safely executed concurrently. We distinguish two categories of operations based on whether they modify the internal state of a table. Overlapping the same operation and all read operations is always valid. However, overlap- ping write operations with another operation of a diﬀerent kind is not supported due to two concerns:

(1) If the combined key-value pair type exceeds the size constraint of 64 bits for CUDA atomic operations, in- sertion of a new key-value pair consists of two memory operations, an atomic swap of the key followed by a relaxed write of the value. If insertion and retrieval of the same key were to occur simultaneously, reading the value might yield incorrect results.

(2) Overlapping insertions and deletions is prone to a variant of the ABA problem. If we simultaneously is- sue a deletion combined with two insertion operations, all working on the same key k which is not yet present in the table, there exists a possible execution order in which a race condition may occur, leaving the table

TBB0.012500.20.40.60.811.21.41.61.850%55%60%65%70%75%80%85%90%95%billion operations per secondstorage density

WarpCore

CUDF

SlabHash

TBB

CUDPP

CUDPP

SlabHash

TBB

CUDF

TBB0.141300.511.522.533.544.550%55%60%65%70%75%80%85%90%95%billion operations per secondstorage density

WarpCore

(a) Bulk insertion performance.

(b) Bulk retrieval performance.

Fig. 5: Performance comparison of diﬀerent single-value hash table implementations during bulk operations for 228 (2 GB) unique key-value pairs.

in an invalid state.

If the hash table is conﬁgured to use 64-bit packed key-value pairs that can be stored using a single atomic operation, all possible combinations of operations leave the table in a valid state and return valid results. Nevertheless, combining insertion with deletion or any write operation with any other read operation might still be undesirable if these operations work with the same keys concurrently. The ﬁnal result may thus depend on their execution order and leave the table in an unpredictable, albeit valid, state.

E. Multi-GPU Support

The limited amount of main memory available on a single GPU can be insuﬃcient for many data-intensive applications. Thus, WC allows for building and querying data structures on multiple GPUs. There are two modes of operation: distributed and independent.

The distributed mode assigns each key (and its asso- ciated values) to exactly one distinct GPU. This is done by ﬁrst partitioning keys of an input batch according to their corresponding GPU ID by means of a device-sided multi-split [16] followed by scattering these segments to the GPUs where they belong. In case each participating GPU holds a separate input batch, we use an all-to-all communication primitive on NVLink connected systems [17] to simultaneously exchange segments between all GPUs. This approach has the advantage that (multi-value) retrieval does not require merging the results of individual GPUs, since each key may only reside on one GPU.

The second mode simply constructs and stores one independent hash table per GPU. This can be desirable in cases where result merging is acceptable or can be done without communicating all values. Data to be inserted is simply scattered and queries are broadcast to all GPUs.

V. Experimental Evaluation

Experiments were conducted on the following systems: System 1: Dual-socket Intel Xeon GOLD 6238 CPU (2x22 cores at 2.10 GHz) with 192 GB DDR4 RAM

and 2 Quadro GV100 GPUs connected via NVLink each with 32 GB HBM2 memory running Ubuntu 18.04 LTS, CUDA 10.2, GCC 8.3.0.

System 2 (DGX-1): Dual-socket Xeon E5-2698 v4 CPU (2x20 cores at 2.20 GHz) with 512 GB DDR4 RAM and 8 Tesla V100 GPUs connected by NVLink each with 32 GB HBM2 memory running Ubuntu 18.04, CUDA 10.1, GCC 8.3.0.

Time measurements are accomplished with CUDA event system timers. In all experiments, we assume that the data to be inserted or retrieved resides either in host RAM for operations executed on the CPU or in video RAM for device-sided benchmarks.

A. Single-Value Performance

We evaluated our single-value hash table against the publicly available state-of-the-art GPU implementations cuDPP [5], SlabHash [9], and cuDF [8]. Additionally, we included a widely-used multi-threaded CPU implementa- tion, namely tbb::unordered_hash_map from TBB. Our benchmark scenario consists of an initial bulk build op- eration which inserts a set of 228 unique 4-byte keys along with 4-byte arbitrary values into each hash table. Subsequently, we query the same set of keys against the table and retrieve their corresponding values. For both phases, we measure the number of executed operations per second averaged over ten consecutive runs in reference to the target density of the data structure, i.e., after all pairs have been inserted (see Figure 5). Benchmarks were conducted on a single GV100 GPU on System 1, while TBB utilizes all 44 CPU cores. Note that the target storage density of TBB’s hash table cannot be set by the user. Regarding insertion performance, WC outperforms cuDPP and cuDF by a factor of 3.95 and 1.6 for ρ = 0.97 and ρ = 0.8, respectively. For relatively low densities, SlabHash’s performance is on par with WC. However, if ρ increases (> 70%), WC’s cooperative probing scheme is superior. Note that some implementations did not ﬁnish

0%20%40%60%80%100%0204060801001201401601801248weak scaling efficiencyruntime [ms]#GPUs

insert

efficiency

multisplit

all-to-all

Fig. 6: Weak scalability analysis of hash table insertion on System 2 (DGX-1) with 2 GB of input data per GPU.

their execution for densities above a certain threshold. For retrieval, WC is faster than all competitors by a factor of 8.76 (ρ = 0.8), 1.64 (ρ = 0.9), 2.39 (ρ = 0.9) compared to cuDF, cuDPP, and SlabHash, respectively. Our results show, that WC outperforms all other tested GPU implementations at high storage densities and is also over two orders-of-magnitude faster than TBB.

To evaluate multi-GPU scalability, we tested the dis- tributed mode discussed in Section IV-E on System 2 with 227 unique 8-byte keys along with 8-byte values as input. Figure 6 shows a weak scalability analysis with runtime breakdowns for data partitioning, communication, and insertion together with the achieved eﬃciency. Note, that it would be possible to further apply common optimization strategies like batching and overlapping CUDA streams to hide the runtime of data transfers behind the kernel execution for multi-split and insertion, but we decided to report the full runtime of each primitive to show the relative cost.

B. Multi-Value Performance

To conduct the multi-value benchmark, we control the average number of identical keys r in the input batch by drawing n elements uniformly random from the range (1,..., n r ). Figure 7a shows the results for inserting such a distribution of keys into diﬀerent hash tables for varying values of r and a ﬁxed target load factor for WC and cuDF (cuDPP and SlabHash are only designed for single values). In case of our bucket list hash table, this load factor is solely enforced on the key store, i.e., the OA hash table holding the keys along with bucket list handles. During retrieval we probe for the complete range of n unique keys (1,...,n). With r increasing, this results in some of the queried keys to not being present in the table, whilst other keys are associated to multiple values. Using this setup, the total number of retrieved values is always equal to the number of input queries, i.e. n, which eliminates any eﬀects of I/O skew from our measurements.

For insertion, our MultiValueHashTable (WC OA) shows comparable performance to its single-value counter- part in the case that input keys are close-to unique. When

the value multiplicity increases, throughput degrades due to longer probing sequences. cuDF shows the same be- haviour but handles high key multiplicities worse due to its LP scheme, which is prone to primary clustering. This eﬀect is ampliﬁed in a multi-value setup, where multiple identical keys collide in the same cluster of initial probing position. WC OA consistently outperforms cuDF during insertion. For value multiplicities ≤ 16 a CG size of 8 shows optimal performance. However, for higher multiplicities larger CG sizes are more beneﬁcial. Both tested variants of warpcore::BucketListHashTable (WC BL) are slower than WC OA if the average number of values per key is less than 32 but show nearly constant performance for higher multiplicity, while WC OA gradually degrades. We suspect that this is a trade-oﬀ between WC BL’s additional steps required after probing, i.e., appending the value to the key’s bucket list and WC OA’s probing chain length. The same eﬀect may apply if we compare WC BL against cuDF but is visible at even lower multiplicities due to cuDF’s lower throughput. BL (1) (default) suﬀers from more bucket allocations compared to BL (2). However, this eﬀect mitigates with growing key multiplicity. Our experiments showed that a CG size of 16 is optimal for WC BL insertion.

As for retrieval (Figure 7b), cuDF shows similar be- haviour as during insertion. With higher key multiplicities, performance decreases gradually. In contrast, WC OA shows a nearly constant throughput between 0.66-0.72 billion operations per second, which highlights the two beneﬁts of our proposed COPS compared to cuDF’s LP approach. (1) DH ensures an overall shorter required chain of probings compared to LP. (2) Probing with a CG allows for parallel retrieval of multiple values associated to the same key inside the same inner probing window. cuDF uses a single thread per query which iterates over its probing sequence sequentially. Furthermore, both WC BL variants show nearly identical performance and consis- tently outperform WC OA. Note that the overall retrieval throughput of our multi-value scenario is considerably lower compared to the retrieval step in the single-value benchmark due to two reasons. (1) With increasing key multiplicity, the number of unsuccessful queries in the input set also increases, implying that more CGs are executed than needed. (2) Before the actual retrieval step, we have to calculate the value oﬀsets for each key in the output array. For both WC OA and WC BL a CG size of 4 shows optimal performance throughout all retrieval experiments.

C. Use Case: Metagenomics

The cost of DNA sequencing has decreased exponen- tially over the last years, making genomic data more acces- sible. A common paradigm in bioinformatics is to store and index sequence data as sets of k-length substrings (called k-mers). We have thus explored the eﬃciency of WC for indexing large amounts of genomes for metagenomic

0.00.20.40.60.81.01.21.41.61248163264128256billion operations per secondaverage values per key

cuDF (1)

cuDF (2)

WC BL (1)

WC BL (2)

WC OA (1)

WC OA (2)

WC OA (3)

cuDF (2)

WC OA

WC BL (2)

cuDF (1)

0.00.20.40.60.81.01.21.41.61.82.01248163264128256billion operations per secondaverage values per key

WC BL (1)

(a) Bulk insertion performance.

(b) Bulk retrieval performance.

Fig. 7: Performance of multi-value hash table implementations in billion operations per second for bulk operations on 228 (2 GB) key-value pairs with a varying number of values per key. We compare our WC OA variant with a target load factor of 0.8 for relevant CG sizes of 8 (1), 16 (2), and 32 (3), cuDF with two target load factors 0.5 (1) and 0.8 (2), as well as our bucket list variant (BL) with default (λ = 1.1, s0 = 1) (1) and optimal growth strategy (λ = 1.0, s0 = average number of values per key) (2).

classiﬁcation tasks in comparison to the popular CPU- based tools Kraken2 [18] and MetaCache [19] – both using hash tables as their primary index data structure – as a case study. Note that such hash tables can be used for a variety of other bioinformatics applications, too.

We store k-mers as keys along with their correspond- ing genomic meta-information as values. Metagenomic se- quencing reads are classiﬁed by querying their own set of k- mers against the constructed hash table and subsequently evaluating the returned values. k-mer reference database construction is typically the most time consuming part and can take several hours. In this work, we focus on the Meta- Cache approach, which employs an eﬃcient subsampling technique based on minhashing [20] in order to reduce the overall amount of to-be-stored k-mers, with minimal loss in terms of classiﬁcation accuracy. In order to alleviate the mentioned bottleneck during the construction of the reference database, we chose to port parts of MetaCache’s purely CPU-based construction phase to the GPU by utilizing GPU hash table building blocks provided by WC. To increase overall throughput, we also ported the k-mer generation and minhashing step to CUDA. Using a single CUDA kernel, we process the sample sequences on the GPU in a data-parallel fashion and insert the resulting k-mers into a multi-value hash table provided by our proposed WC library by using its device-sided interface.

First, we tested which of WC’s multi-value implementa- tions was best suited for metagenomic database construc- tion by building a single-GPU hash table. We therefore limited the overall hash table size to 28 GB and used a sin- gle GV100 GPU of System 1 to build a database for 18 GB of bacterial reference genomes. The remaining 4 GB (of the 32 GB device memory) could then be used for batched input processing and retrieval. Our implementation uses one CPU thread for extracting sequences from input ﬁles

WC OA AoS

Kraken2

runtime in seconds

WC OA SoA

105

WC BL

MetaCache

Kraken2

104

101

102

103

WC BL

MetaCache

16 min 12 min 29 s 20 s 12 s 355 min 190 min 36 s

Fig. 8: Comparison of metagenomic database construction times for small (solid bars) and large (hatched bars) datasets. Small-scale construction on a single GPU com- pares diﬀerent WC multi-value hash table variants. Large- scale construction uses WC’s bucket list on 8 GPUs.

and another thread managing a double buﬀer for batched data transfer to GPU and insertion. The results for WC’s variants compared to Kraken2’s and MetaCache’s default CPU construction are shown in Figure 8. Note that the key distribution for this data set is highly skewed. Although the average number of values per key is near 11, about a third of the keys has only one associated value and a small amount of keys occurs hundreds of times, which beneﬁts the dynamic growth strategy of WC’s bucket list (BL) hash table. Overall, WC BL achieves a speedup of 80.7 and 62.5 compared to Kraken2 and MetaCache, respectively. Because the memory of a single GPU is too small to hold large-scale reference genome databases, we also explored the usage of multiple GPUs. For this test we used a ref- erence genome dataset intended for food sequencing [21], which consists of bacterial, viral, and archaeal as well as animal and plant genomes. About 120 GB of genomes were

used to build a distributed database using the 8 GPUs of System 2 in parallel. Figure 8 also shows the large-scale runtimes for Kraken2 and MetaCache compared to WC’s bucket list (BL) hash table, which turned out fastest in the single-GPU benchmark. Building the multi-GPU database took 36 seconds resulting in a speedup of 592 and 317 compared to Kraken2 and MetaCache, respectively.

VI. Conclusion

Rapidly growing data volumes in many ﬁelds such as bioinformatics have led to an increasing demand for fast associative data structures on modern parallel archi- tectures. State-of-the-art GPU-based solutions are either only applicable to a small range of practical use cases or show unsatisfactory performance characteristics and storage densities. A prominent example of the latter is that many hash map implementations require trading oﬀ runtime performance for memory eﬃciency because their throughput decreases signiﬁcantly for high load factors. Throughput of the few existing GPU multi-value hash maps decreases dramatically for key distributions with many associated values per key.

We have presented massively parallel hashing data structures and associated algorithms for single-value and multi-value hash maps that can be adapted to a variety of use cases. Their customization within a library (WC) is achieved through a set of fundamental building blocks for data layout abstractions. We exploit the fast memory interface of modern GPUs by means of a parallel probing scheme based on CUDA cooperative groups where threads communicate using fast collective operations such as group votes.

We have demonstrated that WC outperforms other state-of-the-art solutions by achieving billions of table operations per second on a single GPU even under very high load factors. Both our multi-value hash maps (pure OA and bucket list hash maps) provide robust throughput over a wide range of possible key multiplicities signiﬁcantly outperforming NVIDIA RAPIDS cuDF, especially for bulk retrieval operations. We have further shown how to scale hash tables to multiple GPUs with fast NVLink intercon- nect in order to overcome the memory limitations of a single GPU. Using our library, we were able to acceler- ate a real-world bioinformatics application - metagenomic classiﬁcation - on both single GPUs as well as on a multi- GPU DGX server.

Scaling to even bigger datasets could be achieved by extending our library to GPU clusters. While WC is speciﬁcally designed for GPUs, the introduced concepts could serve as a basis for eﬃcient implementations on other accelerators such as modern FPGAs.

WC is written in C++/CUDA-C and will be made

publicly available upon the acceptance of the paper.

Acknowledgment

Parts of this research were conducted using the super- computer Mogon II and/or advisory services oﬀered by

Johannes Gutenberg University Mainz (hpc.uni-mainz.de) which is a member of the AHRP and the Gauss Alliance e.V.

References

[1] T. C. Pan, S. Misra, and S. Aluru, “Optimizing high perfor- mance distributed memory parallel hash tables for DNA k-mer counting,” in SC18.

IEEE, 2018, pp. 135–147.

[2] M. Bisson and M. Fatica, “High Performance Exact Triangle Counting on GPUs,” IEEE TPDS, vol. 28, no. 12, pp. 3501– 3510, 2017.

[3] B. Chen, T. Medini, J. Farwell, S. Gobriel, C. Tai, and A. Shri- vastava, “SLIDE: In Defense of Smart Algorithms over Hard- ware Acceleration for Large-Scale Deep Learning Systems,” arXiv:1903.03129, 2019.

[4] D. A. Alcantara, A. Sharf, F. Abbasinejad, S. Sengupta, M. Mitzenmacher, J. D. Owens, and N. Amenta, “Real-time Parallel Hashing on the GPU,” in ACM SIGGRAPH Asia 2009. New York, NY, USA: ACM, 2009, pp. 154:1–154:9.

[5] D. A. F. Alcantara, “Eﬃcient Hash Tables on the GPU,” Ph.D. dissertation, University of California at Davis, Davis, CA, USA, 2011, aAI3482095.

[6] I. García, S. Lefebvre, S. Hornus, and A. Lasram, “Coherent Parallel Hashing,” in ACM SIGGRAPH Asia 2011, ser. SA ’11. New York, NY, USA: ACM, 2011, pp. 161:1–161:8.

[7] F. Khorasani, M. E. Belviranli, R. Gupta, and L. N. Bhuyan, “Stadium Hashing: Scalable and Flexible Hashing on GPUs,” in 2015 International Conference on Parallel Architecture and Compilation (PACT).

IEEE, 2015, pp. 63–74.

[8] RAPIDS Development Team, cuDF - GPU DataFrame Library, 2020. [Online]. Available: https://github.com/rapidsai/cudf [9] S. Ashkiani, M. Farach-Colton, and J. D. Owens, “A Dynamic IEEE, 2018, pp.

Hash Table for the GPU,” in IPDPS 2018. 419–429.

[10] O. Green, “HashGraph – Scalable Hash Tables Using A Sparse Graph Data Structure,” ArXiv, vol. abs/1907.02900, 2019. [11] D. Jünger, C. Hundt, and B. Schmidt, “WarpDrive: Massively Parallel Hashing on Multi-GPU Nodes,” in IPDPS 2018. IEEE, 2018, pp. 441–450.

[12] P. Celis, P. A. Larson, and J. I. Munro, “Robin Hood Hashing,” in 26th Annual Symposium on Foundations of Computer Science (sfcs 1985), Oct 1985, pp. 281–288.

[13] B. Lessley and H. Childs, “Data-Parallel Hashing Techniques for GPU Architectures,” IEEE Transactions on Parallel and Distributed Systems, vol. 31, no. 1, pp. 237–250, 2019.

[14] RAPIDS Development Team, RAPIDS: Collection of Libraries for End to End GPU Data Science, 2020. [Online]. Available: https://rapids.ai

[15] S. Ashkiani. SlabHash code repository. https://github.com/owensgroup/SlabHash

[Online]. Available:

[16] S. Ashkiani, A. Davidson, U. Meyer, and J. D. Owens, “GPU Multisplit,” in 21st ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming (PPoPP ’16). New York, NY, USA: ACM, 2016, pp. 12:1–12:13.

[17] R. Kobus, D. Jünger, C. Hundt, and B. Schmidt, “Gossip: Eﬃcient Communication Primitives for Multi-GPU Systems,” in 48th International Conference on Parallel Processing (ICPP ’19), 2019, pp. 1–10.

[18] D. E. Wood, J. Lu, and B. Langmead, “Improved metagenomic analysis with Kraken 2,” Genome Biology, vol. 20, no. 1, p. 257, 11 2019.

[19] A. Müller, C. Hundt, A. Hildebrandt, T. Hankeln, and B. Schmidt, “MetaCache: classiﬁcation of metagenomic reads using minhashing,” Bioinformatics, vol. 33, no. 23, pp. 3740–3748, 2017.

context-aware

[20] A. Z. Broder, “Identifying and Filtering Near-Duplicate Doc- uments,” in Annual Symposium on Combinatorial Pattern Matching. Springer, 2000, pp. 1–10.

[21] R. Kobus, J. M. Abuín, A. Müller, S. L. Hellmann, J. C. Pichel, T. F. Pena, A. Hildebrandt, T. Hankeln, and B. Schmidt, “A big data approach to metagenomics for all-food-sequencing,” BMC Bioinformatics, vol. 21, no. 1, pp. 1471–2105, 2020.