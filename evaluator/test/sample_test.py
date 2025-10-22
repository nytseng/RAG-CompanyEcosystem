# text_eval/examples/sample_test.py
from evaluator.bleu_evaluator import BLEUEvaluator
from evaluator.rouge_evaluator import ROUGEEvaluator

# Mock test samples
reference = "The quick brown fox jumps over the lazy dog"
candidate_good = "A quick brown fox jumps over the lazy dog"
candidate_bad = "The cat sleeps under the table"

# Instantiate evaluators
bleu_eval = BLEUEvaluator()
rouge_eval = ROUGEEvaluator()

# Evaluate good candidate
print("=== Good Candidate ===")
print("BLEU:", bleu_eval.evaluate(reference, candidate_good))
print("ROUGE:", rouge_eval.evaluate(reference, candidate_good))

# Evaluate bad candidate
print("\n=== Bad Candidate ===")
print("BLEU:", bleu_eval.evaluate(reference, candidate_bad))
print("ROUGE:", rouge_eval.evaluate(reference, candidate_bad))

# output after run
# === Good Candidate ===
# BLEU: 0.8633
# ROUGE: {'rouge1': 0.8889, 'rouge2': 0.875, 'rougeL': 0.8889}

# === Bad Candidate ===
# BLEU: 0.0294
# ROUGE: {'rouge1': 0.2667, 'rouge2': 0.0, 'rougeL': 0.2667}