import os
import requests
from pathlib import Path
import sys

# Constants
PROJECTS_DIR = "docs/projects"
GH_TOKEN = os.getenv("GH_PAT_TOKEN")
MAX_VERSIONS = 5  # Max number of versions to keep

def fetch_docs(repo_name):
    """
    Fetches all documentation files from a given GitHub repository for multiple branches.
    """
    if not GH_TOKEN:
        print("❌ Error: GitHub token is missing. Set GH_PAT_TOKEN as an environment variable.")
        sys.exit(1)

    # Ensure repo_name does NOT contain the org name twice
    repo_owner = "SHINO-01"
    repo_name = repo_name.split("/")[-1]  # Extract only "RTD_CHILD_01"
    
    # Get all branches (to find version branches)
    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    branches_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches"
    branches_res = requests.get(branches_url, headers=headers).json()

    # Filter branches that start with "v" (indicating version branches like v1.0.0, v1.1.0, etc.)
    version_branches = sorted(
        [branch["name"] for branch in branches_res if branch["name"].startswith("v")],
        reverse=True
    )[:MAX_VERSIONS]  # Keep only the latest MAX_VERSIONS

    if not version_branches:
        print(f"❌ No version branches found for {repo_name}")
        sys.exit(1)

    print(f"📥 Fetching docs for {repo_name} from branches: {', '.join(version_branches)}...")

    def fetch_and_save_files(path="docs", local_dir=None, branch=None):
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
            file_path = Path(file["path"].replace("docs/", ""))  # Keep relative path after `docs/`
            local_file_path = Path(local_dir) / file_path

            if file["type"] == "dir":
                # Recursively fetch subdirectory contents
                fetch_and_save_files(file["path"], local_dir, branch)
            elif file["type"] == "file" and file["name"].endswith(".md"):
                # Download Markdown file
                file_content = requests.get(file["download_url"], headers=headers).text
                local_file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
                with open(local_file_path, "w", encoding="utf-8") as f:
                    f.write(file_content)

    # Fetch docs for each versioned branch
    for branch in version_branches:
        target_dir = Path(PROJECTS_DIR) / repo_name / branch / "docs"
        target_dir.mkdir(parents=True, exist_ok=True)

        # Start fetching files recursively for this branch
        fetch_and_save_files("docs", target_dir, branch)

    print(f"✅ Successfully fetched docs for {repo_name} from branches: {', '.join(version_branches)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: No repository name provided. This script must be called with the repository name.")
        sys.exit(1)

    repo_name = sys.argv[1]
    fetch_docs(repo_name)
