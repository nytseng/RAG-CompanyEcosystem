from typing import List, Dict, Any, Optional
from rouge_score import rouge_scorer

from base_evaluator import BaseEvaluator


class ROUGEEvaluator(BaseEvaluator):
    def __init__(self, metrics=("rouge1", "rouge2", "rougeL")):
        """
        Initialize ROUGE evaluator with chosen metrics.
        """
        self.scorer = rouge_scorer.RougeScorer(metrics, use_stemmer=True)

    def _make_reference(self, gold_documents: List[Dict]) -> str:
        return " ".join(self.parse_document_text(doc) for doc in gold_documents).strip()

    def evaluate(
        self,
        question: str,
        response: str,
        gold_documents: List[Dict],
        retrieved_context: List[Dict],
        reference_answer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Compute ROUGE scores between reference and candidate strings.
        """

        reference = reference_answer or self._make_reference(gold_documents)

        if not reference or not response:
            return {m: 0.0 for m in self.scorer.metrics}

        scores = self.scorer.score(reference, response)
        result = {k: round(v.fmeasure, 4) for k, v in scores.items()}
        return result
