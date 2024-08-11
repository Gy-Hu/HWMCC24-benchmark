#!/bin/bash

# Define the base directory as the current working directory plus "verification"
base_dir="$(pwd)/verification"

# Iterate over each subdirectory within the base directory
for dir in "$base_dir"/*/; do
  # Check if the directory contains the file gen_btor.ys
  if [[ -f "${dir}gen_btor.ys" ]]; then
    echo "Executing yosys gen_btor.ys in $dir"
    # Change into the directory and execute yosys in the background
    (cd "$dir" && yosys gen_btor.ys) &
  else
    echo "No gen_btor.ys file found in $dir"
  fi
done

# Wait for all background processes to complete
wait

echo "All yosys processes completed."
