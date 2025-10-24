import json
from ragas import evaluate

class GeminiLLM:
    def __init__(self, client):
        self.client = client

    def __call__(self, prompt: str) -> str:
        response = self.client.generate_text(prompt)
        return response["text"]

with open("retrieval_requests.json") as f:
    data = json.load(f)

requests = data["requests"]
gemini_client = GeminiLLM(client=GeminiClient())
baseline_results = []

for req in requests:
    query_text = req["request"]
    docs = req["documents"]
    top_k_docs = docs[:5]
    retrieved_texts = [d["text"] for d in top_k_docs]
    relevant_doc_ids = [d["document"] for d in docs]
    retrieved_ids = [d["document"] for d in top_k_docs]

    ragas_scores = evaluate(query=query_text, documents=retrieved_texts, model=gemini_client)
    
    rel_flags = [1 if doc_id in relevant_doc_ids else 0 for doc_id in retrieved_ids]
    precision_at_5 = sum(rel_flags[:5]) / 5
    recall_at_5 = sum(rel_flags[:5]) / len(relevant_doc_ids) if relevant_doc_ids else 0

    qualitative_examples = [{"text": t, "ragas_score": s, "is_relevant": bool(f)} 
                            for t, s, f in zip(retrieved_texts, ragas_scores, rel_flags)]

    baseline_results.append({
        "query": query_text,
        "precision@5": precision_at_5,
        "recall@5": recall_at_5,
        "ragas_scores": ragas_scores,
        "qualitative_examples": qualitative_examples
    })

with open("baseline_eval_results.json", "w") as f:
    json.dump(baseline_results, f, indent=2)