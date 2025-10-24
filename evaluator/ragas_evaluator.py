import json
from ragas import Evaluator


with open("retrieval_requests.json") as f:
    data = json.load(f)

requests = data["requests"]
evaluator = Evaluator(model="tiiuae/falcon-7b-instruct")
baseline_results = []

def precision_at_k(relevance_flags, k):
    return sum(relevance_flags[:k]) / k

def recall_at_k(relevance_flags, k, total_relevant):
    return sum(relevance_flags[:k]) / total_relevant if total_relevant else 0

for req in requests:
    query_text = req["request"]
    docs = req["documents"]
    top_k_docs = docs[:5]
    retrieved_texts = [d["text"] for d in top_k_docs]
    
    relevant_doc_ids = [d["document"] for d in docs]
    retrieved_ids = [d["document"] for d in top_k_docs]
    ragas_scores = evaluator.evaluate(query_text, retrieved_texts)
    
    rel_flags = [1 if doc_id in relevant_doc_ids else 0 for doc_id in retrieved_ids]
    prec = precision_at_k(rel_flags, k=5)
    rec = recall_at_k(rel_flags, k=5, total_relevant=len(relevant_doc_ids))
    
    qualitative_examples = []
    for text, score, flag in zip(retrieved_texts, ragas_scores, rel_flags):
        qualitative_examples.append({
            "text": text,
            "ragas_score": score,
            "is_relevant": bool(flag)
        })
    
    baseline_results.append({
        "query": query_text,
        "precision@5": prec,
        "recall@5": rec,
        "ragas_scores": ragas_scores,
        "qualitative_examples": qualitative_examples
    })

with open("baseline_eval_results.json", "w") as f:
    json.dump(baseline_results, f, indent=2)

print("Baseline evaluation complete!")
