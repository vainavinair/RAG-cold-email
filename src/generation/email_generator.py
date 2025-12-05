# src/generation/email_generator.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_context(resume_chunks, github_chunks_with_meta):
    # plain text from resume
    resume_section = "\n\n".join(resume_chunks)

    # format github project chunks with metadata
    github_sections = []
    for item in github_chunks_with_meta:
        github_sections.append(
            f"Project: {item['project_name']}\n"
            f"URL: {item['url']}\n"
            f"Topics: {', '.join(item['topics'])}\n"
            f"Snippet: {item['text']}"
        )

    github_section = "\n\n".join(github_sections)

    return f"""[RESUME CONTEXT]
{resume_section}

[GITHUB PROJECT CONTEXT]
{github_section}
"""

def generate_email_rag(resume_chunks, github_chunks_with_meta, job_row):
    context = build_context(resume_chunks, github_chunks_with_meta)

    prompt = f"""
You are helping me write a personalised internship/job cold email.

Use ONLY the information in the context below to talk about my skills and projects.

CONTEXT:
{context}

JOB DESCRIPTION:
{job_row['job_description']}

Write a short cold email (<120 words) applying for this role: {job_row['job_title']}.

The email must:
- Mention 1–2 specific projects by name (and refer to them naturally, not as a list)
- Optionally mention GitHub if relevant (but not as a raw URL dump)
- Highlight skills that are clearly supported by the context
- Be 5–6 sentences, confident and professional
- End with a clear call to action (e.g., asking for a short call or opportunity to discuss fit)
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
