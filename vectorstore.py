import os
import shutil

from supabase.client import Client, create_client
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import RAG_FILES_DIR, SUPABASE_SERVICE_KEY, SUPABASE_URL


supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
)


def load_documents():
    docs = []
    processed_dir = os.path.join(RAG_FILES_DIR, 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    # Lista arquivos PDF, TXT e MD
    files = [
        os.path.join(RAG_FILES_DIR, f)
        for f in os.listdir(RAG_FILES_DIR)
        if f.endswith((".pdf", ".txt", ".md"))
    ]
    
    for file in files:
        try:
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file)
            elif file.endswith(".txt"):
                loader = TextLoader(file)
            else:
                loader = UnstructuredMarkdownLoader(file)
                
            docs.extend(loader.load())
            
            # Move para a pasta 'processed' após carregar com sucesso
            dest_path = os.path.join(processed_dir, os.path.basename(file))
            shutil.move(file, dest_path)
        except Exception as e:
            print(f"Erro ao processar {file}: {e}")
        
    return docs

def get_vectorstore():
    # Inicializa o store (isso não depende de ter documentos novos)
    return SupabaseVectorStore(
        client=supabase,
        embedding=embedding,
        table_name="documents",
        query_name="match_documents",
    )
    
    
def ingest_documents():
    vectorstore = get_vectorstore()
    # Busca novos documentos
    new_docs = load_documents()
    
    # Só processa o split se a lista não estiver vazia
    if new_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=200,
        )
        splits = text_splitter.split_documents(new_docs)
        vectorstore.add_documents(splits)
    else:
        print("Documento processado")
        
    return vectorstore