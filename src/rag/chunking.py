# src/rag/chunking.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion.resume_loader import get_resume_text

def chunk_resume(docs, chunk_size=500, chunk_overlap=50):
    full_text = get_resume_text(docs)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(full_text)

def chunk_all_projects(project_list, chunk_size=500, chunk_overlap=50):
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    for proj in project_list:
        text = f"""
Project Name: {proj['name']}
URL: {proj['url']}
Description: {proj['description']}
Topics: {", ".join(proj['topics'])}

README:
{proj['readme']}
"""
        chunks = splitter.split_text(text)
        for c in chunks:
            all_chunks.append({
                "text": c,
                "project_name": proj["name"],
                "url": proj["url"],
                "topics": proj["topics"],
            })

    return all_chunks
