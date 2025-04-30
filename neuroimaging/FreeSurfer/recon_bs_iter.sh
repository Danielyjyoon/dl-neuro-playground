#!/bin/bash

# Root directory where the data is stored
data_directory="/nas/yj/centiloid/sev_YC_org"

# Loop through all PID directories in the data directory
for pid_dir in "${data_directory}"/*/; do
    # Extract the PID from the folder name
    pid=$(basename "$pid_dir")
    echo "Processing Brainstem Segmentation for PID: ${pid}"

    # Define SUBJECTS_DIR and result directory
    export SUBJECTS_DIR="${data_directory}/${pid}"
    result_dir="${SUBJECTS_DIR}/result"

    # Check if the result directory exists
    if [ -d "$result_dir" ]; then
        # Run Brainstem segmentation
        echo "Running brainstem segmentation for PID: ${pid}"
        segmentBS.sh result "${data_directory}/${pid}"

        echo "Brainstem segmentation completed for PID: ${pid}"
    else
        echo "Error: Result directory not found for PID: ${pid}. Skipping..."
    fi
done