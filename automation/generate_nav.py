import os
import yaml
from pathlib import Path
import re

DOCS_ROOT = Path("docs")
NAV_FILE = "mkdocs.yml"

def get_sorted_versions(versions):
    """Sort versions in descending order using semantic versioning"""
    def version_key(v):
        return tuple(map(int, re.findall(r'\d+', v)))  # Extract numbers for sorting
    
    return sorted(versions, key=version_key, reverse=True)

def generate_section_nav(start_path):
    """Recursively generate navigation structure for directories and markdown files"""
    nav = []
    items = sorted(start_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    
    for item in items:
        rel_path = item.relative_to(DOCS_ROOT).as_posix()
        
        if item.is_dir():
            children = generate_section_nav(item)
            if children:
                nav.append({item.name.replace("_", " ").title(): children})
        elif item.suffix == ".md":
            if item.name == "index.md":
                nav.insert(0, {"Overview": rel_path})
            else:
                nav.append({item.stem.replace("_", " ").title(): rel_path})
    
    return nav

def generate_project_nav():
    """Generate a dynamic navigation structure for all projects and versions"""
    nav_structure = [
        {"Home": "docs/index.md"},
        {"Projects": []}
    ]
    
    projects_dir = DOCS_ROOT / "projects"
    
    for project in sorted(projects_dir.iterdir()):
        if project.is_dir():
            versions = get_sorted_versions([v.name for v in project.iterdir() if v.is_dir()])
            project_nav = [{"Overview": f"projects/{project.name}/index.md"}]
            
            for version in versions:
                version_path = project / version / "docs"
                if version_path.exists():
                    version_nav = generate_section_nav(version_path)
                    if version_nav:
                        project_nav.append({version: version_nav})
            
            if project_nav:
                nav_structure[1]["Projects"].append({project.name.replace("_", " ").title(): project_nav})
    
    return nav_structure

def update_mkdocs_config(nav_data):
    """Update mkdocs.yml with generated navigation"""
    with open(NAV_FILE, "r") as f:
        config = yaml.safe_load(f) or {}

    config["nav"] = nav_data

    with open(NAV_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

if __name__ == "__main__":
    nav = generate_project_nav()
    update_mkdocs_config(nav)
    print("✅ Navigation updated successfully!")
