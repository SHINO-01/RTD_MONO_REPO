import os
import yaml
from pathlib import Path

DOCS_ROOT = "docs/projects"
NAV_FILE = "mkdocs.yml"

def generate_nav_entry(directory):
    """Recursively generate nav entries for a directory"""
    nav = []
    
    # Get all items in directory, sorted with indexes first
    items = sorted(os.listdir(directory), key=lambda x: (not x.startswith("index.md"), x))
    
    for item in items:
        path = os.path.join(directory, item)
        rel_path = str(Path(path).relative_to(DOCS_ROOT))
        
        if os.path.isdir(path):
            # Directory: create nested entry
            children = generate_nav_entry(path)
            if children:
                dir_name = item.replace("_", " ").title()
                nav.append({dir_name: children})
        elif item.endswith(".md"):
            # Markdown file: create entry
            if item == "index.md":
                # Index file comes first
                nav.insert(0, rel_path)
            else:
                # Other files
                name = item[:-3].replace("_", " ").title()
                nav.append({name: rel_path})
    
    return nav

def generate_nav():
    main_nav = [
        {"Home": "index.md"},
        {"Projects": "projects/index.md"}
    ]
    
    projects_nav = []
    
    # Process each project
    for project in sorted(os.listdir(DOCS_ROOT)):
        project_path = os.path.join(DOCS_ROOT, project)
        if os.path.isdir(project_path) and project != "index.md":
            versions = sorted(
                [v for v in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, v))],
                key=lambda x: tuple(map(int, x[1:].split("."))),
                reverse=True
            )
            
            version_entries = []
            for version in versions:
                version_path = os.path.join(project_path, version, "docs")
                if os.path.exists(version_path):
                    version_nav = generate_nav_entry(version_path)
                    if version_nav:
                        version_entries.append({version: version_nav})
            
            if version_entries:
                project_name = project.replace("_", " ").title()
                projects_nav.append({project_name: version_entries})
    
    # Combine all navigation entries
    full_nav = main_nav + projects_nav
    
    # Update mkdocs.yml
    with open(NAV_FILE, "r") as f:
        config = yaml.safe_load(f)
    
    config["nav"] = full_nav
    
    with open(NAV_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

if __name__ == "__main__":
    generate_nav()