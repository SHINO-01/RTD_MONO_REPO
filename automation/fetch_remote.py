import os
import requests
from pathlib import Path
import sys

# Constants
PROJECTS_DIR = "docs/projects"
GH_TOKEN = os.getenv("GH_PAT_TOKEN")

def fetch_docs(full_repo_name):
    """
    Fetches documentation files from the specified GitHub repository.
    Expects full_repo_name to be in the format "ORG/REPO".
    Files from the child repo's `docs/` folder are downloaded recursively.
    """
    if not GH_TOKEN:
        print("❌ Error: GitHub token is missing. Set GH_PAT_TOKEN as an environment variable.")
        sys.exit(1)

    # Split the full repo name
    parts = full_repo_name.split("/")
    if len(parts) != 2:
        print("❌ Error: Repository name must be in the format 'ORG/REPO'.")
        sys.exit(1)
    repo_owner, repo_name = parts

    # (Optional) If you only want the repo name, you can use: repo_name = parts[-1]
    # But here we need both the owner and repo.

    # Get the default branch dynamically
    headers = {
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    default_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    default_branch_res = requests.get(default_branch_url, headers=headers).json()
    default_branch = default_branch_res.get("default_branch", "main")

    print(f"📥 Fetching docs for {repo_name} from branch {default_branch}...")

    def fetch_and_save_files(path="docs", local_dir=None, branch=default_branch):
        """
        Recursively fetches files from the GitHub API and saves them locally.
        """
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}?ref={branch}"
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch docs from {api_url}. Status Code: {response.status_code}, Message: {response.text}")
            return

        files = response.json()
        for file in files:
            # Compute relative path (strip leading "docs/")
            rel_path = Path(file["path"]).relative_to("docs")
            local_file_path = Path(local_dir) / rel_path

            if file["type"] == "dir":
                # Recursively process subdirectory
                fetch_and_save_files(file["path"], local_dir, branch)
            elif file["type"] == "file" and file["name"].endswith(".md"):
                # Download the Markdown file
                file_content = requests.get(file["download_url"], headers=headers).text
                local_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(local_file_path, "w", encoding="utf-8") as f:
                    f.write(file_content)

    # Define the target directory as: docs/projects/{repo_name}/latest/docs
    target_dir = Path(PROJECTS_DIR) / repo_name / "latest" / "docs"
    target_dir.mkdir(parents=True, exist_ok=True)

    # Start fetching from the child repo's "docs" folder
    fetch_and_save_files("docs", target_dir, default_branch)

    print(f"✅ Successfully fetched docs for {repo_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: No repository name provided. This script must be called with the repository name (e.g., 'SHINO-01/RTD_CHILD_01').")
        sys.exit(1)

    full_repo_name = sys.argv[1]
    fetch_docs(full_repo_name)
