import os
import requests
from pathlib import Path
import sys

# Constants
PROJECTS_DIR = "docs/projects"
GH_TOKEN = os.getenv("GH_PAT_TOKEN")

def fetch_docs(repo_name, repo_owner="SHINO-01"):
    """
    Recursively fetches all documentation files from a given GitHub repository.
    """
    if not GH_TOKEN:
        print("❌ Error: GitHub token is missing. Set GH_PAT_TOKEN as an environment variable.")
        sys.exit(1)

    # Get default branch dynamically
    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    default_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    default_branch_res = requests.get(default_branch_url, headers=headers).json()
    default_branch = default_branch_res.get("default_branch", "main")  # Default to main

    print(f"📥 Fetching docs for {repo_name} from branch {default_branch}...")

    def fetch_and_save_files(path="docs", local_dir=None):
        """
        Recursively fetches files from the GitHub API and saves them locally.
        """
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}?ref={default_branch}"
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch docs from {api_url}. Status Code: {response.status_code}, Message: {response.text}")
            return

        files = response.json()
        for file in files:
            file_path = Path(file["path"].replace("docs/", ""))  # Keep relative path after `docs/`
            local_file_path = Path(local_dir) / file_path

            if file["type"] == "dir":
                # Recursively fetch subdirectory contents
                fetch_and_save_files(file["path"], local_dir)
            elif file["type"] == "file" and file["name"].endswith(".md"):
                # Download Markdown file
                file_content = requests.get(file["download_url"], headers=headers).text
                local_file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
                with open(local_file_path, "w", encoding="utf-8") as f:
                    f.write(file_content)

    # Define where the documentation will be stored in the mother repo
    latest_version = "latest"
    target_dir = Path(PROJECTS_DIR) / repo_name / latest_version / "docs"
    target_dir.mkdir(parents=True, exist_ok=True)

    # Start fetching files recursively
    fetch_and_save_files("docs", target_dir)

    print(f"✅ Successfully fetched docs for {repo_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: No repository name provided. This script must be called with the repository name.")
        sys.exit(1)

    repo_name = sys.argv[1]
    fetch_docs(repo_name)
