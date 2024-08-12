#!/bin/bash

# Define the base directory as the current working directory plus "verification"
base_dir="$(pwd)/verification"
target_dir="$(pwd)/../../btor2_only/array"  # Adjust this relative path as needed

# Get the current folder name (parent of the verification directory)
folder_name=$(basename "$(pwd)")

# Create the target directory if it doesn't exist
mkdir -p "$target_dir"

# Find all .btor2 files, rename them, and copy them to the target directory
find "$base_dir" -name "*.btor2" | while read -r file; do
  # Get the directory name
  dir_name=$(basename "$(dirname "$file")")
  # Get the file name
  file_name=$(basename "$file")
  # Construct the new file name using the current folder name
  new_file_name="${folder_name}_${dir_name}_${file_name}"
  # Rename and copy the file to the target directory
  cp "$file" "$target_dir/$new_file_name"
  echo "Copied and renamed $file to $target_dir/$new_file_name"
done