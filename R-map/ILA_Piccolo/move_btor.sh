#!/bin/bash

# Define the base directory and target directory
base_dir="/data/guangyuh/coding_env/HWMCC24-benchmark/R-map/ILA_Piccolo/verification"
target_dir="/data/guangyuh/coding_env/HWMCC24-benchmark/btor2_only/array"

# Create the target directory if it doesn't exist
mkdir -p "$target_dir"

# Find all .btor2 files, rename them, and copy them to the target directory
find "$base_dir" -name "*.btor2" | while read -r file; do
  # Get the directory name
  dir_name=$(basename "$(dirname "$file")")
  # Get the file name
  file_name=$(basename "$file")
  # Construct the new file name
  new_file_name="ILA_Piccolo_${dir_name}_${file_name}"
  # Rename and copy the file to the target directory
  cp "$file" "$target_dir/$new_file_name"
  echo "Copied and renamed $file to $target_dir/$new_file_name"
done