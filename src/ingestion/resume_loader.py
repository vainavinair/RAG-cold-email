# src/ingestion/resume_loader.py
import os
from langchain_community.document_loaders import PyPDFLoader

def load_resume(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    loader = PyPDFLoader(file_path)
    return loader.load() 

def get_resume_text(docs):
    return "\n".join(d.page_content for d in docs)
