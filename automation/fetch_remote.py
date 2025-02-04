import os
import requests
from pathlib import Path
import sys

# Constants
PROJECTS_DIR = "docs/projects"
GH_TOKEN = os.getenv("GH_PAT_TOKEN")  # GitHub authentication token

def fetch_docs(repo_name):
    """
    Fetches the latest documentation from a given GitHub repository.

    Args:
        repo_name (str): Name of the repository that triggered the webhook.
    """
    if not GH_TOKEN:
        print("Error: GitHub token is missing. Set GH_PAT_TOKEN as an environment variable.")
        sys.exit(1)

    repo_owner = "YOUR_ORG"  # Change to your GitHub organization name
    docs_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/docs?ref=main"

    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    response = requests.get(docs_url, headers=headers)

    if response.status_code == 200:
        docs = response.json()
        latest_version = "latest"  # Store docs under the 'latest' folder
        target_dir = Path(PROJECTS_DIR) / repo_name / latest_version / "docs"
        target_dir.mkdir(parents=True, exist_ok=True)

        for file in docs:
            if file["type"] == "file" and file["name"].endswith(".md"):
                file_content = requests.get(file["download_url"], headers=headers).text
                with open(target_dir / file["name"], "w", encoding="utf-8") as f:
                    f.write(file_content)
        
        print(f"✅ Docs fetched for {repo_name}")
    else:
        print(f"❌ Failed to fetch docs for {repo_name}. Status Code: {response.status_code}, Message: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No repository name provided. This script must be called with the repository name.")
        sys.exit(1)

    repo_name = sys.argv[1]
    fetch_docs(repo_name)
