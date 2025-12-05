# src/rag/retrieval.py
import numpy as np
from sentence_transformers.util import cos_sim
from src.utils.model import get_embedder

embedder = get_embedder()

def rank_jobs_for_resume(jobs_df, resume_text):
    resume_emb = embedder.encode(resume_text, convert_to_tensor=True)
    job_embs = embedder.encode(
        jobs_df["job_description"].tolist(),
        convert_to_tensor=True
    )
    cos_scores = cos_sim(resume_emb, job_embs)[0]
    scores = cos_scores.cpu().numpy()

    ranked = jobs_df.copy()
    ranked["similarity_score"] = scores
    return ranked.sort_values("similarity_score", ascending=False).reset_index(drop=True)

def embed_chunks(chunks):
    return embedder.encode(chunks, convert_to_tensor=True)

def embed_project_chunks(project_chunks):
    return embedder.encode(
        [c["text"] for c in project_chunks],
        convert_to_tensor=True
    )

def retrieve_resume_chunks(job_description, resume_chunks, resume_embeddings, threshold=0.2):
    job_emb = embedder.encode(job_description, convert_to_tensor=True)
    scores = cos_sim(job_emb, resume_embeddings)[0].cpu().numpy()
    return [chunk for score, chunk in zip(scores, resume_chunks) if score >= threshold]

def retrieve_github_chunks(job_description, project_chunks, project_embeddings, k=4):
    job_emb = embedder.encode(job_description, convert_to_tensor=True)
    scores = cos_sim(job_emb, project_embeddings)[0].cpu().numpy()

    scored = []
    for score, chunk in zip(scores, project_chunks):
        scored.append({
            "score": float(score),
            "text": chunk["text"],
            "project_name": chunk["project_name"],
            "url": chunk["url"],
            "topics": chunk["topics"],
        })

    scored = sorted(scored, key=lambda x: x["score"], reverse=True)[:k]
    return scored
