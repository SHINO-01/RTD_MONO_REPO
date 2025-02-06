import os
import shutil
from pathlib import Path

# Constants
PROJECTS_DIR = "docs/projects"
MAX_VERSIONS = 5  # Maximum number of versions to keep per project

def cleanup_versions():
    if not os.path.exists(PROJECTS_DIR):
        print(f"Warning: {PROJECTS_DIR} does not exist. Skipping cleanup.")
        return

    for project in os.listdir(PROJECTS_DIR):
        project_path = Path(PROJECTS_DIR) / project
        if not project_path.is_dir():
            continue

        # List all version directories (e.g., v1.0.8, v1.0.7, etc.) 
        versions = sorted(
            [v for v in os.listdir(project_path) if (project_path / v).is_dir()],
            key=lambda x: tuple(map(int, x[1:].split("."))) if x.startswith("v") else (0,),
            reverse=True
        )

        if len(versions) > MAX_VERSIONS:
            old_versions = versions[MAX_VERSIONS:]
            for version in old_versions:
                version_path = project_path / version
                print(f"Deleting old version: {version_path}")
                shutil.rmtree(version_path)

if __name__ == "__main__":
    cleanup_versions()
