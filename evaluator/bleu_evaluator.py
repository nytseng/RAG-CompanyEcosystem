from typing import List, Dict, Any, Optional
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from base_evaluator import BaseEvaluator


class BLEUEvaluator(BaseEvaluator):
    def __init__(self, weights=(0.25, 0.25, 0.25, 0.25)):
        """
        Initialize BLEU evaluator with optional n-gram weights.
        Default: BLEU-4 with uniform weights.
        """
        self.weights = weights
        self.smooth_fn = SmoothingFunction().method1

    def _make_reference(self, gold_documents: List[Dict]) -> str:
        return " ".join(self.parse_document_text(doc) for doc in gold_documents).strip()

    def evaluate(
        self,
        question: str,
        response: str,
        gold_documents: List[Dict],
        retrieved_context: List[Dict],
        reference_answer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compute BLEU score between reference and candidate strings.
        """

        # Use explicit reference if provided
        reference = reference_answer or self._make_reference(gold_documents)

        if not reference or not response:
            return {"bleu": 0.0}

        ref_tokens = [reference.split()]
        cand_tokens = response.split()

        score = sentence_bleu(
            ref_tokens,
            cand_tokens,
            weights=self.weights,
            smoothing_function=self.smooth_fn,
        )
        return {"bleu": round(float(score), 4)}
