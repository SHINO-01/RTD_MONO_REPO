import os
import yaml
from pathlib import Path

DOCS_ROOT = "docs/projects"
MKDOCS_FILE = "mkdocs.yml"

def generate_nav_entry(directory):
    """Recursively generate navigation entries for a directory."""
    nav = []
    items = sorted(os.listdir(directory))
    for item in items:
        item_path = os.path.join(directory, item)
        rel_path = str(Path(item_path).relative_to("docs"))
        if os.path.isdir(item_path):
            children = generate_nav_entry(item_path)
            if children:
                nav.append({item.replace("_", " ").title(): children})
        elif item.endswith(".md"):
            # Use the file name (without extension) as the nav title
            name = item[:-3].replace("_", " ").title()
            nav.append({name: rel_path})
    return nav

def generate_nav():
    main_nav = [
        {"Home": "index.md"}
    ]
    projects_nav = []

    for project in sorted(os.listdir(DOCS_ROOT)):
        project_path = os.path.join(DOCS_ROOT, project)
        if os.path.isdir(project_path):
            version_dirs = sorted(
                [v for v in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, v))],
                key=lambda x: x,  # You might adjust sorting if version names follow semver
                reverse=True
            )
            version_entries = []
            for version in version_dirs:
                docs_path = os.path.join(project_path, version, "docs")
                if os.path.exists(docs_path):
                    nav_entry = generate_nav_entry(docs_path)
                    if nav_entry:
                        version_entries.append({version: nav_entry})
            if version_entries:
                projects_nav.append({project.replace("_", " ").title(): version_entries})

    full_nav = main_nav + [{"Projects": projects_nav}]

    # Load the existing mkdocs.yml, update its nav, and write it back
    with open(MKDOCS_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    config["nav"] = full_nav
    
    with open(MKDOCS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print("✅ Navigation structure updated in mkdocs.yml")

if __name__ == "__main__":
    generate_nav()
