from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)
try:
    from langchain.schema import Document
except ImportError:
    from langchain_core.documents import Document
import re


class ChunkingStrategy(ABC):
    
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.params = kwargs
    
    @abstractmethod
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        pass
    
    def get_strategy_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "params": self.params
        }


class RecursiveChunkingStrategy(ChunkingStrategy):
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None,
        length_function: callable = len,
        **kwargs
    ):
        super().__init__("RecursiveChunking", **kwargs)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function
        
        if separators is None:
            self.separators = [
                "\n\n\n",  # Multiple newlines (paragraph breaks)
                "\n\n",    # Double newlines
                "\n",      # Single newlines
                ". ",      # Sentence endings
                " ",       # Spaces
                "",        # Characters
            ]
        else:
            self.separators = separators
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=self.separators,
            length_function=length_function,
        )
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        chunks = []
        for doc in documents:
            doc_chunks = self.splitter.split_documents([doc])
            chunks.extend(doc_chunks)
        return chunks


class MarkdownHeaderChunkingStrategy(ChunkingStrategy):
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        headers_to_split_on: Optional[List[tuple]] = None,
        **kwargs
    ):
        super().__init__("MarkdownHeaderChunking", **kwargs)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if headers_to_split_on is None:
            self.headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
                ("####", "Header 4"),
            ]
        else:
            self.headers_to_split_on = headers_to_split_on
        
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on
        )
        
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        chunks = []
        for doc in documents:
            header_chunks = self.markdown_splitter.split_text(doc.page_content)
            
            for header_chunk in header_chunks:
                if isinstance(header_chunk, str):
                    temp_doc = Document(page_content=header_chunk, metadata=doc.metadata)
                    final_chunks = self.recursive_splitter.split_documents([temp_doc])
                else:
                    final_chunks = self.recursive_splitter.split_documents([header_chunk])
                chunks.extend(final_chunks)
        return chunks


class SentenceChunkingStrategy(ChunkingStrategy):
    
    def __init__(
        self,
        sentences_per_chunk: int = 5,
        sentence_overlap: int = 1,
        **kwargs
    ):
        super().__init__("SentenceChunking", **kwargs)
        self.sentences_per_chunk = sentences_per_chunk
        self.sentence_overlap = sentence_overlap
    
    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        chunks = []
        for doc in documents:
            sentences = self._split_into_sentences(doc.page_content)
            
            for i in range(0, len(sentences), self.sentences_per_chunk - self.sentence_overlap):
                chunk_sentences = sentences[i:i + self.sentences_per_chunk]
                chunk_text = " ".join(chunk_sentences)
                
                chunk = Document(
                    page_content=chunk_text,
                    metadata={**doc.metadata, "chunk_index": i}
                )
                chunks.append(chunk)
        return chunks


class DomainAwareRecursiveChunkingStrategy(RecursiveChunkingStrategy):

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        preserve_code_blocks: bool = True,
        preserve_equations: bool = True,
        **kwargs
    ):
        super().__init__(chunk_size, chunk_overlap, **kwargs)
        self.name = "DomainAwareRecursiveChunking"
        self.preserve_code_blocks = preserve_code_blocks
        self.preserve_equations = preserve_equations
    
    def _preserve_special_content(self, text: str) -> Tuple[str, Dict[str, str]]:
        placeholders = {}
        placeholder_counter = 0
        
        if self.preserve_code_blocks:
            code_block_pattern = r'```[\s\S]*?```'
            for match in re.finditer(code_block_pattern, text):
                placeholder = f"__CODE_BLOCK_{placeholder_counter}__"
                placeholders[placeholder] = match.group(0)
                text = text.replace(match.group(0), placeholder)
                placeholder_counter += 1
        
        if self.preserve_code_blocks:
            inline_code_pattern = r'`[^`]+`'
            for match in re.finditer(inline_code_pattern, text):
                placeholder = f"__INLINE_CODE_{placeholder_counter}__"
                placeholders[placeholder] = match.group(0)
                text = text.replace(match.group(0), placeholder)
                placeholder_counter += 1
        
        if self.preserve_equations:
            equation_pattern = r'\$[\s\S]*?\$'
            for match in re.finditer(equation_pattern, text):
                placeholder = f"__EQUATION_{placeholder_counter}__"
                placeholders[placeholder] = match.group(0)
                text = text.replace(match.group(0), placeholder)
                placeholder_counter += 1
        
        return text, placeholders
    
    def _restore_special_content(self, text: str, placeholders: Dict[str, str]) -> str:
        for placeholder, original in placeholders.items():
            text = text.replace(placeholder, original)
        return text
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        chunks = []
        for doc in documents:
            processed_text, placeholders = self._preserve_special_content(doc.page_content)
            
            temp_doc = Document(page_content=processed_text, metadata=doc.metadata)
            
            doc_chunks = self.splitter.split_documents([temp_doc])
            
            for chunk in doc_chunks:
                chunk.page_content = self._restore_special_content(chunk.page_content, placeholders)
                chunks.append(chunk)
        
        return chunks

