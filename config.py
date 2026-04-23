import os
from dotenv import load_dotenv
load_dotenv()

MODEL = os.getenv('MODEL')
VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH')
RAG_FILES_DIR = os.getenv('RAG_FILES_DIR')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')