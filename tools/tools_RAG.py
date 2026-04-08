from langchain.tools import tool

from vectorstore import get_vectorstore, ingest_documents

@tool
def rag_query(query: str) -> str:
    """
    CONSULTE ESTA FERRAMENTA SEMPRE que o usuário fizer perguntas técnicas, 
    sobre procedimentos internos ou dúvidas que dependam de conhecimento específico. 
    Use esta ferramenta antes de responder para garantir que a informação é verídica.
    """
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=2)

    if not vectorstore:
        return "Nenhum documento foi indexado na base RAG."


    return "\n\n".join([f"Fonte: {d.metadata.get('source')}\nConteúdo: {d.page_content}" for d in docs])


@tool
def rag_ingest_documents(query: str = ""):
    """
    USE ESTA FERRAMENTA APENAS para incluir novos documentos na base.
    """
    return ingest_documents()