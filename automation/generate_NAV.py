import os
import yaml

PROJECTS_DIR = "docs/projects"
NAV_FILE = "mkdocs.yml"

def generate_nav():
    nav = {
        "Home": "index.md",
        "Projects": {}
    }

    # Loop through projects and versions
    for project in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project)
        if os.path.isdir(project_path):
            project_nav = {}
            for version in os.listdir(project_path):
                version_path = os.path.join(project_path, version)
                if os.path.isdir(version_path):
                    docs_dir = os.path.join(version_path, "docs")
                    if os.path.isdir(docs_dir):
                        version_nav = []
                        # Loop through the docs files and subdirectories
                        for root, dirs, files in os.walk(docs_dir):
                            for file in files:
                                if file.endswith(".md"):
                                    rel_path = os.path.relpath(os.path.join(root, file), PROJECTS_DIR)
                                    version_nav.append(f"{rel_path}")
                        project_nav[version] = version_nav
            if project_nav:
                nav["Projects"][project] = project_nav

    # Write the generated nav to mkdocs.yml
    with open(NAV_FILE, "r") as f:
        mkdocs_config = yaml.safe_load(f)

    mkdocs_config["nav"] = nav

    with open(NAV_FILE, "w") as f:
        yaml.dump(mkdocs_config, f, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    generate_nav()
