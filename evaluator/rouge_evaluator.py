# text_eval/rouge_evaluator.py
from rouge_score import rouge_scorer

class ROUGEEvaluator:
    def __init__(self, metrics=('rouge1', 'rouge2', 'rougeL')):
        """
        Initialize ROUGE evaluator with chosen metrics.
        """
        self.scorer = rouge_scorer.RougeScorer(metrics, use_stemmer=True)

    def evaluate(self, reference: str, candidate: str) -> dict:
        """
        Compute ROUGE scores between reference and candidate strings.
        """
        scores = self.scorer.score(reference, candidate)
        result = {k: round(v.fmeasure, 4) for k, v in scores.items()}
        return result
