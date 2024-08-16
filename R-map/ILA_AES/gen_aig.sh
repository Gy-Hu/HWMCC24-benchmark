#!/bin/bash

# Define the base directory as the current working directory plus "verification"
base_dir="$(pwd)/verification"

# Iterate over each subdirectory within the base directory
for dir in "$base_dir"/*/; do
  # Check if the directory contains the file gen_btor.ys
  if [[ -f "${dir}gen_aig.ys" ]]; then
    echo "Executing yosys gen_aig.ys in $dir"
    # Change into the directory and execute yosys
    (cd "$dir" && yosys gen_aig.ys)
  else
    echo "No gen_aig.ys file found in $dir"
  fi
done