from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.tools import rag_query


model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")


tools = [
    rag_query,
]

system_prompt = """
Você é um agente de culinária.
Você tem acesso a ferramenta de busca na base de dados.
Você deve usar essa ferramenta para buscar informações. Caso nenhum dado seja encontrado,
responda que não encontrou informações.
"""

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
)