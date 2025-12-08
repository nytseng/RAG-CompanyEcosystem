import os
from typing import List, Dict, Any, Optional
import asyncio

from ragas import evaluate, SingleTurnSample, EvaluationDataset
from ragas.llms import llm_factory
from ragas.embeddings import embedding_factory, HuggingFaceEmbeddings
from ragas.metrics.collections import (
    ContextPrecision,
    ContextRecall,
    Faithfulness,
    AnswerRelevancy,
    FactualCorrectness,
)


from base_evaluator import BaseEvaluator
from llm_evaluator import LLMClient


class RagasEvaluator(BaseEvaluator):
    """
    Wraps ragas.evaluate for a single example and adds retrieval metrics.
    """

    def __init__(self, llm_client: LLMClient):
        """
        Pass in an LLMClient (OpenAIClient, ClaudeClient, LocalLLMClient, etc.)
        """
        self.model = llm_factory(llm_client.model, provider=llm_client.provider, client=llm_client.async_client, max_tokens=8192)
        self.embedding = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

        self.faithfulness_metric = Faithfulness(llm=self.model)
        self.context_precision_metric = ContextPrecision(llm=self.model)
        self.context_recall_metric = ContextRecall(llm=self.model)
        self.response_relevancy_metric = AnswerRelevancy(llm=self.model, embeddings=self.embedding)

    def _compute_retrieval_metrics(
        self,
        gold_documents: List[Dict],
        retrieved_context: List[Dict],
    ) -> Dict[str, float]:
        """
        Compute precision@1, precision@5, recall@1, recall@5.
        """

        # Gold IDs (from ground_truth "documents" entries)
        gold_ids = set()
        for doc in gold_documents:
            doc_id = self.parse_document_id(doc)
            if doc_id is not None:
                gold_ids.add(doc_id)

        # Retrieved IDs (from results "context" entries), deduped in order
        retrieved_ids: List[str] = []
        seen = set()
        for ctx in retrieved_context:
            doc_id = self.parse_document_id(ctx)
            if doc_id is not None and doc_id not in seen:
                seen.add(doc_id)
                retrieved_ids.append(doc_id)

        def prec_recall_at_k(k: int):
            topk = retrieved_ids[:k]
            if not topk:
                return 0.0, 0.0

            # unique hits among top-k
            hits = len(gold_ids.intersection(topk))

            precision = hits / len(topk)
            recall = hits / len(gold_ids) if gold_ids else 0.0
            return precision, recall

        p1, r1 = prec_recall_at_k(1)
        p5, r5 = prec_recall_at_k(5)

        return {
            "precision@1": round(p1, 4),
            "precision@5": round(p5, 4),
            "recall@1": round(r1, 4),
            "recall@5": round(r5, 4),
        }

    def evaluate(
        self,
        question: str,
        response: str,
        gold_documents: List[Dict],
        retrieved_context: List[Dict],
        reference_answer: Optional[str] = None
    ) -> Dict[str, Any]:
        return asyncio.run(self.aevaluate(question, response, gold_documents, retrieved_context, reference_answer))


    async def aevaluate(
        self,
        question: str,
        response: str,
        gold_documents: List[Dict],
        retrieved_context: List[Dict],
        reference_answer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run ragas on (question, retrieved texts) + compute retrieval metrics.

        Returns:
        {
            "ragas_scores": [...],
            "ragas_avg": float,
            "precision@1": float,
            "precision@5": float,
            "recall@1": float,
            "recall@5": float,
        }
        """
        retrieved_texts: List[str] = [t for t in (self.parse_document_text(c) for c in retrieved_context) if t is not None]

        # Always compute classical retrieval metrics
        retrieval = self._compute_retrieval_metrics(gold_documents, retrieved_context)

        # If we have no texts or no model, just return retrieval metrics
        if not retrieved_texts or self.model is None:
            return retrieval

        ragas_scores: Dict[str, Any] = {}

        # Faithfulness
        faithfulness_result = await self.faithfulness_metric.ascore(
            user_input=question,
            response=response,
            retrieved_contexts=retrieved_texts,
        )
        ragas_scores["ragas/faithfulness"] = faithfulness_result.value

        # Context Precision
        if reference_answer is not None:
            context_precision_result = await self.context_precision_metric.ascore(
                user_input=question,
                reference=reference_answer,
                retrieved_contexts=retrieved_texts,
            )
            ragas_scores["ragas/context_precision"] = context_precision_result.value

            # Context Recall
            context_recall_result = await self.context_recall_metric.ascore(
                user_input=question,
                retrieved_contexts=retrieved_texts,
                reference=reference_answer,
            )
            ragas_scores["ragas/context_recall"] = context_recall_result.value
        else:
            ragas_scores["ragas/context_precision"] = None
            ragas_scores["ragas/context_recall"] = None

        # Response Relevancy
        response_relevancy_result = await self.response_relevancy_metric.ascore(
            user_input=question,
            response=response,
        )
        ragas_scores["ragas/response_relevancy"] = response_relevancy_result.value

        return {
            **ragas_scores,
            **retrieval,
        }


