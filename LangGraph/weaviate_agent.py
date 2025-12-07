from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

import os
import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout
from weaviate.classes.query import MetadataQuery
import getpass
import os
# LangChain Imports
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.documents import Document
# Corrected Import to match ingestion script
from langchain_community.embeddings import HuggingFaceEmbeddings 

# --- CONFIGURATION ---
# Ensure you have pulled this model in Ollama: `ollama pull llama3`
LLM_MODEL = "gemma3" 
OLLAMA_BASE_URL = "http://ollama:11434" # Hostname 'ollama' comes from docker-compose
WEAVIATE_URL = "http://weaviate:8080"
MODEL_NAME = "all-MiniLM-L6-v2"

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

# Initialize Local LLM
llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    question: str
    category: str
    context: str
    answer: str
    sufficient: bool

# --- ROUTER LOGIC ---
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["transcripts", "newsletters", "papers"] = Field(
        ...,
        description="Given a user question, choose which datasource would be most relevant."
    )

def route_question(state: AgentState):
    print(f"---ROUTING QUESTION: {state['question']}---")
    
    # "json_schema" method is often more reliable for local models than tool calling
    structured_llm = llm.with_structured_output(RouteQuery, method="json_schema")
    
    system_prompt = """You are an expert at routing NVIDIA-related questions.
    Return a JSON object with a single key 'datasource'.
    - 'transcripts': Use for questions about speeches, keynotes, or earnings calls.
    - 'newsletters': Use for questions about general updates, summaries, or marketing.
    - 'papers': Use for technical questions about deep learning, research, or algorithms.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    router = prompt | structured_llm
    result = router.invoke({"question": state["question"]})
    
    # Fallback if model fails to adhere strictly (common with smaller local models)
    chosen_source = result.datasource if result else "newsletters"
    print(f"---ROUTED TO: {chosen_source}---")
    return {"category": chosen_source}


try:
    # 1. Initialize the raw Weaviate client
    # client = weaviate.connect_to_local(host="weaviate", port=8080, grpc_port=50051)
    client = weaviate.connect_to_local(host="weaviate", port=8080, grpc_port=50051,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
    ))  
    if not client.is_ready():
        print("❌ Weaviate client is not ready. Check your Docker container.")
        
    print(f"✅ Raw Weaviate client connected successfully at {WEAVIATE_URL}")

    # 2. Initialize the Embedding Model (MUST match ingestion model)
    embeddings_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    print(f"✅ HuggingFace Embeddings initialized with model: {MODEL_NAME}")

    # 3. Initialize the LangChain VectorStore
    # Pass the matching embeddings_model to the vectorstore for query vectorization
    transcript_vectorstore = WeaviateVectorStore(
        client=client,
        index_name="NvidiaTranscripts",
        text_key="text", # Text property name in your schema
        embedding=embeddings_model # Pass the embeddings model here
    )
    transcript_retriever = transcript_vectorstore.as_retriever(search_kwargs={"k": 5})

    publications_vectorstore = WeaviateVectorStore(
        client=client,
        index_name="NvidiaPublications",
        text_key="text", # Text property name in your schema
        embedding=embeddings_model # Pass the embeddings model here
    )
    publications_retriever = publications_vectorstore.as_retriever(search_kwargs={"k": 5})
    articles_vectorstore = WeaviateVectorStore(
        client=client,
        index_name="NvidiaArticles",
        text_key="text", # Text property name in your schema
        embedding=embeddings_model # Pass the embeddings model here
    )
    articles_retriever = articles_vectorstore.as_retriever(search_kwargs={"k": 5})
    print("✅ LangChain WeaviateVectorStore initialized with embedding model.")
    
except Exception as e:
    print(f"❌ Could not initialize clients: {e}")

# --- RETRIEVERS (MOCK) ---
def retrieve_transcripts(state: AgentState):
    print("--RETRIEVE TRANSCRIPTS--")
    query = state["question"]
    docs = transcript_retriever.invoke(query)
    print(docs[0])
    return {"context": docs}

def retrieve_newsletters(state: AgentState):
    print("--RETRIEVE NEWSLETTERS--")
    query = state["question"]
    docs = articles_retriever.invoke(query)
    print(docs[0])
    return {"context": docs}

def retrieve_papers(state: AgentState):
    print("--RETRIEVE PAPERS--")
    query = state["question"]
    docs = publications_retriever.invoke(query)
    print(docs[0])
    return {"context": docs}

def rerank(docs):
    return docs[0].content
# --- GENERATOR ---
def generate_answer(state: AgentState):
    print("---GENERATING ANSWER---")
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant. Answer the question based ONLY on the provided context.
        
        Context:
        {context}
        
        Question:
        {question}
        """
    )
    chain = prompt | llm
    response = chain.invoke({"context": state["context"], "question": state["question"]})
    print(response)
    return {"answer": response.content}

# --- GRAPH CONSTRUCTION ---
workflow = StateGraph(AgentState)

workflow.add_node("router", route_question)
workflow.add_node("retrieve_transcripts", retrieve_transcripts)
workflow.add_node("retrieve_newsletters", retrieve_newsletters)
workflow.add_node("retrieve_papers", retrieve_papers)
workflow.add_node("generate", generate_answer)

workflow.set_entry_point("router")

def get_next_node(state: AgentState):
    category = state["category"]
    if category == "transcripts": return "retrieve_transcripts"
    elif category == "papers": return "retrieve_papers"
    else: return "retrieve_newsletters"

workflow.add_conditional_edges(
    "router",
    get_next_node,
    {
        "retrieve_transcripts": "retrieve_transcripts",
        "retrieve_newsletters": "retrieve_newsletters",
        "retrieve_papers": "retrieve_papers"
    }
)

workflow.add_edge("retrieve_transcripts", "generate")
workflow.add_edge("retrieve_newsletters", "generate")
workflow.add_edge("retrieve_papers", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

# Agentic workflow

class AnswerCheck(BaseModel):
    sufficient: bool = Field(..., description="True if the answer sufficiently and clearly addresses the question.")

def assess_answer(state: AgentState):
    print("---ASSESS---")
    structured_llm = llm.with_structured_output(AnswerCheck, method="json_schema")

    system_prompt = """You check if an answer sufficiently and clearly addresses a user's question.
    Return a JSON object with a single key 'sufficient'.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Question:\n{question}\n\nAnswer:\n{answer}")
    ])

    checker = prompt | structured_llm
    result = checker.invoke({"question": state["question"], "answer": state["answer"]})
    print(result)
    update = {"sufficient": result.sufficient}
    if not result.sufficient:
        update["question"] = f"Improve and expand this answer: {state['answer']}"
    return update

def agent_next_step(state: AgentState):
    print("\n\n\n\n")
    print(state)
    return "end" if state.get("sufficient") else "router"

agent_workflow = StateGraph(AgentState)

agent_workflow.add_node("router", route_question)
agent_workflow.add_node("retrieve_transcripts", retrieve_transcripts)
agent_workflow.add_node("retrieve_newsletters", retrieve_newsletters)
agent_workflow.add_node("retrieve_papers", retrieve_papers)
agent_workflow.add_node("generate", generate_answer)
agent_workflow.add_node("assess", assess_answer)

agent_workflow.set_entry_point("router")

agent_workflow.add_conditional_edges(
    "router",
    get_next_node,
    {
        "retrieve_transcripts": "retrieve_transcripts",
        "retrieve_newsletters": "retrieve_newsletters",
        "retrieve_papers": "retrieve_papers",
    }
)

agent_workflow.add_edge("retrieve_transcripts", "generate")
agent_workflow.add_edge("retrieve_newsletters", "generate")
agent_workflow.add_edge("retrieve_papers", "generate")
agent_workflow.add_edge("generate", "assess")

agent_workflow.add_conditional_edges(
    "assess",
    agent_next_step,
    {"router": "router", "end": END}
)

agent = agent_workflow.compile()


# --- EXECUTION ---
if __name__ == "__main__":
    # Example 1
    inputs = {"question": "How does NVIDIA reduce latency in ray tracing?"}
    result = agent.invoke(inputs)
    print(f"\nFINAL ANSWER:\n{result['answer']}")

