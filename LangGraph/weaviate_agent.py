from typing import TypedDict, Literal
from typing import List, Annotated, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.types import Send
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import operator
import json
from metric_handler import MetricsHandler

import time
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

import time
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
# from raptor.raptor import RetrievalAugmentation, RetrievalAugmentationConfig
# from build_raptor_graph import OllamaSummarizationModel, HFEmbeddingModel, OllamaQAModel

# --- CONFIGURATION ---
# Ensure you have pulled this model in Ollama: `ollama pull llama3`
LLM_MODEL = "gemma3" 
OLLAMA_BASE_URL = "http://ollama:11434" # Hostname 'ollama' comes from docker-compose
WEAVIATE_URL = "http://weaviate:8080"
MODEL_NAME = "all-MiniLM-L6-v2"

metrics_handler = MetricsHandler()
# Initialize Local LLM
llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.01,
    callbacks=[metrics_handler]
)



# classList = ["RaptorNvidiaArticles", "RaptorNvidiaPublications", "RaptorNvidiaTranscripts", "RaptorNvidiaInfo"]

# RAArticles = RetrievalAugmentation(tree="RaptorNvidiaArticles", config=custom_config)
# RAPublication = RetrievalAugmentation(tree="RaptorNvidiaPublications", config=custom_config)
# RATranscripts = RetrievalAugmentation(tree="RaptorNvidiaTranscripts", config=custom_config)
# RANvidiaInfo = RetrievalAugmentation(tree="RaptorNvidiaInfo", config=custom_config)



def reduce_documents(existing: List[Document], new: List[Document]) -> List[Document]:
    # 1. Combine existing and new documents
    all_docs = existing + new
    
    # 2. Deduplicate based on page_content
    # Using a dictionary key ensures uniqueness because keys must be unique
    unique_map = {doc.page_content: doc for doc in all_docs}
    
    # 3. Return the unique values as a list
    return list(unique_map.values())

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    question: str
    category: str
    context: Annotated[List[Document], reduce_documents]
    answer: str
    sufficient: bool
    original_question: str
    sub_questions: List[str]

class SubQueries(BaseModel):
    """A list of sub-questions derived from a complex user question."""
    sub_questions: List[str] = Field(
        ...,
        description="A list of distinct, independent sub-questions that need to be answered to fully resolve the user's original, complex question."
    )

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
        index_name="ChunkedNvidiaTranscripts",
        text_key="text", # Text property name in your schema
        embedding=embeddings_model # Pass the embeddings model here
    )
    transcript_retriever = transcript_vectorstore.as_retriever(search_kwargs={"k": 5})

    publications_vectorstore = WeaviateVectorStore(
        client=client,
        index_name="ChunkedNvidiaPublications",
        text_key="text", # Text property name in your schema
        embedding=embeddings_model # Pass the embeddings model here
    )
    publications_retriever = publications_vectorstore.as_retriever(search_kwargs={"k": 5})
    articles_vectorstore = WeaviateVectorStore(
        client=client,
        index_name="ChunkedNvidiaArticles",
        text_key="text", # Text property name in your schema
        embedding=embeddings_model # Pass the embeddings model here
    )
    articles_retriever = articles_vectorstore.as_retriever(search_kwargs={"k": 5})
    print("✅ LangChain WeaviateVectorStore initialized with embedding model.")

    info_vectorstore = WeaviateVectorStore(
        client=client,
        index_name="NvidiaInfo",
        text_key="text", # Text property name in your schema
        embedding=embeddings_model # Pass the embeddings model here
    )
    info_retriever = info_vectorstore.as_retriever(search_kwargs={"k": 5})
    print("✅ LangChain WeaviateVectorStore initialized with embedding model.")
    
except Exception as e:
    print(f"❌ Could not initialize clients: {e}")

# --- RETRIEVERS (MOCK) ---
def retrieve_transcripts(state: AgentState):
    print("--RETRIEVE TRANSCRIPTS--")
    query = state["question"]
    docs = transcript_retriever.invoke(query)
    return {"context": docs}

def retrieve_newsletters(state: AgentState):
    print("--RETRIEVE NEWSLETTERS--")
    query = state["question"]
    docs = articles_retriever.invoke(query)
    return {"context": docs}

def retrieve_papers(state: AgentState):
    print("--RETRIEVE PAPERS--")
    query = state["question"]
    docs = publications_retriever.invoke(query)
    return {"context": docs}

def retrieve_info(state: AgentState):
    print("--RETRIEVE INFO--")
    query = state["question"]
    docs = info_retriever.invoke(query)
    return {"context": docs}

# --- DECOMPOSER LOGIC (FAN-OUT) ---
def decompose_query(state: AgentState):
    """Uses LLM to break a complex question into multiple sub-questions."""
    print(f"---DECOMPOSING QUERY: {state['question']}---")

    structured_llm = llm.with_structured_output(SubQueries, method="json_schema")
    
    system_prompt = """You are a Query Decomposer. Your task is to analyze a complex user question 
    and break it down into 4 distinct, simple, and independent sub-questions. 
    Each sub-question should be answerable on its own. Please be specific and ensure that you keep the keywords in each query. 
    Return a JSON object containing a list of these sub-questions.

    If the question is simple then just return a JSON object containing a list of the original question.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    decomposer_chain = prompt | structured_llm
    result = decomposer_chain.invoke({"question": state["question"]})

    # Ensure result is a list of strings, fall back if LLM fails
    sub_questions = result.sub_questions if result and result.sub_questions else [state['question']]
    print(("\n").join(sub_questions))
    print(f"---GENERATED {len(sub_questions)} SUB-QUERIES---")

    return {"sub_questions": sub_questions, "original_question": state["question"]}

def distribute_queries(state: AgentState):
    """
    Decide routing HERE instead of in a separate node. 
    This prevents 'category' state collisions.
    """
    sub_qs = state.get("sub_questions", [])
    print(f"---ROUTING {len(sub_qs)} SUB-TASKS---")
    
    structured_llm = llm.with_structured_output(RouteQuery, method="json_schema")
    router_prompt = ChatPromptTemplate.from_messages([
        ("system", "Route to: 'transcripts', 'newsletters', or 'papers'."),
        ("human", "{question}")
    ])
    router_chain = router_prompt | structured_llm

    sends = []
    for q in sub_qs:
        # Run router for this specific sub-question
        try:
            res = router_chain.invoke({"question": q})
            source = res.datasource
        except:
            source = "newsletters" # Fallback

        target_node = f"retrieve_{source}"
        
        # Create the Send object
        # Note: We pass 'question' so the retriever knows what to search for
        sends.append(Send(target_node, {"question": q}))
        
    return sends

def rerank(docs):
    return docs[0].content
# --- GENERATOR ---
def generate_answer(state: List[AgentState]):
    print("---GENERATING ANSWER---")
    prompt = ChatPromptTemplate.from_template(
        """You are a an expert on NVIDIA. 
        Answer the question in an authoritative manner using the provided context. 
        Only use context that will help answer the question.
        Only respond in english
        
        Context:
        {context}
        
        Question:
        {question}

        Response: 
        """
    )
    combined_results = ""
    for d in state["context"]:
        combined_results += f"\n {d.page_content}"
    chain = prompt | llm
    response = chain.invoke({"context": combined_results, "question": state["original_question"]})

    return {"answer": response.content, "context": state["context"]}

def generate_baseline_answer(state: List[AgentState]):
    print("---GENERATING ANSWER---")
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant. Answer the question based ONLY on the provided context.
        
        Context:
        {context}
        
        Question:
        {question}
        """
    )
    combined_results = ""
    for d in state["context"]:
        combined_results += f"\n {d.page_content}"
    chain = prompt | llm
    response = chain.invoke({"context": combined_results, "question": state["question"]})

    return {"answer": response.content, "context": state["context"]}

def get_next_node(state: AgentState):
    category = state["category"]
    if category == "transcripts": return "retrieve_transcripts"
    elif category == "papers": return "retrieve_papers"
    else: return "retrieve_newsletters"

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
    update = {"sufficient": result.sufficient}
    if not result.sufficient:
        update["original_question"] = f"Improve and expand this answer: {state['answer']}"
    return update

def agent_next_step(state: AgentState):
    return "end" if state.get("sufficient") else "generate"

agent_workflow = StateGraph(AgentState)

agent_workflow.add_node("decompose_query", decompose_query)
agent_workflow.add_node("router", route_question)
agent_workflow.add_node("retrieve_transcripts", retrieve_transcripts)
agent_workflow.add_node("retrieve_newsletters", retrieve_newsletters)
agent_workflow.add_node("retrieve_papers", retrieve_papers)
agent_workflow.add_node("generate", generate_answer)
agent_workflow.add_node("assess", assess_answer)

agent_workflow.set_entry_point("decompose_query")

agent_workflow.add_conditional_edges("decompose_query", distribute_queries)

agent_workflow.add_edge("retrieve_transcripts", "generate")
agent_workflow.add_edge("retrieve_newsletters", "generate")
agent_workflow.add_edge("retrieve_papers", "generate")
agent_workflow.add_edge("generate", "assess")

agent_workflow.add_conditional_edges(
    "assess",
    agent_next_step,
    {"generate": "generate", "end": END}
)

agent = agent_workflow.compile()

base_line_workflow = StateGraph(AgentState)

base_line_workflow.add_node("retrieve_info", retrieve_info)
base_line_workflow.add_node("generate", generate_baseline_answer)

base_line_workflow.set_entry_point("retrieve_info")
base_line_workflow.add_edge("retrieve_info", "generate")


baseline = base_line_workflow.compile()




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
    return "end" if state.get("sufficient") else "decompose_query"

agent_workflow = StateGraph(AgentState)

agent_workflow.add_node("decompose_query", decompose_query)
agent_workflow.add_node("router", route_question)
agent_workflow.add_node("retrieve_transcripts", retrieve_transcripts)
agent_workflow.add_node("retrieve_newsletters", retrieve_newsletters)
agent_workflow.add_node("retrieve_papers", retrieve_papers)
agent_workflow.add_node("generate", generate_answer)
agent_workflow.add_node("assess", assess_answer)

agent_workflow.set_entry_point("decompose_query")

agent_workflow.add_conditional_edges("decompose_query", distribute_queries)

agent_workflow.add_edge("retrieve_transcripts", "generate")
agent_workflow.add_edge("retrieve_newsletters", "generate")
agent_workflow.add_edge("retrieve_papers", "generate")
agent_workflow.add_edge("generate", "assess")

agent_workflow.add_conditional_edges(
    "assess",
    agent_next_step,
    {"generate": "generate", "end": END}
)

agent = agent_workflow.compile()

def main():
    # Example 1
    inputs = {"question": "How does NVIDIA reduce latency in ray tracing?"}

    start_time = time.perf_counter()

    result = agent.invoke(inputs)

    end_time = time.perf_counter() 
    total_time = end_time - start_time

    print(f"\nFINAL ANSWER:\n{result['answer']}")
    metrics_handler.report()
    print(f"Total Workflow Duration (Wall Clock): {total_time:.2f}s")

    results = []
    with open('complex_retrieval_requests.json', 'r') as f:
        data_dict = json.load(f)

        reqs = data_dict["requests"]
        for r in reqs:
            inputs = {"question": r["request"]}
            start_time = time.perf_counter()

            result = agent.invoke(inputs)

            end_time = time.perf_counter() 
            total_time = end_time - start_time

            serialized_context = []
            if "context" in result:
                serialized_context = [
                    {
                        "content": doc.page_content, 
                        "metadata": doc.metadata
                    } 
                    for doc in result['context']
                ]
            request_metrics = {}
            request_metrics["response"] = result['answer']
            request_metrics["context"] = serialized_context
            request_metrics["total_time"] = total_time
            request_metrics["successful_requests"] = metrics_handler.successful_requests
            request_metrics["total_latency"] = metrics_handler.total_latency
            request_metrics["total_input_tokens"] = metrics_handler.total_input_tokens
            request_metrics["total_output_tokens"] = metrics_handler.total_output_tokens

            metrics_handler.successful_requests = 0
            metrics_handler.total_latency = 0
            metrics_handler.total_input_tokens = 0
            metrics_handler.total_output_tokens = 0
            results.append(request_metrics)
    

    with open('./data/chunked_result.json', 'w') as fp:
        json.dump({"results": results}, fp)
    results = []
    with open('complex_retrieval_requests.json', 'r') as f:
        data_dict = json.load(f)

        reqs = data_dict["requests"]
        for r in reqs:
            inputs = {"question": r["request"]}
            start_time = time.perf_counter()

            result = baseline.invoke(inputs)

            end_time = time.perf_counter() 
            total_time = end_time - start_time

            serialized_context = []
            if "context" in result:
                serialized_context = [
                    {
                        "content": doc.page_content, 
                        "metadata": doc.metadata
                    } 
                    for doc in result['context']
                ]
            request_metrics = {}
            request_metrics["response"] = result['answer']
            request_metrics["context"] = serialized_context
            request_metrics["total_time"] = total_time
            request_metrics["successful_requests"] = metrics_handler.successful_requests
            request_metrics["total_latency"] = metrics_handler.total_latency
            request_metrics["total_input_tokens"] = metrics_handler.total_input_tokens
            request_metrics["total_output_tokens"] = metrics_handler.total_output_tokens

            metrics_handler.successful_requests = 0
            metrics_handler.total_latency = 0
            metrics_handler.total_input_tokens = 0
            metrics_handler.total_output_tokens = 0

            results.append(request_metrics)

    

    with open('./data/chunked_baseline_result.json', 'w') as fp:
        json.dump({"results": results}, fp)

# --- EXECUTION ---
if __name__ == "__main__":
    main()


    

