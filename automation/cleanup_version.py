import os
import shutil

PROJECTS_DIR = "docs/projects"
MAX_VERSIONS = 5  # Keep only the latest 5 versions

def cleanup_versions():
    if not os.path.exists(PROJECTS_DIR):
        print(f"Warning: {PROJECTS_DIR} does not exist. Skipping cleanup.")
        return

    for project in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project)
        
        if not os.path.isdir(project_path):
            continue

        versions = sorted(
            [v for v in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, v))],
            reverse=True
        )

        if len(versions) > MAX_VERSIONS:
            old_versions = versions[MAX_VERSIONS:]

            for version in old_versions:
                version_path = os.path.join(project_path, version)
                print(f"Deleting old version: {version_path}")
                shutil.rmtree(version_path)

if __name__ == "__main__":
    cleanup_versions()
