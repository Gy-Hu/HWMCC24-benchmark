#!/bin/bash

# Define the base directory
base_dir="/data/guangyuh/coding_env/HWMCC24-benchmark/R-map/ILA_Ridecore/verification"

# Iterate over each subdirectory
for dir in "$base_dir"/*/; do
  # Check if the directory contains the file gen_btor.ys
  if [[ -f "${dir}gen_btor.ys" ]]; then
    echo "Executing yosys gen_btor.ys in $dir"
    # Change into the directory and execute yosys
    (cd "$dir" && yosys gen_btor.ys)
  else
    echo "No gen_btor.ys file found in $dir"
  fi
done