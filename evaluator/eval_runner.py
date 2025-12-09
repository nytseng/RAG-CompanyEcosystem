import json
import os
import sys
from tqdm import tqdm

from bleu_evaluator import BLEUEvaluator
from rouge_evaluator import ROUGEEvaluator
from llm_evaluator import LLMEvaluator, OpenAIClient
from ragas_evaluator import RagasEvaluator


def load_data(gt_path="ground_truth.json", res_path="results.json"):
    with open(gt_path, "r", encoding="utf-8") as f:
        gt = json.load(f)
    with open(res_path, "r", encoding="utf-8") as f:
        res = json.load(f)
    return gt["requests"], res["results"]


def compute_averages(all_metrics):
    """
    Automatically discover all numeric metric keys and compute their averages.
    """
    numeric_keys = set()

    # Discover numeric keys
    for m in all_metrics:
        for k, v in m.items():
            if isinstance(v, (int, float)):
                numeric_keys.add(k)

    # Compute averages
    averages = {}
    for key in sorted(numeric_keys):
        vals = [m[key] for m in all_metrics if isinstance(m.get(key), (int, float))]
        if vals:
            averages[key] = sum(vals) / len(vals)
    return averages


def evaluate_results(
    gt_path="ground_truth.json",
    res_path="results.json",
    out_path="metrics_report.json",
):
    ground_truth, results = load_data(gt_path, res_path)

    bleu = BLEUEvaluator()
    rouge = ROUGEEvaluator()
    llm_eval = LLMEvaluator(OpenAIClient())
    ragas_eval = RagasEvaluator(llm_client=OpenAIClient())

    all_metrics = []
    per_request = []

    for i, (gt_ex, res_ex) in tqdm(enumerate(zip(ground_truth, results)), desc="Evaluating..."):
        question = gt_ex["request"]
        gold_docs = bleu.parse_documents_list(gt_ex)
        reference_answer = gt_ex.get("reference_answer", None)
        response = res_ex["response"]
        retrieved = bleu.parse_documents_list(res_ex)

        m_bleu = bleu.evaluate(question, response, gold_docs, retrieved, reference_answer=reference_answer)
        m_rouge = rouge.evaluate(question, response, gold_docs, retrieved, reference_answer=reference_answer)
        m_llm = llm_eval.evaluate(question, response, gold_docs, retrieved, reference_answer=reference_answer)
        m_ragas = ragas_eval.evaluate(question, response, gold_docs, retrieved, reference_answer=reference_answer)

        metrics = {
            **m_bleu,
            **m_rouge,
            **m_llm,
            **m_ragas,
        }

        all_metrics.append(metrics)

        per_request.append(
            {
                "index": i,
                "request": question,
                "response": response,
                "metrics": metrics,
            }
        )

    # Compute overall averages for all numeric metric keys
    averages = compute_averages(all_metrics)

    # Build final JSON structure
    report = {
        "per_request": per_request,
        "averages": averages
    }

    # Write to JSON file
    print(f"Writing results into {out_path}...")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Optional: print averages to stdout too
    print("Average metrics over dataset:")
    print(json.dumps(averages, indent=2))


if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(SCRIPT_DIR)
    LANGGRAPH_DIR = os.path.join(ROOT_DIR, "LangGraph")

    # Defaults
    DEFAULT_RESULTS_FILE = "result.json"
    DEFAULT_OUTPUT_FILE = "evaluation_report.json"

    # Parse arguments
    # Usage: python eval_runner.py [results_file] [output_file]
    results_filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RESULTS_FILE
    output_filename = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_FILE

    GROUND_TRUTH_PATH = os.path.join(ROOT_DIR, "complex_retrieval_requests_ref_answers.json")
    RESULTS_PATH = os.path.join(LANGGRAPH_DIR, "data", results_filename)
    OUT_PATH = output_filename

    print("Evaluating metrics using files:")
    print(f"Ground truth file:   {GROUND_TRUTH_PATH}")
    print(f"Results file:        {RESULTS_PATH}")
    print(f"Output file:         {OUT_PATH}")

    evaluate_results(GROUND_TRUTH_PATH, RESULTS_PATH, OUT_PATH)
