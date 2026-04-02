from langchain.tools import tool

from vectorstore import get_vectorstore

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

    if not docs:
        return "Nenhum documento relevante foi encontrado."

    resultados = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Fonte desconhecida")
        page = doc.metadata.get("page", "Página desconhecida")
        content = doc.page_content.strip()

        resultados.append(
            f"Resultado {i}\n"
            f"Fonte: {source}\n"
            f"Página: {page}\n"
            f"Conteúdo: {content}\n"
        )

    return "\n---\n".join(resultados)