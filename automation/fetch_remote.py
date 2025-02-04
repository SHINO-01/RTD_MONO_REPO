import os
import requests
from pathlib import Path

# Configuration
REMOTE_LIST = "automation/remotes.txt"
DEST_DIR = "projects"
GH_TOKEN = os.getenv("GH_PAT_TOKEN")

# Function to fetch the documentation
def fetch_docs():
    with open(REMOTE_LIST, "r") as file:
        lines = file.readlines()

    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        
        project, repo_url = line.strip().split(" ", 1)
        repo_owner, repo_name = repo_url.split("/")[-2:]

        # Construct the URL for the documentation
        docs_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/docs?ref=main"

        # Request documentation content from GitHub
        headers = {"Authorization": f"token {GH_TOKEN}"}
        response = requests.get(docs_url, headers=headers)
        
        if response.status_code == 200:
            docs = response.json()
            target_dir = Path(DEST_DIR) / project / "versions" / "latest"
            target_dir.mkdir(parents=True, exist_ok=True)

            for file in docs:
                if file["name"].endswith(".md"):
                    file_content = requests.get(file["download_url"]).text
                    with open(target_dir / file["name"], "w") as f:
                        f.write(file_content)
            print(f"Docs fetched for {project}")
        else:
            print(f"Failed to fetch docs for {project}: {response.status_code}")

if __name__ == "__main__":
    fetch_docs()
