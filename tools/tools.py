from langchain.tools import tool

from src.vectorstore import get_vectorstore

@tool
def rag_quary(query: str):
    """
    CONSULTE ESTA FERRAMENTA SEMPRE que o usuário fizer perguntas técnicas, 
    sobre procedimentos internos ou dúvidas que dependam de conhecimento específico. 
    Use esta ferramenta antes de responder para garantir que a informação é verídica.
    """
    vs = get_vectorstore() # Busca a instância atual
    if vs is None:
        return "A base de conhecimento está vazia no momento."
    
    docs = vs.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])