# text_eval/examples/sample_test.py
from evaluator.bleu_evaluator import BLEUEvaluator
from evaluator.rouge_evaluator import ROUGEEvaluator
from evaluator.llm_evaluator import LLMEvaluator, OpenAIClient, ClaudeClient, LocalLLMClient


# Mock test samples
reference = "The quick brown fox jumps over the lazy dog"
candidate_good = "A quick brown fox jumps over the lazy dog"
candidate_bad = "The cat sleeps under the table"

# Instantiate evaluators
bleu_eval = BLEUEvaluator()
rouge_eval = ROUGEEvaluator()

# model detail
question = "What jumps over what"
reference = "The quick brown fox jumps over the lazy dog"
generated = "A quick brown fox jumps over the lazy dog"


# Evaluate good candidate
print("=== Good Candidate ===")
print("BLEU:", bleu_eval.evaluate(reference, candidate_good))
print("ROUGE:", rouge_eval.evaluate(reference, candidate_good))

# Evaluate bad candidate
print("\n=== Bad Candidate ===")
print("BLEU:", bleu_eval.evaluate(reference, candidate_bad))
print("ROUGE:", rouge_eval.evaluate(reference, candidate_bad))


# LLM Evaluate
print("\n=== Bad LLM Candidate ===")
openaillm = OpenAIClient() # pass API key here
llmevaluator = LLMEvaluator(openaillm)

question = "where is Eiffel Tower"
generated = "The Eiffel Tower is located in Berlin."
reference = "The Eiffel Tower is located in Paris, France."

result = llmevaluator.evaluate(question, generated, reference)
print(result)

# output after run
# === Good Candidate ===
# BLEU: 0.8633
# ROUGE: {'rouge1': 0.8889, 'rouge2': 0.875, 'rougeL': 0.8889}

# === Bad Candidate ===
# BLEU: 0.0294
# ROUGE: {'rouge1': 0.2667, 'rouge2': 0.0, 'rougeL': 0.2667}

# === Bad LLM Candidate ===
# The generated answer is "Incorrect." 
# The reference answer accurately states that the Eiffel Tower is located in Paris, France, while the generated answer incorrectly claims it is located in Berlin. This is a clear factual contradiction, as the Eiffel Tower is a well-known landmark specifically associated with Paris.