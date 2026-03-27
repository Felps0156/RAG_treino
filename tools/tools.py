from langchain.tools import tool

from vectorstore import get_vectorstore

vectorstore = get_vectorstore()

@tool
def knowledge_base_search(query: str):
    """Busca informações técnicas nos documentos carregados."""
    
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])