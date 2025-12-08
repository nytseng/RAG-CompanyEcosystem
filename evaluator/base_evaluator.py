from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os


class BaseEvaluator(ABC):
    """
    Base interface: all evaluators should take a *single example*
    (question, response, gold docs, retrieved context) and return a dict.
    """

    @abstractmethod
    def evaluate(
        self,
        question: str,
        response: str,
        gold_documents: List[Dict],
        retrieved_context: List[Dict],
        reference_answer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate one example and return a dictionary of metrics.
        - question: ground truth request string
        - response: model-generated response string
        - gold_documents: list of { "document": str, "text": str }
        - retrieved_context: list of { "content": str, "metadata": { "source": str, ... } }
        - reference_answer: "ground truth" answer to the question
        """
        raise NotImplementedError
    
    @staticmethod
    def parse_document_id(entry: Dict) -> str | None:
        doc_id = None
        if "document" in entry:
            doc_id = entry.get("document")
        elif "source" in entry:
            doc_id = entry.get("source")
        elif "file" in entry:
            doc_id = entry.get("file")
        elif "metadata" in entry:
            metadata = entry.get("metadata", {})
            doc_id = metadata.get("source")

        if doc_id is not None:
            doc_id = os.path.basename(doc_id.replace("\\", "/"))
        return doc_id
    
    @staticmethod
    def parse_document_text(entry: Dict) -> str:
        doc_text = ""
        if "doc" in entry:
            doc_text = entry.get("doc")
        elif "text" in entry:
            doc_text = entry.get("text")
        elif "content" in entry:
            doc_text = entry.get("content")

        return doc_text
    
    @staticmethod
    def parse_documents_list(entry: Dict) -> List[Dict]:
        doc_list = None
        if "documents" in entry:
            doc_list = entry.get("documents")
        elif "context" in entry:
            doc_list = entry.get("context")
        elif "result" in entry:
            doc_list = entry.get("result")

        return doc_list