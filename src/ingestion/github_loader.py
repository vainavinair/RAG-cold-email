# src/ingestion/github_loader.py
from github import Github
import base64
import os

def load_github_profile_repos(profile_url: str):
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)

    username = profile_url.rstrip("/").split("/")[-1]
    repos = g.get_user(username).get_repos()
    project_list = []

    for repo in repos:
        try:
            readme = repo.get_readme()
            readme_text = base64.b64decode(readme.content).decode("utf-8")
        except Exception:
            readme_text = ""

        project_info = {
            "name": repo.name,
            "description": repo.description or "",
            "topics": repo.get_topics() or [],
            "url": repo.html_url,
            "readme": readme_text,
        }
        project_list.append(project_info)

    return project_list
