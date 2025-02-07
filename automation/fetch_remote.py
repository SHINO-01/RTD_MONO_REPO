import os
import requests
import sys
from pathlib import Path
from urllib.parse import urljoin

# Configuration
PROJECTS_DIR = Path("docs/projects")
MAX_VERSIONS = 5
REPO_OWNER = "SHINO-01"
BASE_API_URL = "https://api.github.com"

def get_env_vars():
    """Validate and return required environment variables"""
    token = os.getenv("GH_PAT_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    
    if not token:
        sys.exit("❌ Error: GH_PAT_TOKEN environment variable is missing")
    if not repo_name:
        sys.exit("❌ Error: REPO_NAME environment variable is missing")
    
    return token, repo_name.split("/")[-1]  # Ensure clean repo name

def get_version_branches(token, repo_name):
    """Fetch and sort version branches from GitHub"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{BASE_API_URL}/repos/{REPO_OWNER}/{repo_name}/branches"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        sys.exit(f"❌ Failed to fetch branches: {str(e)}")

    branches = [b["name"] for b in response.json() if b["name"].startswith("v")]
    return sorted(
        branches,
        key=lambda x: tuple(map(int, x[1:].split("."))),
        reverse=True
    )[:MAX_VERSIONS]

def fetch_docs(token, repo_name, version_branches):
    """Main documentation fetching logic"""
    for branch in version_branches:
        target_dir = PROJECTS_DIR / repo_name / branch / "docs"
        target_dir.mkdir(parents=True, exist_ok=True)
        fetch_branch_content(token, repo_name, branch, target_dir)

def fetch_branch_content(token, repo_name, branch, target_dir, path="docs"):
    """Recursively fetch content from a branch"""
    headers = {"Authorization": f"token {token}"}
    url = f"{BASE_API_URL}/repos/{REPO_OWNER}/{repo_name}/contents/{path}?ref={branch}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Warning: Skipping {path} in {branch} - {str(e)}")
        return

    for item in response.json():
        item_path = Path(item["path"])
        local_path = target_dir / item_path.relative_to("docs")
        
        if item["type"] == "dir":
            fetch_branch_content(token, repo_name, branch, target_dir, item["path"])
        elif item["type"] == "file" and item["name"].endswith(".md"):
            download_file(item["download_url"], local_path, headers)

def download_file(url, path, headers):
    """Download and save a single file"""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(response.text, encoding="utf-8")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Warning: Failed to download {url} - {str(e)}")

if __name__ == "__main__":
    gh_token, clean_repo = get_env_vars()
    versions = get_version_branches(gh_token, clean_repo)
    
    if not versions:
        sys.exit(f"❌ No version branches found for {clean_repo}")
    
    print(f"📥 Fetching docs for {clean_repo} branches: {', '.join(versions)}")
    fetch_docs(gh_token, clean_repo, versions)
    print("✅ Documentation fetch completed successfully")