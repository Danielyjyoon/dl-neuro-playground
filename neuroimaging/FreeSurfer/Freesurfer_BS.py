import os
import nibabel as nib
import numpy as np
from scipy.stats import mode
import argparse
import time


def median(data, coord, radius):
    """Calculate the median of voxel values in a 3D neighborhood."""
    x, y, z = coord
    radius_range = range(-radius, radius + 1)
    pix = [
        data[x + dx, y + dy, z + dz]
        for dx in radius_range
        for dy in radius_range
        for dz in radius_range
        if 0 <= x + dx < data.shape[0]
        and 0 <= y + dy < data.shape[1]
        and 0 <= z + dz < data.shape[2]
        and data[x + dx, y + dy, z + dz] != 16  # Exclude value 16
    ]
    if not pix:
        return 16
    res = mode(pix)
    # Ensure the mode result is an array before indexing
    mode_value = np.atleast_1d(res.mode)[0]
    return mode_value


def merge_brainstem_label(root_dir):
    """Merge brainstem labels into DKT atlas."""
    err_list = []

    for pid in os.listdir(root_dir):
        pid_dir = os.path.join(root_dir, pid)
        target_path = os.path.join(pid_dir, 'bs_DKT.nii')

        # Skip if already processed
        if os.path.exists(target_path):
            print(f'Already done: {pid}')
            continue

        seg_path = os.path.join(pid_dir, 'DKT.nii')
        brainstem_path = os.path.join(pid_dir, 'Brainstem.nii')

        # Ensure required files exist
        if not (os.path.exists(seg_path) and os.path.exists(brainstem_path)):
            print(f"Missing files for PID: {pid}")
            continue

        try:
            start = time.time()

            # Load NIfTI files
            dkt = nib.load(seg_path)
            bs = nib.load(brainstem_path)

            dkt_np = dkt.get_fdata().astype(np.int16)
            bs_np = bs.get_fdata().astype(np.int16)

            # Merge brainstem labels into DKT
            brainstem_labels = {173, 174, 175}
            dkt_np[bs_np == 173] = 173
            dkt_np[bs_np == 174] = 174
            dkt_np[bs_np == 175] = 175

            print('Brainstem label merged into DKT')

            # Refine DKT atlas
            while True:
                changed = False
                dkt_copy = dkt_np.copy()

                for x in range(dkt_np.shape[0]):
                    for y in range(dkt_np.shape[1]):
                        for z in range(dkt_np.shape[2]):
                            if dkt_np[x, y, z] == 16:
                                dkt_copy[x, y, z] = median(dkt_np, (x, y, z), 1)
                                changed = True

                dkt_np = dkt_copy
                print('Refinement cycle completed')

                if not changed:
                    break

            # Save the merged and refined NIfTI file
            dkt_header = dkt.header.copy()
            dkt_header['bitpix'] = 16
            dkt_header['scl_slope'] = 1
            dkt_header['scl_inter'] = 0

            merged_nii = nib.Nifti1Image(dkt_np, affine=dkt.affine, header=dkt_header)
            nib.save(merged_nii, target_path)

            print(f'{pid} processed in {time.time() - start:.2f} seconds')

        except Exception as e:
            print(f"Error processing PID {pid}: {e}")
            err_list.append(pid)

    # Print error list
    if err_list:
        print("Errors occurred for the following PIDs:")
        print(err_list)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Merge brainstem labels into DKT atlas.")
    parser.add_argument(
        '--root_dir', 
        type=str, 
        help="Path to the root directory containing PID folders."
    )
    
    # Parse arguments
    args = parser.parse_args()

    # Merge brainstem labels
    print("Merging brainstem labels into DKT...")
    merge_brainstem_label(args.root_dir)


if __name__ == '__main__':
    main()
