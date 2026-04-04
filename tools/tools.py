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

    if not vectorstore:
        return "Nenhum documento foi indexado na base RAG."

    docs = vectorstore.similarity_search(query, k=2)

    return docs


@tool
def rag_ingest_documents():
    """
    USE ESTA FERRAMENTA APENAS quando o usuário solicitar explicitamente 
    a inclusão de novos documentos na base de conhecimento. 
    Não a utilize para buscar informações, apenas para indexar novos arquivos.
    """
    
    result = ingest_documents()
    return result
    
    
    
    