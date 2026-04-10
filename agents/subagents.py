from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.tools_RAG import rag_query, rag_ingest_documents
from tools.tools_stock import check_inventary, update_inventary, add_item
from src.system_prompt import system_prompt_agent_culinary, system_prompt_agent_stock


model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")


tools_agent_culinary = [
    rag_query,
    rag_ingest_documents,
]

tools_agent_stock = [
    check_inventary,
    update_inventary,
    add_item,
]


agent_culinary = create_agent(
    model=model,
    tools=tools_agent_culinary,
    system_prompt=system_prompt_agent_culinary,
)
    

agent_stock = create_agent(
    model=model,
    tools=tools_agent_stock,
    system_prompt=system_prompt_agent_stock
)


@tool
def culinary_subagent_tool(query: str) -> str:
    """Encaminha perguntas sobre receitas para o especialista."""
    result = agent_culinary.invoke({"messages": [("user", query)]}) 
    return result["messages"][-1].content

@tool
def stock_subagent_tool(query: str) -> str:
    """Subagent especializado em gerenciamento de estoque."""
    result = agent_stock.invoke({"messages": [("user", query)]})
    return result["messages"][-1].content