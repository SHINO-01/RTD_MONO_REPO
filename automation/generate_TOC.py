import os

DOCS_DIR = "projects"
INDEX_FILE = "landing_page/docs/index.md"

def generate_toc():
    toc = ["# Unified Project Documentation\n", "## Table of Contents\n"]

    projects = sorted([d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d))])

    for project in projects:
        versions_dir = os.path.join(DOCS_DIR, project, "versions")
        if not os.path.exists(versions_dir):
            continue
        
        latest_version = sorted(os.listdir(versions_dir), reverse=True)[0]
        latest_docs_path = os.path.join(versions_dir, latest_version, "docs")

        if os.path.exists(latest_docs_path):
            toc.append(f"- **[{project.replace('_', ' ').title()}]({latest_docs_path}/index.md)**\n")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.writelines(toc)

if __name__ == "__main__":
    generate_toc()
