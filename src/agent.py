from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from agents.subagents import stock_subagent_tool, culinary_subagent_tool, market_subagent_tool
from src.system_prompt import system_prompt_agent_chef

from config import MODEL

model = ChatGoogleGenerativeAI(model=MODEL)

subagents = [
    stock_subagent_tool,
    culinary_subagent_tool,
    market_subagent_tool
]

agent_chef = create_agent(
    model=model,
    tools=subagents,
    system_prompt=system_prompt_agent_chef
)