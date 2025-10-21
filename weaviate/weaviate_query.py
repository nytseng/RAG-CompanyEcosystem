import weaviate
import os
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery

# LangChain Imports
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.documents import Document
# Corrected Import to match ingestion script
from langchain_community.embeddings import HuggingFaceEmbeddings 

# --- Configuration (Update these values) ---
WEAVIATE_URL = "http://localhost:8080"
COLLECTION_NAME = "NvidiaNewsArticleHF" 
# Define the model used for ingestion (must match your ingestion script)
MODEL_NAME = "all-MiniLM-L6-v2"

def initialize_client():
    """Initializes and returns the raw Weaviate client and the LangChain VectorStore."""
    try:
        # 1. Initialize the raw Weaviate client
        client = weaviate.connect_to_local() 
        if not client.is_ready():
            print("❌ Weaviate client is not ready. Check your Docker container.")
            return None, None
            
        print(f"✅ Raw Weaviate client connected successfully at {WEAVIATE_URL}")

        # 2. Initialize the Embedding Model (MUST match ingestion model)
        embeddings_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        print(f"✅ HuggingFace Embeddings initialized with model: {MODEL_NAME}")

        # 3. Initialize the LangChain VectorStore
        # Pass the matching embeddings_model to the vectorstore for query vectorization
        vectorstore = WeaviateVectorStore(
            client=client,
            index_name=COLLECTION_NAME,
            text_key="text", # Text property name in your schema
            embedding=embeddings_model # Pass the embeddings model here
        )
        print("✅ LangChain WeaviateVectorStore initialized with embedding model.")
        return client, vectorstore
        
    except Exception as e:
        print(f"❌ Could not initialize clients: {e}")
        return None, None

def langchain_retrieval_search(vectorstore: WeaviateVectorStore, query: str, k: int = 3):
    """
    Performs a simple vector retrieval using LangChain's VectorStore.
    """
    print(f"\n--- LangChain Vector Retrieval Search for: '{query}' ---")
    
    try:
        # Create a retriever from the vectorstore
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        
        # Retrieve relevant documents
        # The retriever uses the 'embeddings_model' initialized above to embed 'query'
        docs = retriever.invoke(query)

        if not docs:
            print("No documents found for this query.")
            return

        for i, doc in enumerate(docs):
            # doc is a LangChain Document object
            print(f"\n[{i+1}] Source Path: {doc.metadata.get('source', 'N/A')}")
            # The .page_content is the chunked text itself
            print(f"  Snippet: {doc.page_content[:500]}...")
            
    except Exception as e:
        # This will catch runtime errors like a missing collection or connection issues
        print(f"Error during LangChain retrieval search: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    client, vectorstore = initialize_client()
    
    if client and vectorstore:
        
        # Running the original retrieval query with the corrected setup:
        langchain_retrieval_search(
            vectorstore=vectorstore, 
            query="the latest trends and challenges in semiconductor manufacturing processes",
            k=3
        )

        # Example 2: Another Retrieval Query
        langchain_retrieval_search(
            vectorstore=vectorstore, 
            query="What new partnerships or acquisitions has Nvidia made recently?",
            k=5
        )
        
        # Close the raw Weaviate client connection
        client.close()
