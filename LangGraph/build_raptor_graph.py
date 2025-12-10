import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from raptor.raptor import BaseSummarizationModel, BaseQAModel, BaseEmbeddingModel
from langchain_community.embeddings import HuggingFaceEmbeddings

LLM_MODEL = "gemma3" 
OLLAMA_BASE_URL = "http://localhost:11434" # Hostname 'ollama' comes from docker-compose
MODEL_NAME = "all-MiniLM-L6-v2"
# Initialize Local LLM
llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

ARTICLE_DIR = "../data"
MODEL_NAME = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
print(f"✅ Initialized Hugging Face Embeddings with model: {MODEL_NAME}")

class OllamaSummarizationModel(BaseSummarizationModel):
    def __init__(self, llm):
        self.llm = llm
    
    def summarize(self, context, max_tokens=150):
        """Create NVIDIA-specific technical summary using our custom prompt"""
        
        # Our domain-specific technical prompt
        prompt = f"""You are an expert technical analyst specializing in NVIDIA technologies.

            Here is a cluster of documents about NVIDIA technologies. Your goal is to compress the information into a detailed summary that preserves specific names, numbers, and causal relationships.

            DO NOT write a vague overview.
            DO NOT use phrases like "The documents discuss..." or "This cluster covers..."

            STRUCTURE:
            1. **Technical Specifications**: List specific hardware specs, versions, and benchmarks found in the text.
            2. **Key Entities**: List specific product names, partner companies, and software tools.
            3. **Strategic Insights**: Explain the *how* and *why* connecting these entities.

            Context:
            {context}

            DETAILED TECHNICAL SUMMARY:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"❌ Error in summarization: {e}")
            return f"Technical summary of NVIDIA-related content covering hardware specifications, software frameworks, and strategic business relationships. Content spans multiple documents with technical details about GPU architectures, AI/ML platforms, and industry partnerships."

class HFEmbeddingModel(BaseEmbeddingModel):
    def __init__(self, model="text-embedding-ada-002"):
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    def create_embedding(self, text):
        text = text.replace("\n", " ")
        return (
            self.embeddings.embed_query(text)
        )

class OllamaQAModel(BaseQAModel):
    """Adapter for Ollama LLM to work with RAPTOR library Q&A"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def answer_question(self, context, question):
        """Answer question using NVIDIA-specific context"""
        
        prompt = f"""You are an AI assistant specializing in NVIDIA technologies, products, and business strategy.

            Use the provided context to answer questions accurately and comprehensively. The context includes original NVIDIA documents and hierarchical summaries at different abstraction levels.

            **Instructions:**
            - Provide detailed, accurate answers based on the context
            - Reference specific NVIDIA technologies, products, and initiatives when relevant
            - Synthesize information from multiple sources and abstraction levels
            - Maintain technical accuracy while ensuring clarity
            - If information isn't available in context, state this clearly

            **Context:**
            {context}

            **Question:** {question}

            **Comprehensive Answer:**"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"❌ Error in Q&A: {e}")
            return f"Error processing question: {e}"

from raptor.raptor import RetrievalAugmentation, RetrievalAugmentationConfig

# Initialize your custom models
custom_summarizer = OllamaSummarizationModel(llm)
custom_qa = OllamaQAModel(llm)
custom_embedding = HFEmbeddingModel()

# Create a config with your custom models
custom_config = RetrievalAugmentationConfig(
    summarization_model=custom_summarizer,
    qa_model=custom_qa,
    embedding_model=custom_embedding
)



# Initialize RAPTOR with your custom config


# --- 1. Load Documents from Directory ---
def load_documents(d):
    """Loads all .txt files from the specified directory using LangChain."""
    print(f"\n1️⃣ Starting document loading from '{d}/'...")
    try:
        # Use LangChain's DirectoryLoader to read all files ending in .txt
        loader = DirectoryLoader(
            path=d, 
            glob="*.txt/", 
            loader_kwargs={"encoding": "utf-8"},
            silent_errors=True,
            recursive=True
        )
        documents = loader.load()
        print(f"   ✅ Loaded {len(documents)} total documents.")
        loader = DirectoryLoader(
            path=d, 
            glob="*.md/", 
            loader_kwargs={"encoding": "utf-8"},
            silent_errors=True,
            recursive=True
        )
        documents += loader.load()

        print(f"   ✅ Loaded {len(documents)} total documents.")
        return documents
    except Exception as e:
        print(f"   ❌ Error during document loading: {e}")
        return []

# --- 2. Split Documents into Chunks ---
def split_documents(documents):
    """Splits large documents into smaller, overlapping chunks."""
    print("2️⃣ Splitting documents into manageable chunks...")
    # Smaller chunks are generally better for RAG/vector search
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"   ✅ Split into {len(chunks)} text chunks.")
    return chunks

"""Runs the full pipeline to load and ingest data."""
dirList = ["../data/nvidia_articles", "../data/publications", "../data/transcripts", "../data"]
classList = ["RaptorNvidiaArticles", "RaptorNvidiaPublications", "RaptorNvidiaTranscripts", "RaptorNvidiaInfo"]
for d, c in zip(dirList, classList):
    RA = RetrievalAugmentation(config=custom_config)
    if not os.path.isdir(d):
        print(f"The directory '{d}' was not found. Please run the scraping script first.")
        break

    # 1. Load and Split
    documents = load_documents(d)
    if not documents:
        print("No documents found. Exiting.")
        break
        
    chunks = split_documents(documents)


    RA.add_documents("".join([chunk.page_content for chunk in chunks]))
    
    RA.save(c)
    print("\n--- INGESTION COMPLETE ---")
