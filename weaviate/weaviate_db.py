import os
import weaviate
# --- UPDATED IMPORT ---
# langchain_community.vectorstores.Weaviate is deprecated in favor of langchain_weaviate.vectorstores.WeaviateVectorStore
from langchain_weaviate.vectorstores import WeaviateVectorStore 
# --- UNCHANGED IMPORTS ---
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- Configuration ---
WEAVIATE_URL = "http://localhost:8080"
WEAVIATE_CLASS_NAME = "NvidiaInfo"
ARTICLE_DIR = "../data" # This should match the directory from the scraping script

# --- Embedding Model Setup (Hugging Face) ---
# NOTE: The first time this runs, the model will be downloaded to your machine.
MODEL_NAME = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
print(f"✅ Initialized Hugging Face Embeddings with model: {MODEL_NAME}")

# --- 1. Load Documents from Directory ---
def load_documents():
    """Loads all .txt files from the specified directory using LangChain."""
    print(f"\n1️⃣ Starting document loading from '{ARTICLE_DIR}/'...")
    try:
        # Use LangChain's DirectoryLoader to read all files ending in .txt
        loader = DirectoryLoader(
            path=ARTICLE_DIR, 
            glob="*.txt/", 
            loader_kwargs={"encoding": "utf-8"},
            silent_errors=True,
            recursive=True
        )
        documents = loader.load()
        print(f"   ✅ Loaded {len(documents)} total documents.")
        loader = DirectoryLoader(
            path=ARTICLE_DIR, 
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

# --- 3. Initialize Weaviate Client and Schema ---
def setup_weaviate_client():
    """Initializes the Weaviate client and ensures the class schema exists."""
    print(f"3️⃣ Connecting to Weaviate at {WEAVIATE_URL}...")
    try:
        # Weaviate client connection (this uses the v4 weaviate-client library)
        client = weaviate.connect_to_local()
        client.is_live() # Check if the instance is reachable
        print("   ✅ Successfully connected to Weaviate.")
        return client
    except Exception as e:
        print(f"   ❌ Error connecting to Weaviate. Is the Docker container running? Details: {e}")
        return None

def configure_weaviate_schema(client):
    """Configures the schema for the NvidiaNewsArticleHF class."""
    # Note: Using the v4 client, collections are the new name for classes.
    # The LangChain integration handles this conversion seamlessly.

    # Delete class if it exists to ensure a clean start
    if client.collections.exists(WEAVIATE_CLASS_NAME):
        print(f"   ⚠️ Deleting existing class '{WEAVIATE_CLASS_NAME}' for clean setup...")
        client.collections.delete(WEAVIATE_CLASS_NAME)
    
    # Define the new collection schema
    # When vectorizer is 'none', Weaviate expects the vectors to be provided at import time.
    from weaviate.classes.config import Configure, Property, DataType
    
    client.collections.create(
        name=WEAVIATE_CLASS_NAME,
        description="NVIDIA Newsletter and Newsroom articles (Hugging Face Vectorized).",
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(
                name="text",
                data_type=DataType.TEXT,
                description="The chunked content of the article.",
            ),
            Property(
                name="source",
                data_type=DataType.TEXT,
                description="The file path (source) of the original article.",
            ),
        ],
    )
    print(f"   ✅ Created Weaviate class '{WEAVIATE_CLASS_NAME}'.")


# --- 4. Upload Data to Weaviate ---
def upload_to_weaviate(chunks, client):
    """Uses LangChain's Weaviate integration to upload all chunks."""
    print("\n4️⃣ Generating embeddings and uploading documents...")

    # The class is now WeaviateVectorStore
    try:
        vectorstore = WeaviateVectorStore.from_documents(
            chunks,
            embeddings,
            client=client,
            index_name=WEAVIATE_CLASS_NAME,
            # 'text_key' is often required in the new package 
            # and defaults to 'text' (which matches the schema we set up).
            text_key="text", 
        )
        print(f"   ✅ Successfully injected {len(chunks)} vectors into Weaviate.")
        return vectorstore
    except Exception as e:
        print(f"   ❌ Error during data upload to Weaviate. Details: {e}")
        return None

# --- Main Execution ---
def main():
    """Runs the full pipeline to load and ingest data."""
    if not os.path.isdir(ARTICLE_DIR):
        print(f"The directory '{ARTICLE_DIR}' was not found. Please run the scraping script first.")
        return

    # 1. Load and Split
    documents = load_documents()
    if not documents:
        print("No documents found. Exiting.")
        return
        
    chunks = split_documents(documents)

    # 2. Setup Weaviate
    client = setup_weaviate_client()
    if not client:
        return
        
    # **NOTE**: The schema creation logic needed an update for the new Weaviate v4 client syntax.
    configure_weaviate_schema(client)

    # 3. Upload Data
    vectorstore = upload_to_weaviate(chunks, client)
    
    if vectorstore:
        print("\n--- INGESTION COMPLETE ---")
        print(f"Your data is now in the Weaviate collection/class '{WEAVIATE_CLASS_NAME}'.")
        print("You can now perform vector similarity searches.")

if __name__ == "__main__":
    main()