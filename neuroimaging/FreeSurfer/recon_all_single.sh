#!/bin/bash

# Root directory where the data is stored
data_directory="/nas/yj/centiloid/sev_YC_org"

# List of PIDs to process (add more PIDs separated by space)
pids=("6546044")

# Loop through each PID
for pid in "${pids[@]}"; do
    echo "Processing PID: ${pid}"

    # Define SUBJECTS_DIR and file paths
    export SUBJECTS_DIR="${data_directory}/${pid}"
    t1_file="${SUBJECTS_DIR}/MR.nii"  # T1 file is MR.nii
    t2_flair_file="${SUBJECTS_DIR}/${pid}_T2FLAIR.nii"
    result_dir="${SUBJECTS_DIR}/result"

    # Check if T1 (MR.nii) exists
    if [ -f "$t1_file" ]; then
        if [ -f "$t2_flair_file" ]; then
            echo "Running recon-all with MR.nii (T1) and T2 FLAIR for PID: ${pid}"
            recon-all -i "$t1_file" -T2 "$t2_flair_file" -s "$result_dir" -T2pial -all
        else
            echo "Running recon-all with MR.nii (T1 only) for PID: ${pid}"
            recon-all -i "$t1_file" -s "$result_dir" -all
        fi

        # Brainstem segmentation
        echo "Running brainstem segmentation for PID: ${pid}"
        segmentBS.sh result "${data_directory}/${pid}"

        echo "Processing completed for PID: ${pid}"
    else
        echo "Error: MR.nii (T1 file) not found for PID: ${pid}. Skipping..."
    fi
done