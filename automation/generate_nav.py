import os
import yaml
from pathlib import Path

DOCS_ROOT = Path("docs")
NAV_FILE = "mkdocs.yml"
PROJECTS_INDEX = DOCS_ROOT / "projects" / "index.md"

def get_sorted_versions(versions):
    """Sort versions by semantic versioning"""
    return sorted(
        versions,
        key=lambda v: tuple(map(int, v[1:].split("."))),
        reverse=True
    )

def generate_section_markdown(start_path, level=0):
    """Generate Markdown content for a directory recursively"""
    markdown = []
    items = sorted(os.listdir(start_path), key=lambda x: (not x.startswith("index.md"), x))
    
    for item in items:
        item_path = start_path / item
        rel_path = item_path.relative_to(DOCS_ROOT)
        
        if item_path.is_dir():
            # Add directory header
            markdown.append(f"{'#' * (level + 2)} {item.replace('_', ' ').title()}\n")
            # Recursively add subdirectories and files
            markdown.extend(generate_section_markdown(item_path, level + 1))
        elif item.endswith(".md"):
            # Add file link
            if item == "index.md":
                markdown.append(f"- [{item_path.parent.name.replace('_', ' ').title()}]({rel_path})\n")
            else:
                markdown.append(f"- [{item[:-3].replace('_', ' ').title()}]({rel_path})\n")
    
    return markdown

def generate_projects_markdown():
    """Generate Markdown content for all projects and versions"""
    markdown = ["# Projects\n\n"]
    
    projects_dir = DOCS_ROOT / "projects"
    for project in sorted(projects_dir.iterdir()):
        if project.is_dir() and project.name != "index.md":
            markdown.append(f"## {project.name.replace('_', ' ').title()}\n")
            
            versions = get_sorted_versions([v.name for v in project.iterdir() if v.is_dir()])
            for version in versions:
                version_path = project / version / "docs"
                if version_path.exists():
                    markdown.append(f"### {version}\n")
                    markdown.extend(generate_section_markdown(version_path))
                    markdown.append("\n")
    
    return "".join(markdown)

def update_projects_index(markdown_content):
    """Write the generated Markdown content to docs/projects/index.md"""
    with open(PROJECTS_INDEX, "w", encoding="utf-8") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    markdown = generate_projects_markdown()
    update_projects_index(markdown)
    print(f"✅ Successfully updated {PROJECTS_INDEX}")