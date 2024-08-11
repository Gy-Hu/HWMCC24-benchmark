#!/bin/bash

# Define the base directory as the current working directory plus "verification"
base_dir="$(pwd)/verification"

# Set the maximum number of parallel jobs
max_jobs=2
current_jobs=0

# Iterate over each subdirectory within the base directory
for dir in "$base_dir"/*/; do
  # Check if the directory contains the file gen_btor.ys
  if [[ -f "${dir}gen_btor.ys" ]]; then
    echo "Executing yosys gen_btor.ys in $dir"
    # Change into the directory and execute yosys in the background
    (cd "$dir" && yosys gen_btor.ys) &

    # Increment the count of current jobs
    current_jobs=$((current_jobs + 1))

    # If the current number of jobs reaches max_jobs, wait for one to finish
    if [[ $current_jobs -ge $max_jobs ]]; then
      wait -n  # Wait for any background process to finish
      current_jobs=$((current_jobs - 1))
    fi
  else
    echo "No gen_btor.ys file found in $dir"
  fi
done

# Wait for all remaining background processes to complete
wait

echo "All yosys processes completed."
