# RAG-CompanyEcosystem:

## Executive Summary

RAG-CompanyEcosystem is a specialized Retrieval-Augmented Generation (RAG) system designed as an internal NVIDIA research tool for discovering ongoing work, facilitating team collaborations, and ensuring leadership alignment. The system addresses the critical need for efficient knowledge discovery within NVIDIA's vast ecosystem of research publications, news announcements, and executive communications.

This Phase 1 implementation demonstrates a domain-specific RAG system optimized for technical and strategic decision-making within NVIDIA's corporate environment, moving beyond general-purpose question-answering to provide contextually relevant insights for research teams, project managers, and executives.

## Project Structure

```
RAG-CompanyEcosystem/
├── README.md                           # This comprehensive documentation
├── retrieval_requests.json             # 10 manual domain-specific test queries
├── weaviate_results.json               # Experimental results from Weaviate system
│
├── data/                               # Curated NVIDIA knowledge base (125 docs)
│   ├── nvidia_articles/                # Recent newsroom content (67 .txt files)
│   │   └── [Articles covering AI infrastructure, partnerships, sustainability]
│   ├── publications/                   # Research paper collection (43 .md files)
│   │   ├── README.md                   # Collection methodology documentation
│   │   ├── download_arxiv.py           # Automated paper collection script
│   │   ├── parse_papers.py             # PDF to markdown conversion utility
│   │   └── rag_papers_text/            # Processed research papers
│   │       └── [43 highly-cited NVIDIA research papers on AI, CUDA, GPUs]
│   └── transcripts/                    # Executive communications (15 .txt files)
│       ├── metadata.json               # Comprehensive interview metadata
│       ├── readme.md                   # Collection and processing methodology
│       └── [15 Jensen Huang interviews/keynotes from 2025]
│
├── qdrant/                             # Primary vector database implementation
│   ├── script.py                       # Vector ingestion with incremental processing
│   ├── readme.md                       # Technical implementation documentation
│   ├── requirements.txt                # Python dependencies
│   └── qdrant_db_COSINE/               # SQLite-based vector storage
│
├── evaluator/                          # Multi-modal evaluation framework
│   ├── __init__.py                     # Package initialization
│   ├── bleu_evaluator.py               # N-gram similarity metrics (BLEU)
│   ├── rouge_evaluator.py              # Recall-oriented metrics (ROUGE-1, -2, -L)
│   ├── llm_evaluator.py                # LLM-based factual accuracy assessment
│   ├── ragas_evaluator.py              # Retrieval quality metrics (RAGAS)
│   ├── readme.md                       # Comprehensive evaluation documentation
│   └── test/                           # Evaluation examples and validation
│       ├── __init__.py
│       └── sample_test.py              # Usage examples
│
└── weaviate/                           # Alternative vector store experiments
    ├── README.md                       # Weaviate implementation documentation
    ├── newsletter_scraper.py           # Web scraping utilities
    ├── weaviate_db.py                  # Vector database setup and configuration
    ├── weaviate_db_backup.py           # Backup utilities
    ├── weaviate_db_restore.py          # Restore utilities
    ├── weaviate_query.py               # Query interface implementation
    └── weaviate_backups/               # Backup storage directory
        ├── my_nvidia_rag_export_20251021/
        └── nvidia_all_1/
```

## Domain Justification

### Internal Research Tool Vision

The RAG-CompanyEcosystem serves as NVIDIA's internal knowledge discovery platform, specifically designed to:

- **Discover Ongoing Work**: Enable research teams to identify related projects, avoid duplication, and find collaboration opportunities across NVIDIA's diverse research portfolio
- **Facilitate Team Collaborations**: Surface relevant expertise, publications, and project contexts to accelerate cross-team initiatives
- **Ensure Leadership Alignment**: Provide executives with comprehensive context on research directions, market positioning, and strategic communications

### Why NVIDIA-Specific RAG Matters

Unlike general-purpose RAG systems, this implementation focuses on NVIDIA's unique ecosystem characteristics:

1. **Technical Depth**: Deep understanding of GPU architectures, AI frameworks, and accelerated computing
2. **Strategic Context**: Integration of market positioning, partnership announcements, and executive vision
3. **Research Continuity**: Tracking of research progression from academic papers to product implementations
4. **Competitive Intelligence**: Understanding of technology trends and market developments affecting NVIDIA's position

## Dataset Composition

### Overview: 125 Documents Across Three Categories

Our curated dataset represents NVIDIA's knowledge ecosystem through strategically selected document types that capture different aspects of the company's technical and strategic landscape:

#### Articles (67 documents)
**Source**: Recent NVIDIA newsroom posts
**Format**: `.txt` files  
**Content Focus**: Product announcements, partnership developments, AI infrastructure advances, and sustainability initiatives
**Strategic Value**: Current market positioning and product roadmap insights

#### Publications (43 documents)  
**Source**: Highly-cited research papers
**Format**: `.md` files (converted from PDF)
**Content Focus**: Foundational AI research, GPU architectures, accelerated computing frameworks
**Strategic Value**: Technical foundation and research direction understanding

#### Transcripts (15 documents)
**Source**: Jensen Huang interviews and keynotes from 2025
**Format**: `.txt` files
**Content Focus**: Strategic vision, industry perspectives, and executive insights
**Strategic Value**: Leadership alignment and strategic direction context

### Data Collection Methodology

- **Articles**: Automated scraping of NVIDIA newsroom with relevance filtering
- **Publications**: Targeted collection using ArXiv API with citation-based selection criteria  
- **Transcripts**: Manual curation of key executive communications with comprehensive metadata

## Technical Architecture

### Vector Database Implementation

**Primary System: Weaviate**
- **Purpose**: Experimental implementation for comparison
- **Features**: Backup/restore capabilities, alternative querying approaches
- **Location**: `./weaviate/` with comprehensive system

**Alternative System: Qdrant**
- **Backend**: SQLite for local deployment and development
- **Embedding Model**: SentenceTransformer `all-MiniLM-L6-v2` (384 dimensions)
- **Distance Metric**: Cosine similarity
- **Storage**: `./qdrant/qdrant_db_COSINE/`
- **Processing**: Incremental ingestion with smart deduplication


## Evaluation Methodology

### Test Set Design: 10 Domain-Specific Queries

The evaluation framework centers on manually crafted queries that test practical scenarios requiring semantic understanding within NVIDIA's domain:

**Query Categories**:
1. **Technical Infrastructure**: AI factory scalability, networking bottlenecks
2. **Framework Applications**: NeMo toolkit real-world implementations  
3. **Strategic Vision**: AI agents in enterprise environments
4. **Medical AI**: GPU-accelerated clinical applications
5. **Industrial Applications**: Digital twin technology benefits
6. **Partnership Ecosystem**: Cloud platform AI infrastructure expansion
7. **Sustainability**: Energy efficiency improvements in data centers
8. **Performance Scaling**: Hopper to Blackwell architecture evolution
9. **Cost Optimization**: Token generation cost reduction strategies
10. **Research Collaboration**: Academic and industry partnership models

Each query includes manually selected ground truth documents with specific text passages, enabling precise evaluation of retrieval accuracy and semantic matching.

### Multi-Modal Evaluation Framework

#### Quantitative Evaluation (RAGAS)
- **Retrieval Precision**: Accuracy of document selection for queries
- **Retrieval Recall**: Coverage of relevant documents in results  
- **Semantic Similarity**: Embedding-based relevance scoring
- **Answer Relevancy**: Generated response alignment with query intent

#### Traditional NLP Metrics
- **BLEU Score**: N-gram overlap assessment (lexical similarity)
- **ROUGE Metrics**: Recall-oriented evaluation (ROUGE-1, ROUGE-2, ROUGE-L)
- **Token-level Analysis**: Precision/recall for generated content

#### LLM-Based Qualitative Evaluation
- **Factual Accuracy Assessment**: Three-tier classification (Correct/Partially Correct/Incorrect)
- **Reasoning Explanation**: 2-3 sentence justification for each evaluation
- **Error Categorization**: Systematic classification of failure modes
- **Cross-Model Validation**: Multiple LLM provider consistency checking

### Technical Domain Error Classification

**Error Type Categories**:
1. **Technical Specification Errors**: Incorrect performance metrics, architecture details
2. **Strategic Misalignment**: Responses contradicting NVIDIA's stated positions
3. **Temporal Inconsistencies**: Outdated information conflicting with recent developments
4. **Context Fragmentation**: Incomplete retrieval leading to missing critical context
5. **Hallucination Detection**: Generated content not supported by retrieved documents


## Phase 1 Achievements

### Dataset Curation
- ✅ **125 documents** collected across three strategic categories
- ✅ **Comprehensive metadata** with source tracking and temporal information
- ✅ **Quality filtering** ensuring relevance to NVIDIA's ecosystem

### Technical Implementation  
- ✅ **Dual vector store** implementation (Weaviate primary, Qdrant experimental)
- ✅ **Incremental processing** with smart deduplication
- ✅ **Local deployment** optimized for research team usage

### Evaluation Framework
- ✅ **10 domain-specific queries** with manual ground truth annotation
- ✅ **Multi-modal evaluation** combining quantitative and qualitative metrics
- ✅ **Error categorization** framework for technical domain failures

### Research Infrastructure
- ✅ **Reproducible pipeline** with comprehensive documentation
- ✅ **Backup/restore** capabilities for data preservation
- ✅ **Modular architecture** enabling component-wise improvements


## Future Development Roadmap

1. Implement complete RAG with generation
2. Improve retrieval by adding reranking and reasoning
3. Implement retrieval improvements after reflecting on research
4. Research method of function calling to query websites to add to the vector store
5. Implement function calling
6. Implement additional evaluation methods and metrics

## Contributing

This project serves as NVIDIA's internal research infrastructure. For technical improvements or domain-specific enhancements:

1. **Vector Database Optimization**: Improvements to ingestion pipeline or query performance
2. **Evaluation Framework**: Additional metrics or domain-specific evaluation criteria  
3. **Content Curation**: Enhanced document selection or metadata enrichment
4. **Query Interface**: User experience improvements for research team workflows

## Technical Specifications

- **Python**: 3.8+ required
- **Vector Database**: Weaviate
- **Evaluation**: BLEU, ROUGE, LLM-based accuracy, RAGAS metrics
- **Storage**: vector database, scalable to distributed deployment
- **Processing**: Incremental document ingestion with hash-based deduplication

## License and Usage

This project is designed for NVIDIA internal research applications. The implementation serves as a foundation for domain-specific RAG systems optimized for technical and strategic knowledge discovery within corporate environments.

---

**Project Status**: Phase 1 Complete  
**Last Updated**: October 2025  
