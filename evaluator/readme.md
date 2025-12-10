# RAG Evaluation Framework

This framework evaluates **Retrieval-Augmented Generation (RAG)** systems by comparing:

1. **The system’s retrieved documents + generated answer**
2. **Against a ground-truth set of golden documents + reference answers**

It produces both **quantitative** and **qualitative** metrics that assess retrieval quality, answer correctness, and alignment with reference answers.

------------------------------------------------------------

## What This Framework Does

Given:

- **Ground truth file**
  - complex_retrieval_requests_ref_answers.json (preferred)
    - Contains: query, golden retrieved documents/snippets, reference answer (optional but required for many metrics)
  - OR complex_retrieval_requests.json
    - Same structure, but no reference answers
    - Used when reference answers are disabled

- **RAG system output**
  - results.json (your system generates this)
  - Contains:
    - query
    - generated response
    - retrieved documents/snippets used by the system

The evaluator computes:

- BLEU
- ROUGE (1, 2, L)
- RAGAS metrics (faithfulness, context precision/recall, response relevancy)
- Retrieval metrics (precision@K, recall@K)
- LLM-as-a-judge factuality scoring (correct / partially correct / incorrect + explanation)

Results are written into a final evaluation_report.json.

------------------------------------------------------------

# Metrics Overview

Example output snippet:

{
  "metrics": {
    "bleu": 0.0168,
    "rouge1": 0.3481,
    "rouge2": 0.0896,
    "rougeL": 0.2148,
    "llm_factuality_judgement": "Rating: Partially Correct\n\nReasoning...",
    "ragas/faithfulness": 0.61538,
    "ragas/context_precision": 0.0,
    "ragas/context_recall": 0.6667,
    "ragas/response_relevancy": 0.7532,
    "precision@1": 1.0,
    "precision@5": 0.25,
    "recall@1": 0.3333,
    "recall@5": 0.3333
  }
}

### Types of Metrics

1. **Answer Quality**
   - BLEU
   - ROUGE-1, ROUGE-2, ROUGE-L

2. **LLM-Based Qualitative Evaluation**
   - Correct / Partially Correct / Incorrect
   - Multi-sentence explanation

3. **RAGAS Metrics**
   - Faithfulness
   - Context Precision
   - Context Recall
   - Response Relevancy

4. **Retrieval Ranking**
   - precision@K
   - recall@K

------------------------------------------------------------

# Running the Evaluator

The evaluator is self-contained and has its own Python dependencies separate from the outer project. Follow these steps to install and run it correctly.

# 1. Navigate to the Evaluator Directory (from the project root)

```
cd evaluator
```

# 2. (Optional but recommended) Create and Activate a Virtual Environment

# macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```
# Windows (PowerShell):
```
python -m venv venv
venv\Scripts\Activate.ps1
```

# 3. Install Dependencies

Make sure you remain inside the evaluator/ folder:
```
pip install -r requirements.txt
```

------------------------------------------------------------
# 4. Run the Evaluator

python evaluator_runner.py [results_file] [output_file]

Example:
```
python evaluator_runner.py results.json my_report.json
```

------------------------------------------------------------

# Output: evaluation_report.json

{
  "per_request": [
    {
      "index": 0,
      "request": "...",
      "response": "...",
      "metrics": { ... }
    }
  ],
  "averages": {
    "bleu": ...,
    "rouge1": ...,
    "ragas/context_precision": ...,
    ...
  }
}

------------------------------------------------------------

# How Reference Answers Affect Metrics

### With reference answers:
✔ BLEU  
✔ ROUGE  
✔ RAGAS: context precision, recall  
✔ LLM factuality judgment  
✔ Retrieval precision/recall  

### Without reference answers:
- The evaluator **concatenates the golden documents into a pseudo-answer**
- BLEU/ROUGE comparisons become weaker indicators
- LLM judgment still works but with weaker grounding

