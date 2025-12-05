# main.py
import os
from dotenv import load_dotenv
load_dotenv()

from src.ingestion.resume_loader import load_resume, get_resume_text
from src.ingestion.jobs_loader import load_jobs
from src.ingestion.github_loader import load_github_profile_repos

from src.rag.chunking import chunk_resume, chunk_all_projects
from src.rag.retrieval import (
    rank_jobs_for_resume,
    embed_chunks,
    embed_project_chunks,
    retrieve_resume_chunks,
    retrieve_github_chunks,
)

from src.generation.email_generator import generate_email_rag
from src.utils.mailer import send_email

def main():
    # 1. Load data
    resume_docs = load_resume("data/resume.pdf")
    resume_text = get_resume_text(resume_docs)
    jobs = load_jobs("data/jobs.csv")
    projects = load_github_profile_repos("https://github.com/vainavinair")

    # 2. Chunk
    resume_chunks = chunk_resume(resume_docs)
    project_chunks = chunk_all_projects(projects)

    # 3. Embed
    resume_embs = embed_chunks(resume_chunks)
    project_embs = embed_project_chunks(project_chunks)

    # 4. Rank jobs
    jobs_ranked = rank_jobs_for_resume(jobs, resume_text)
    top_job = jobs_ranked.iloc[0]
    job_description = top_job["job_description"]

    # 5. Retrieve context
    relevant_resume_chunks = retrieve_resume_chunks(job_description, resume_chunks, resume_embs)
    relevant_github_chunks = retrieve_github_chunks(job_description, project_chunks, project_embs, k=4)

    # 6. Generate email (combined RAG)
    email_content = generate_email_rag(relevant_resume_chunks, relevant_github_chunks, top_job)
    print("\n=== Generated Email ===\n")
    print(email_content)

    # 7. Optionally send
    ans = input("\nSend this email to TEST_EMAIL? (y/n): ")
    if ans.lower() == "y":
        to = os.getenv("TEST_EMAIL")
        send_email(
            to=to,
            subject=f"Application for {top_job['job_title']}",
            body=email_content,
            attachment="data/resume.pdf",
        )
        print("Email sent!")

if __name__ == "__main__":
    main()
