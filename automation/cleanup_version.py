import os
import shutil

PROJECTS_DIR = "projects"
MAX_VERSIONS = 5

def cleanup_versions():
    for project in os.listdir(PROJECTS_DIR):
        project_dir = os.path.join(PROJECTS_DIR, project, "versions")
        if not os.path.isdir(project_dir):
            continue

        versions = sorted(os.listdir(project_dir), reverse=True)
        if len(versions) > MAX_VERSIONS:
            to_delete = versions[MAX_VERSIONS:]
            for version in to_delete:
                shutil.rmtree(os.path.join(project_dir, version))
                print(f"Deleted old version: {version}")

if __name__ == "__main__":
    cleanup_versions()
