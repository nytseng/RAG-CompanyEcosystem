from typing import TypedDict, Literal
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

# --- CONFIGURATION ---
# Ensure you have pulled this model in Ollama: `ollama pull llama3`
LLM_MODEL = "gemma3" 
OLLAMA_BASE_URL = "http://ollama:11434" # Hostname 'ollama' comes from docker-compose

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

# --- RETRIEVERS (MOCK) ---
def retrieve_transcripts(state: AgentState):
    print("---RETRIEVING FROM TRANSCRIPTS---")
    return {"context": "Jensen Huang GTC Keynote: 'Blackwell is the engine of the new industrial revolution.'"}

def retrieve_newsletters(state: AgentState):
    print("---RETRIEVING FROM NEWSLETTERS---")
    return {"context": "NVIDIA Weekly: Announced new partnerships with healthcare providers for AI diagnostics."}

def retrieve_papers(state: AgentState):
    print("---RETRIEVING FROM PAPERS---")
    return {"context": "Abstract: We present a novel method for reducing latency in ray tracing using AI denoisers."}

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
        update["question"] = f"Improve and expand this answer: {state['answer']}"
    return update

def agent_next_step(state: AgentState):
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
    result = app.invoke(inputs)
    print(f"\nFINAL ANSWER:\n{result['answer']}")