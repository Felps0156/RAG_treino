import os
from dotenv import load_dotenv
load_dotenv()

VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH')
RAG_FILES_DIR = os.getenv('RAG_FILES_DIR')