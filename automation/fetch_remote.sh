#!/bin/bash
# Fetch docs from child repositories

REMOTE_LIST="automation/remotes.txt"
DEST_DIR="projects"

while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue

  project=$(echo "$line" | awk '{print $1}')
  repo_url=$(echo "$line" | awk '{print $2}')

  echo "Fetching docs for $project from $repo_url"

  TARGET_DIR="$DEST_DIR/$project/tree/main"
  mkdir -p "$TARGET_DIR"

  git archive --remote="$repo_url" HEAD docs | tar -x -C "$TARGET_DIR"
done < "$REMOTE_LIST"
