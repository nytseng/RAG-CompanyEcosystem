import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from typing import List, Dict, Any
from chunking import (
    RecursiveChunkingStrategy,
    SentenceChunkingStrategy,
    ChunkingEvaluator,
)
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document
import json
import csv
from datetime import datetime


def load_articles() -> List[Document]:
    docs: List[Document] = []
    articles_dir = ROOT / "data" / "nvidia_articles"
    
    if articles_dir.exists():
        for path in articles_dir.rglob("*.txt"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                docs.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(path),
                            "doc_type": "article",
                        },
                    )
                )
            except Exception as e:
                print(f"Error loading {path}: {e}")
    
    print(f"Loaded {len(docs)} articles")
    return docs


def load_publications() -> List[Document]:
    docs: List[Document] = []
    pubs_dir = ROOT / "data" / "publications" / "rag_papers_text"
    
    if pubs_dir.exists():
        for path in pubs_dir.rglob("*.md"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                docs.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(path),
                            "doc_type": "publication",
                        },
                    )
                )
            except Exception as e:
                print(f"Error loading {path}: {e}")
    
    print(f"Loaded {len(docs)} publications")
    return docs


def load_transcripts() -> List[Document]:
    docs: List[Document] = []
    transcripts_dir = ROOT / "data" / "transcripts"
    
    if transcripts_dir.exists():
        for path in transcripts_dir.rglob("*.txt"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                docs.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(path),
                            "doc_type": "transcript",
                        },
                    )
                )
            except Exception as e:
                print(f"Error loading {path}: {e}")
    
    print(f"Loaded {len(docs)} transcripts")
    return docs


def test_article_parameters(articles: List[Document]) -> List[Dict[str, Any]]:
    print("\n" + "="*80)
    print("TESTING ARTICLE CHUNKING PARAMETERS")
    print("="*80)
    
    evaluator = ChunkingEvaluator()
    results = []
    
    chunk_sizes = [800, 1000, 1200, 1500]
    chunk_overlaps = [150, 200, 250, 300]
    
    for chunk_size in chunk_sizes:
        for chunk_overlap in chunk_overlaps:
            if chunk_overlap >= chunk_size * 0.5:
                continue
            
            strategy_name = f"recursive_{chunk_size}_{chunk_overlap}"
            print(f"\nTesting: {strategy_name}")
            
            try:
                strategy = RecursiveChunkingStrategy(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                
                chunks = strategy.chunk_documents(articles)
                metrics = evaluator.evaluate(chunks, articles)
                
                result = {
                    "data_type": "articles",
                    "strategy": "RecursiveCharacterTextSplitter",
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "num_chunks": metrics["num_chunks"],
                    "avg_chunk_size": round(metrics["avg_chunk_size"], 2),
                    "median_chunk_size": round(metrics["median_chunk_size"], 2),
                    "min_chunk_size": metrics["min_chunk_size"],
                    "max_chunk_size": metrics["max_chunk_size"],
                    "std_chunk_size": round(metrics["std_chunk_size"], 2),
                    "avg_chunks_per_doc": round(metrics.get("avg_chunks_per_doc", 0), 2),
                    **metrics.get("size_distribution", {})
                }
                
                results.append(result)
                print(f"  -> {metrics['num_chunks']} chunks, avg size: {metrics['avg_chunk_size']:.0f}")
                
            except Exception as e:
                print(f"  ERROR: {e}")
                continue
    
    return results


def test_publication_parameters(publications: List[Document]) -> List[Dict[str, Any]]:
    print("\n" + "="*80)
    print("TESTING PUBLICATION CHUNKING PARAMETERS")
    print("="*80)
    
    evaluator = ChunkingEvaluator()
    results = []
    
    chunk_sizes = [1200, 1500, 1800, 2000]
    chunk_overlaps = [200, 300, 400, 500]
    
    for chunk_size in chunk_sizes:
        for chunk_overlap in chunk_overlaps:
            if chunk_overlap >= chunk_size * 0.5:
                continue
            
            strategy_name = f"recursive_{chunk_size}_{chunk_overlap}"
            print(f"\nTesting: {strategy_name}")
            
            try:
                strategy = RecursiveChunkingStrategy(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                
                chunks = strategy.chunk_documents(publications)
                metrics = evaluator.evaluate(chunks, publications)
                
                result = {
                    "data_type": "publications",
                    "strategy": "RecursiveCharacterTextSplitter",
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "num_chunks": metrics["num_chunks"],
                    "avg_chunk_size": round(metrics["avg_chunk_size"], 2),
                    "median_chunk_size": round(metrics["median_chunk_size"], 2),
                    "min_chunk_size": metrics["min_chunk_size"],
                    "max_chunk_size": metrics["max_chunk_size"],
                    "std_chunk_size": round(metrics["std_chunk_size"], 2),
                    "avg_chunks_per_doc": round(metrics.get("avg_chunks_per_doc", 0), 2),
                    **metrics.get("size_distribution", {})
                }
                
                results.append(result)
                print(f"  -> {metrics['num_chunks']} chunks, avg size: {metrics['avg_chunk_size']:.0f}")
                
            except Exception as e:
                print(f"  ERROR: {e}")
                continue
    
    return results


def test_transcript_parameters(transcripts: List[Document]) -> List[Dict[str, Any]]:
    print("\n" + "="*80)
    print("TESTING TRANSCRIPT CHUNKING PARAMETERS")
    print("="*80)
    
    evaluator = ChunkingEvaluator()
    results = []
    
    sentences_per_chunk = [5, 6, 7, 8, 10, 12]
    sentence_overlaps = [1, 2, 3]
    
    for sentences in sentences_per_chunk:
        for overlap in sentence_overlaps:
            if overlap >= sentences * 0.5:
                continue
            
            strategy_name = f"sentence_{sentences}_{overlap}"
            print(f"\nTesting: {strategy_name}")
            
            try:
                strategy = SentenceChunkingStrategy(
                    sentences_per_chunk=sentences,
                    sentence_overlap=overlap
                )
                
                chunks = strategy.chunk_documents(transcripts)
                metrics = evaluator.evaluate(chunks, transcripts)
                
                result = {
                    "data_type": "transcripts",
                    "strategy": "SentenceChunkingStrategy",
                    "sentences_per_chunk": sentences,
                    "sentence_overlap": overlap,
                    "num_chunks": metrics["num_chunks"],
                    "avg_chunk_size": round(metrics["avg_chunk_size"], 2),
                    "median_chunk_size": round(metrics["median_chunk_size"], 2),
                    "min_chunk_size": metrics["min_chunk_size"],
                    "max_chunk_size": metrics["max_chunk_size"],
                    "std_chunk_size": round(metrics["std_chunk_size"], 2),
                    "avg_chunks_per_doc": round(metrics.get("avg_chunks_per_doc", 0), 2),
                    **metrics.get("size_distribution", {})
                }
                
                results.append(result)
                print(f"  -> {metrics['num_chunks']} chunks, avg size: {metrics['avg_chunk_size']:.0f}")
                
            except Exception as e:
                print(f"  ERROR: {e}")
                continue
    
    return results


def save_results(all_results: List[Dict[str, Any]], output_dir: Path):
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    json_path = output_dir / f"chunking_parameter_test_results_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✅ Saved JSON results to: {json_path}")
    
    for data_type in ["articles", "publications", "transcripts"]:
        type_results = [r for r in all_results if r["data_type"] == data_type]
        if type_results:
            csv_path = output_dir / f"{data_type}_chunking_results_{timestamp}.csv"
            
            fieldnames = set()
            for result in type_results:
                fieldnames.update(result.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(type_results)
            print(f"✅ Saved {data_type} CSV to: {csv_path}")
    
    summary_path = output_dir / f"chunking_test_summary_{timestamp}.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("CHUNKING PARAMETER TEST RESULTS SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for data_type in ["articles", "publications", "transcripts"]:
            type_results = [r for r in all_results if r["data_type"] == data_type]
            if type_results:
                f.write(f"\n{data_type.upper()}\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total parameter combinations tested: {len(type_results)}\n\n")
                
                target_size = 1000 if data_type != "transcripts" else 800
                
                def score_result(result):
                    size_diff = abs(result["avg_chunk_size"] - target_size)
                    size_penalty = (size_diff / target_size) * 0.4
                    
                    cv = result["std_chunk_size"] / result["avg_chunk_size"] if result["avg_chunk_size"] > 0 else 1.0
                    consistency_penalty = cv * 0.3
                    
                    total_chunks = result["num_chunks"]
                    if total_chunks > 0:
                        medium_count = result.get("medium (500-1000)", 0)
                        large_count = result.get("large (1000-2000)", 0) if data_type != "transcripts" else 0
                        optimal_ratio = (medium_count + large_count * 0.5) / total_chunks
                        distribution_penalty = (1 - optimal_ratio) * 0.2
                    else:
                        distribution_penalty = 0.2
                    
                    tiny_count = result.get("tiny (< 100)", 0)
                    tiny_ratio = tiny_count / total_chunks if total_chunks > 0 else 0
                    tiny_penalty = tiny_ratio * 0.1
                    
                    total_score = size_penalty + consistency_penalty + distribution_penalty + tiny_penalty
                    return total_score
                
                scored_results = [(score_result(r), r) for r in type_results]
                scored_results.sort(key=lambda x: x[0])
                best = scored_results[0][1]
                best_score = scored_results[0][0]
                
                f.write("Recommended Parameters:\n")
                f.write(f"  (Selected using multi-factor scoring: size proximity 40%, consistency 30%, ")
                f.write(f"distribution 20%, avoid tiny chunks 10%)\n")
                if data_type == "transcripts":
                    f.write(f"  Strategy: SentenceChunkingStrategy\n")
                    f.write(f"  sentences_per_chunk: {best['sentences_per_chunk']}\n")
                    f.write(f"  sentence_overlap: {best['sentence_overlap']}\n")
                else:
                    f.write(f"  Strategy: RecursiveCharacterTextSplitter\n")
                    f.write(f"  chunk_size: {best['chunk_size']}\n")
                    f.write(f"  chunk_overlap: {best['chunk_overlap']}\n")
                f.write(f"  Results: {best['num_chunks']} chunks, avg size: {best['avg_chunk_size']:.0f}, ")
                f.write(f"std: {best['std_chunk_size']:.0f}\n")
                f.write(f"  Score: {best_score:.4f} (lower is better)\n\n")
                
                f.write("Top 3 Alternatives (for comparison):\n")
                for i, (score, result) in enumerate(scored_results[1:4], 1):
                    if data_type == "transcripts":
                        f.write(f"  {i}. sentences={result['sentences_per_chunk']}, overlap={result['sentence_overlap']}, ")
                    else:
                        f.write(f"  {i}. size={result['chunk_size']}, overlap={result['chunk_overlap']}, ")
                    f.write(f"chunks={result['num_chunks']}, avg={result['avg_chunk_size']:.0f}, score={score:.4f}\n")
                f.write("\n")
    
    print(f"✅ Saved summary report to: {summary_path}")
    
    return json_path, summary_path


def main():
    print("="*80)
    print("CHUNKING PARAMETER TESTING FOR ALL DATA TYPES")
    print("="*80)
    
    print("\nLoading data...")
    articles = load_articles()
    publications = load_publications()
    transcripts = load_transcripts()
    
    if not articles and not publications and not transcripts:
        print("ERROR: No documents loaded. Check data directory paths.")
        return
    
    all_results = []
    
    if articles:
        article_results = test_article_parameters(articles)
        all_results.extend(article_results)
    else:
        print("\n⚠️  No articles found, skipping article tests")
    
    if publications:
        publication_results = test_publication_parameters(publications)
        all_results.extend(publication_results)
    else:
        print("\n⚠️  No publications found, skipping publication tests")
    
    if transcripts:
        transcript_results = test_transcript_parameters(transcripts)
        all_results.extend(transcript_results)
    else:
        print("\n⚠️  No transcripts found, skipping transcript tests")
    
    output_dir = ROOT / "chunking" / "test_results"
    json_path, summary_path = save_results(all_results, output_dir)
    
    print("\n" + "="*80)
    print("TESTING COMPLETE!")
    print("="*80)
    print(f"\nTotal parameter combinations tested: {len(all_results)}")
    print(f"\nResults saved to:")
    print(f"  - JSON: {json_path}")
    print(f"  - Summary: {summary_path}")
    print(f"\nShare these files with your partner for analysis!")


if __name__ == "__main__":
    main()

