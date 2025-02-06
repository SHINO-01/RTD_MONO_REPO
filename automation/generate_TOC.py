import os

DOCS_DIR = "docs/projects"
NAV_FILE = "mkdocs.yml"

def generate_nav():
    nav = ["nav:"]
    
    projects = sorted([d for d in os.listdir(DOCS_DIR) if os.path.isdir(os.path.join(DOCS_DIR, d))])

    for project in projects:
        project_entry = f"  - {project.replace('_', ' ').title()}:"
        versions = sorted(
            [v for v in os.listdir(os.path.join(DOCS_DIR, project)) if os.path.isdir(os.path.join(DOCS_DIR, project, v))],
            reverse=True
        )

        version_entries = [f"    - {version}: {DOCS_DIR}/{project}/{version}/docs/index.md" for version in versions]
        project_entry += "\n" + "\n".join(version_entries)
        
        nav.append(project_entry)

    with open(NAV_FILE, "a", encoding="utf-8") as f:  # Append to mkdocs.yml
        f.write("\n" + "\n".join(nav) + "\n")

if __name__ == "__main__":
    generate_nav()
