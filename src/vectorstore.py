import os
import shutil

from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import RAG_FILES_DIR, VECTOR_STORE_PATH

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
    docs = load_documents()
    if docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        splits = text_splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(
            documents=splits, 
            embedding=embedding,
        )
        
        vectorstore.save_local(VECTOR_STORE_PATH)
        return vectorstore
        
    if os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss")):
        return FAISS.load_local(
            VECTOR_STORE_PATH, 
            embedding, 
            allow_dangerous_deserialization=True
        )
        
    return None