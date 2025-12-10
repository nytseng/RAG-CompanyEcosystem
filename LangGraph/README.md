# Multi-Strategy RAG Agent with LangGraph and Weaviate

This project implements an advanced Retrieval-Augmented Generation (RAG) system specialized for NVIDIA-related content. It features two distinct workflows: an **Agentic Workflow** using query decomposition and database routing, and a **Baseline Workflow** for simple retrieval. The system is built using LangChain, LangGraph, Weaviate, and Ollama for local LLM inference.

## System Architecture

### 1. Agentic Workflow
This workflow handles complex user queries through a multi-step state graph:
* **Decomposition:** Breaks down complex questions into independent sub-questions using a custom schema.
* **Routing:** Analyzes each sub-question and routes it to the most relevant data source:
    * **Transcripts:** Speeches and earnings calls.
    * **Papers:** Technical deep learning research.
    * **Newsletters:** General updates and articles.
* **Retrieval:** Executes vector searches in parallel across the selected Weaviate indices.
* **Generation:** Synthesizes an answer using the aggregated context.
* **Assessment:** An LLM evaluator checks if the generated answer is sufficient. If not, the question is refined, and the cycle repeats.

### 2. Baseline Workflow
A standard RAG pipeline used for performance comparison:
* **Retrieval:** Queries a single general-purpose index (NvidiaInfo).
* **Generation:** Produces an answer based solely on the retrieved documents without refinement steps.

## Prerequisites

### Docker Services
Ensure the following services are running:
* **Weaviate:** Running on port 8080 (HTTP) and 50051 (gRPC).
* **Ollama:** Running on port 11434 with the gemma3 model pulled.

### Python Dependencies
Dependencies are located in requirements.txt but should automatically be installed when the docker image is built

### External Files
* metric_handler.py: A custom module required for tracking token usage and latency (referenced in imports).
* complex_retrieval_requests.json: A JSON file containing the list of queries to process.

## Configuration

The script contains several hardcoded configuration variables at the top of the file that may need adjustment based on your environment:

* **LLM_MODEL:** Defaults to gemma3. Ensure this model is available in Ollama.
* **OLLAMA_BASE_URL:** Defaults to http://ollama:11434. Change to http://localhost:11434 if running outside of Docker.
* **WEAVIATE_URL / Host:** Defaults to weaviate. Change to localhost if running outside of Docker.
* **MODEL_NAME:** Defaults to all-MiniLM-L6-v2 for HuggingFace embeddings.

## Vector Store Indices
The system expects the following schemas to exist in your Weaviate instance:
* ChunkedNvidiaTranscripts
* ChunkedNvidiaPublications
* ChunkedNvidiaArticles
* NvidiaInfo

## Usage

Run the script directly using Python:

```
python weaviate_agent.py
```

### Execution Flow
1.  **Single Query Test:** The script first runs a hardcoded test question ("How does NVIDIA reduce latency in ray tracing?") through the Agentic workflow in order to ensure services are initialized.
2.  **Batch Processing (Agent):** It iterates through requests in complex_retrieval_requests.json using the Agentic workflow.
3.  **Batch Processing (Baseline):** It iterates through the same requests using the Baseline workflow.

### Output
Results are saved to the ./data/ directory:
* chunked_result.json: Performance metrics and answers from the Agentic workflow.
* chunked_baseline_result.json: Performance metrics and answers from the Baseline workflow.

Each output entry includes:
* Generated response
* Retrieved context (content and metadata)
* Total execution time
* Token usage (input/output)
* Latency metrics

## Troubleshooting

* **Connection Errors:** If the script fails to connect to Weaviate or Ollama, check the host parameters in the weaviate.connect_to_local call and OLLAMA_BASE_URL variable.
* **Model Not Found:** Run ollama list to verify gemma3 is installed.
* **Import Errors:** Ensure metric_handler.py is in the same directory as the script.