# RAG Text Vectorization Workflow

## Overview
This project implements a RAG (Retrieval-Augmented Generation) text vectorization pipeline that processes documents from GitHub repositories, converts them to vector embeddings, and stores them in a Qdrant vector database.

## Dataflow Architecture
![RAG flowchart](./RAG_flowchart.png)


## Technical Components

### 1. Data Sources
- **GitHub API**: Recursively fetches file URLs from repository
- **File Types**: `.txt` and `.md` files (excluding README.md)
- **Repository**: `nytseng/RAG-CompanyEcosystem/data`

### 2. Vector Generation
- **Model**: SentenceTransformer `all-MiniLM-L6-v2`
- **Dimensions**: 384 float values per document
- **Distance Metric**: Cosine similarity

### 3. Database Storage
- **Vector DB**: Qdrant (local instance)
- **Backend**: SQLite for persistence
- **Collection**: `github_all_txt_documents`
- **Location**: `./qdrant_db_COSINE/`

### 4. Data Structure
Each vector point contains:
```json
{
  "id": "uuid-string",
  "vector": [384 float values],
  "payload": {
    "source_url": "https://raw.githubusercontent.com/..."
  }
}