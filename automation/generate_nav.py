import os
import yaml
from pathlib import Path

DOCS_ROOT = Path("docs")
NAV_FILE = "mkdocs.yml"

def get_sorted_versions(versions):
    """Sort versions by semantic versioning"""
    return sorted(
        versions,
        key=lambda v: tuple(map(int, v[1:].split("."))),
        reverse=True
    )

def generate_section_nav(start_path):
    """Generate navigation entries recursively relative to docs root"""
    nav = []
    items = sorted(os.listdir(start_path), key=lambda x: (not x.startswith("index.md"), x))
    
    for item in items:
        item_path = start_path / item
        rel_path = item_path.relative_to(DOCS_ROOT)
        
        if item_path.is_dir():
            children = generate_section_nav(item_path)
            if children:
                nav.append({item.replace("_", " ").title(): children})
        elif item.endswith(".md"):
            nav_entry = str(rel_path).replace("\\", "/")
            if item == "index.md":
                nav.insert(0, nav_entry)
            else:
                nav.append({item[:-3].replace("_", " ").title(): nav_entry})
    
    return nav

def generate_project_nav():
    """Generate navigation for all projects and versions"""
    nav_structure = [
        {"Home": "index.md"},
        {"Projects": "projects/index.md"}
    ]
    
    projects_dir = DOCS_ROOT / "projects"
    for project in sorted(projects_dir.iterdir()):
        if project.is_dir() and project.name != "index.md":
            versions = get_sorted_versions([v.name for v in project.iterdir() if v.is_dir()])
            project_nav = []
            
            for version in versions:
                version_path = project / version / "docs"
                if version_path.exists():
                    version_nav = generate_section_nav(version_path)
                    if version_nav:
                        project_nav.append({version: version_nav})
            
            if project_nav:
                nav_structure.append({
                    project.name.replace("_", " ").title(): project_nav
                })
    
    return nav_structure

def update_mkdocs_config(nav_data):
    """Update mkdocs.yml with generated navigation"""
    with open(NAV_FILE, "r") as f:
        config = yaml.safe_load(f) or {}
    
    config["nav"] = nav_data
    
    with open(NAV_FILE, "w") as f:
        yaml.dump(config, f, 
                 default_flow_style=False, 
                 sort_keys=False, 
                 allow_unicode=True,
                 Dumper=yaml.SafeDumper)

if __name__ == "__main__":
    nav = generate_project_nav()
    update_mkdocs_config(nav)