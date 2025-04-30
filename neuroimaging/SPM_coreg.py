import os
import argparse
import pandas as pd
from nipype.interfaces import spm
from nipype.interfaces.matlab import MatlabCommand
from nipype.interfaces.spm import Coregister

def main(args):
    # ✅ MATLAB Runtime 설정
    matlab_cmd = '/usr/local/spm12/run_spm12.sh /usr/local/MATLAB/MATLAB_Runtime/v97/ script'
    use_mcr = True

    # ✅ SPM 설정
    MatlabCommand.set_default_matlab_cmd(matlab_cmd)
    MatlabCommand.set_default_paths('/usr/local/spm12')
    spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=use_mcr)

    # If you prefer to use an Excel file for the PID list, uncomment the following:
    # excel_path = '/nas/yj/centiloid/2025/failed_pids.csv'
    # pid_list = pd.read_csv(excel_path)['PID'].dropna().astype(str).tolist()

    # Otherwise, generate PID list from subdirectories in the provided root_dir
    pid_list = [d for d in os.listdir(args.root_dir)
                if os.path.isdir(os.path.join(args.root_dir, d))]

    # Initialize success and failure lists
    success_pids = []
    failed_pids = []

    # Iterate through each PID directory and perform coregistration
    for pid in pid_list:
        pid_path = os.path.join(args.root_dir, pid)
        target_file = os.path.join(pid_path, 'orig.nii')
        source_file = os.path.join(pid_path, args.source_file)  # Source file from argument

        # Check if both target and source files exist
        if os.path.exists(target_file) and os.path.exists(source_file):
            print(f'Processing PID: {pid}')
            coreg = Coregister()
            coreg.inputs.target = target_file
            coreg.inputs.source = source_file
            coreg.inputs.out_prefix = 'r'
            try:
                coreg.run()
                print(f'Successfully coregistered for {pid}')
                success_pids.append(pid)
            except Exception as e:
                print(f'Error processing {pid}: {e}')
                failed_pids.append(pid)
        else:
            print(f'Missing files in {pid}: {args.source_file} or orig.nii not found')
            failed_pids.append(pid)

    # Optionally, save the success and failure lists to CSV files
    # success_df = pd.DataFrame(success_pids, columns=['Successful_PID'])
    # failed_df = pd.DataFrame(failed_pids, columns=['Failed_PID'])
    # success_df.to_csv('successful_pids.csv', index=False)
    # failed_df.to_csv('failed_pids.csv', index=False)

    print("Processing complete. Results saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coregistration processing script.")
    parser.add_argument("--root_dir", type=str, required=True,
                        help="Root directory containing PID directories.")
    parser.add_argument("--source_file", type=str, default="PT.nii",
                        help="Source file name for coregistration (e.g., PT.nii).")
    args = parser.parse_args()
    
    main(args)
