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
    
    files = [
        os.path.join(RAG_FILES_DIR, f)
        for f in os.listdir(RAG_FILES_DIR)
        if f.endswith(".pdf") or f.endswith(".txt") or f.endswith(".md")
    ]
    
    for file in files:
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file)
        elif file.endswith(".txt"):
            loader = TextLoader(file)
        else:
            loader = UnstructuredMarkdownLoader(file)
            
        docs.extend(loader.load())
        dest_path = os.path.join(processed_dir, os.path.basename(file))
        shutil.move(file, dest_path)
        
    return docs

embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
)

def get_vectorstore():
    vectorstore = SupabaseVectorStore(
        client=supabase,
        embedding=embedding,
        table_name="documents",
        query_name="match_documents",
    )
    
    # 2. Verifica se há arquivos novos para processar
    docs = load_documents()
    
    if docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        splits = text_splitter.split_documents(docs)
        
        # 3. Adiciona os novos documentos diretamente na nuvem
        # O LangChain enviará os textos e os embeddings gerados pelo Gemini
        vectorstore.add_documents(splits)
        
    return vectorstore