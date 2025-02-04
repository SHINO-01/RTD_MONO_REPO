#!/bin/bash
# Cleanup old versions, keep latest 5 only

PROJECTS_DIR="projects"
MAX_VERSIONS=5

for project in "$PROJECTS_DIR"/*; do
  if [ -d "$project/versions" ]; then
    cd "$project/versions" || continue
    versions=( $(ls -d v* 2>/dev/null | sort -V) )
    count=${#versions[@]}
    if [ "$count" -gt "$MAX_VERSIONS" ]; then
      num_to_delete=$((count - MAX_VERSIONS))
      echo "Deleting $num_to_delete old version(s) in $project/versions"
      for ((i=0; i<num_to_delete; i++)); do
        rm -rf "${versions[$i]}"
      done
    fi
    cd - >/dev/null || exit
  fi
done
