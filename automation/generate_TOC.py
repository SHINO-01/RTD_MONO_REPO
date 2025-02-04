import os

DOCS_DIR = "docs/projects"
INDEX_FILE = "docs/index.md"

def generate_toc():
    toc = ["# Unified Project Documentation\n", "## Table of Contents\n"]

    projects = sorted([d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d))])

    for project in projects:
        project_path = os.path.join(DOCS_DIR, project)
        versions = sorted(
            [v for v in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, v))],
            reverse=True
        )

        if versions:
            latest_version = versions[0]
            latest_docs_path = f"{DOCS_DIR}/{project}/{latest_version}/docs/index.md"
            toc.append(f"- **[{project.replace('_', ' ').title()} - {latest_version}]({latest_docs_path})**\n")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.writelines(toc)

if __name__ == "__main__":
    generate_toc()
