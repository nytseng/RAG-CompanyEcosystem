from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

class BLEUEvaluator:
    def __init__(self, weights=(0.25, 0.25, 0.25, 0.25)):
        """
        Initialize BLEU evaluator with optional n-gram weights.
        Default: BLEU-4 with uniform weights.
        """
        self.weights = weights
        self.smooth_fn = SmoothingFunction().method1

    def evaluate(self, reference: str, candidate: str) -> float:
        """
        Compute BLEU score between reference and candidate strings.
        """
        ref_tokens = [reference.split()]
        cand_tokens = candidate.split()
        score = sentence_bleu(ref_tokens, cand_tokens, weights=self.weights, smoothing_function=self.smooth_fn)
        return round(score, 4)