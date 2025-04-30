import numpy as np
from collections import defaultdict
import csv
from tqdm import tqdm
import os
import nibabel as nib
def calculate_ROI_intensity_DKTatlas(file_CSV_ROI, seg_nifti, PET_256_nifti):

    np_MR_seg = seg_nifti.get_fdata().astype(int)
    np_MR_seg[np.isnan(np_MR_seg)] = 0

    np_PET = PET_256_nifti.get_fdata()
    np_PET[np.isnan(np_PET)] = 0
    
    np_ROI_intensity_dict = defaultdict(float)
    np_ROI_cnt_dict = defaultdict(int)
    
    np_ROI_intensity = np.zeros(2036)
    np_ROI_cnt = np.zeros(2036)
    np_ROI_avg = np.zeros(2036)
    
    for np_MR_seg_x, np_PET_x in zip(np_MR_seg, np_PET):
        for np_MR_seg_y, np_PET_y in zip(np_MR_seg_x, np_PET_x):
            for np_MR_seg_z, np_PET_z in zip(np_MR_seg_y, np_PET_y):
                np_ROI_intensity_dict[int(np_MR_seg_z)] += np_PET_z
                np_ROI_cnt_dict[int(np_MR_seg_z)] += 1
    
    with open(file_CSV_ROI, 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['no.', 'ROI_intensity_sum', 'ROI_cnt', 'ROI_average'])
        
        for i in sorted(np_ROI_intensity_dict.keys()):
            np_ROI_intensity[i] = np_ROI_intensity_dict[i]
            np_ROI_cnt[i] = np_ROI_cnt_dict[i]
            np_ROI_avg[i] = np_ROI_intensity_dict[i] / np_ROI_cnt_dict[i]
            if np.isnan(np_ROI_avg[i]):
                np_ROI_avg[i] = 0 
            wr.writerow([i, np_ROI_intensity_dict[i], np_ROI_cnt_dict[i], np_ROI_avg[i]])

base = r"C:\Users\byeby\Desktop\test\sb_LBD\Revision\sb_dcm_download"
pids = os.listdir(base)

for _, pid in tqdm(enumerate(pids), total=len(pids)):

    FILE_DIR = os.path.join(base, pid)
    file_CSV_ROI = os.path.join(FILE_DIR, f'RAW_Parc_MR_Early.csv')

    try:
        if os.path.exists(os.path.join(FILE_DIR, f'DKT.nii')) and os.path.exists(os.path.join(FILE_DIR, 'FDG_1.nii')) and not os.path.exists(file_CSV_ROI):
            file_CSV_ROI = os.path.join(FILE_DIR, f'RAW_Parc_MR_FDG_1.csv')
            seg_nifti = nib.load(os.path.join(FILE_DIR, f'DKT.nii'))
            PET_256_nifti = nib.load(os.path.join(FILE_DIR, 'FDG_1.nii'))

            calculate_ROI_intensity_DKTatlas(file_CSV_ROI, seg_nifti, PET_256_nifti)
        elif not os.path.exists(os.path.join(FILE_DIR, f'FDG_1.nii')):
            raise FileNotFoundError(f"FDG_1.nii not found for PID {pid}. Skipping...")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error for PID {pid}: {e}")