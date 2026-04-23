from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.tools_RAG import rag_query, rag_ingest_documents
from tools.tools_stock import check_inventary, update_inventary, add_item
from tools.tools_market import market_search, market_save_item, market_report, market_clear_list

from src.system_prompt import system_prompt_agent_culinary, system_prompt_agent_stock, system_prompt_agent_market

from config import MODEL



model = ChatGoogleGenerativeAI(model=MODEL)


tools_agent_culinary = [
    rag_query,
    rag_ingest_documents,
]

tools_agent_stock = [
    check_inventary,
    update_inventary,
    add_item,
]

tools_agent_market = [
    market_search,
    market_save_item,
    market_report,
    market_clear_list,    
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

agent_market = create_agent(
    model=model,
    tools=tools_agent_market,
    system_prompt=system_prompt_agent_market
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

@tool
def market_subagent_tool(query: str) -> str:
    """Subagent especializado no gerenciamento da lista de compras"""
    result = agent_stock.invoke({"messages": [("user", query)]})
    return result["messages"][-1].content
