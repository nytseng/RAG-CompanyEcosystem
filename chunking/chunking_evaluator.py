from typing import List, Dict, Any, Optional
try:
    from langchain.schema import Document
except ImportError:
    from langchain_core.documents import Document
import numpy as np


class ChunkingEvaluator:

    
    def __init__(self):
        pass
    
    def evaluate(
        self,
        chunks: List[Document],
        original_documents: Optional[List[Document]] = None
    ) -> Dict[str, Any]:
       
        metrics: Dict[str, Any] = {}
        
        metrics["num_chunks"] = len(chunks)
        metrics["chunk_sizes"] = [len(chunk.page_content) for chunk in chunks]
        
        if metrics["chunk_sizes"]:
            metrics["avg_chunk_size"] = float(np.mean(metrics["chunk_sizes"]))
            metrics["median_chunk_size"] = float(np.median(metrics["chunk_sizes"]))
            metrics["min_chunk_size"] = int(np.min(metrics["chunk_sizes"]))
            metrics["max_chunk_size"] = int(np.max(metrics["chunk_sizes"]))
            metrics["std_chunk_size"] = float(np.std(metrics["chunk_sizes"]))
            metrics["size_distribution"] = self._compute_size_distribution(metrics["chunk_sizes"])
        else:
            metrics["avg_chunk_size"] = 0.0
            metrics["median_chunk_size"] = 0.0
            metrics["min_chunk_size"] = 0
            metrics["max_chunk_size"] = 0
            metrics["std_chunk_size"] = 0.0
            metrics["size_distribution"] = {}
        
        if chunks and chunks[0].metadata:
            metrics["metadata_keys"] = list(chunks[0].metadata.keys())
        
        if original_documents:
            original_total_size = sum(len(doc.page_content) for doc in original_documents)
            chunked_total_size = sum(len(chunk.page_content) for chunk in chunks)
            metrics["total_size_original"] = original_total_size
            metrics["total_size_chunked"] = chunked_total_size
            metrics["size_increase_ratio"] = chunked_total_size / original_total_size if original_total_size > 0 else 0
            metrics["num_original_docs"] = len(original_documents)
            metrics["avg_chunks_per_doc"] = len(chunks) / len(original_documents) if original_documents else 0
        
        overlap_info = self._analyze_overlaps(chunks)
        metrics.update(overlap_info)
        
        return metrics
    
    def _compute_size_distribution(self, sizes: List[int]) -> Dict[str, int]:
        if not sizes:
            return {}
        
        buckets = {
            "tiny (< 100)": 0,
            "small (100-500)": 0,
            "medium (500-1000)": 0,
            "large (1000-2000)": 0,
            "very_large (> 2000)": 0,
        }
        
        for size in sizes:
            if size < 100:
                buckets["tiny (< 100)"] += 1
            elif size < 500:
                buckets["small (100-500)"] += 1
            elif size < 1000:
                buckets["medium (500-1000)"] += 1
            elif size < 2000:
                buckets["large (1000-2000)"] += 1
            else:
                buckets["very_large (> 2000)"] += 1
        
        return buckets
    
    def _analyze_overlaps(self, chunks: List[Document]) -> Dict[str, Any]:
        overlap_info = {
            "has_overlap_info": False,
            "avg_overlap": None,
        }

        overlaps = []
        for chunk in chunks:
            if "overlap_size" in chunk.metadata:
                overlaps.append(chunk.metadata["overlap_size"])
        
        if overlaps:
            overlap_info["has_overlap_info"] = True
            overlap_info["avg_overlap"] = np.mean(overlaps)
            overlap_info["overlaps"] = overlaps
        
        return overlap_info
    
    def print_evaluation_report(self, metrics: Dict[str, Any], strategy_name: str = ""):
        print(f"\n{'='*60}")
        print(f"Chunking Evaluation Report: {strategy_name}")
        print(f"{'='*60}")
        
        print(f"\nBasic Statistics:")
        print(f"  Number of chunks: {metrics['num_chunks']}")
        print(f"  Average chunk size: {metrics['avg_chunk_size']:.2f} characters")
        print(f"  Median chunk size: {metrics['median_chunk_size']:.2f} characters")
        print(f"  Min chunk size: {metrics['min_chunk_size']} characters")
        print(f"  Max chunk size: {metrics['max_chunk_size']} characters")
        print(f"  Std deviation: {metrics['std_chunk_size']:.2f} characters")
        
        if "size_distribution" in metrics:
            print(f"\nSize Distribution:")
            for bucket, count in metrics["size_distribution"].items():
                print(f"  {bucket}: {count} chunks")
        
        if "num_original_docs" in metrics:
            print(f"\nDocument Comparison:")
            print(f"  Original documents: {metrics['num_original_docs']}")
            print(f"  Average chunks per document: {metrics['avg_chunks_per_doc']:.2f}")
            if "size_increase_ratio" in metrics:
                print(f"  Size increase ratio: {metrics['size_increase_ratio']:.2f}x")
        
        if metrics.get("has_overlap_info"):
            print(f"\nOverlap Analysis:")
            print(f"  Average overlap: {metrics['avg_overlap']:.2f} characters")
        
        print(f"{'='*60}\n")

