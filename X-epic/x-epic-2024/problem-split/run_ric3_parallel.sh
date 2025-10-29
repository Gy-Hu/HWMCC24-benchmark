#!/bin/bash

# Script to recursively find all .aig and .aag files and run rIC3 solver on each
# with a timeout of 3600 seconds (1 hour) and configurable parallelism

# Default number of parallel jobs (use number of CPU cores)
PARALLEL_JOBS=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -j|--jobs)
            PARALLEL_JOBS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [-j|--jobs N]"
            echo "  -j, --jobs N    Number of parallel jobs (default: number of CPU cores)"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo "Running with $PARALLEL_JOBS parallel jobs"

# Create a directory to store logs
LOG_DIR="rIC3_solver_logs"
mkdir -p "$LOG_DIR"

# Find all .aig and .aag files recursively
echo "Finding all AIGER files (.aig and .aag)..."
AIGER_FILES=$(find . -name "*.aig" -o -name "*.aag")
TOTAL_FILES=$(echo "$AIGER_FILES" | wc -l)
echo "Found $TOTAL_FILES AIGER files."

# Counter for processed files
COUNTER=0

# Function to process a single file
process_file() {
    local FILE=$1
    local COUNTER=$2
    local TOTAL_FILES=$3
    
    # Extract filename without path and extension for log naming
    local FILENAME=$(basename "$FILE")
    local LOG_FILE="$LOG_DIR/${FILENAME%.*}_log.txt"
    
    echo "[$COUNTER/$TOTAL_FILES] Processing: $FILE"
    echo "Log will be saved to: $LOG_FILE"
    
    # Run rIC3 solver with timeout
    {
        echo "File: $FILE"
        echo "Command: ~/coding_env/rIC3/target/release/rIC3 $FILE"
        echo "Started at: $(date)"
        echo "----------------------------------------"
        
        # Run the solver with timeout and capture output
        timeout 3600 ~/coding_env/rIC3/target/release/rIC3 "$FILE" 2>&1
        
        # Check if the command timed out
        if [ $? -eq 124 ]; then
            echo "----------------------------------------"
            echo "STATUS: TIMEOUT (exceeded 3600 seconds)"
        else
            echo "----------------------------------------"
            echo "STATUS: COMPLETED"
        fi
        
        echo "Finished at: $(date)"
        echo "========================================"
    } > "$LOG_FILE"
    
    # Print progress (use directory-based locking for macOS compatibility)
    # mkdir is atomic on all Unix systems including macOS
    local LOCK_DIR="/tmp/rIC3_solver_lock.d"
    while ! mkdir "$LOCK_DIR" 2>/dev/null; do
        sleep 0.01
    done
    echo "Completed $COUNTER of $TOTAL_FILES files: $FILE"
    echo "----------------------------------------"
    rmdir "$LOCK_DIR"
}

# Process files in parallel with controlled concurrency
for FILE in $AIGER_FILES; do
    COUNTER=$((COUNTER + 1))

    # Wait if we've reached the maximum number of parallel jobs
    # Use jobs -r which is compatible with bash 3.2 (macOS default)
    while [ $(jobs -r | wc -l) -ge $PARALLEL_JOBS ]; do
        # Sleep briefly before checking again
        sleep 0.1
    done

    # Process the file in the background
    process_file "$FILE" "$COUNTER" "$TOTAL_FILES" &
done

# Wait for all remaining jobs to finish
wait

echo "All files processed. Logs are stored in the $LOG_DIR directory."