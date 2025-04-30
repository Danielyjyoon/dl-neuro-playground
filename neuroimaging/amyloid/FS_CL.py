# This script processes FBB (PET) images for a list of patients, calculates SUVR values using specified ROIs, 
# and saves the results to an Excel file. It also handles errors and missing files gracefully.
import os
import nibabel as nib
from tqdm import tqdm
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter

# Define base directory
base = ''

# Initialize data storage lists
data_list = []
error_list = []


# #1. Loop through each patient folder
# # PID to string
# for pid in os.listdir(base):

#2. Loop through an excel file to get the PIDs
pids = pd.read_excel('.xlsx')['PID']
pids = pids.apply(lambda x: str(int(x)) if isinstance(x, float) else str(x)).tolist()

for pid in pids:
    
    FILE_DIR = os.path.join(base, pid)
    file_FBB = os.path.join(FILE_DIR, 'orig_FBB.nii')
    orig_mask_path = os.path.join(FILE_DIR, 'bs_DKT.nii')
    
    # Check if required files exist
    if not os.path.exists(file_FBB) or not os.path.exists(orig_mask_path):
        print(f"Missing files for PID: {pid}")
        error_list.append({'PID': pid, 'Missing Files': 'orig_FBB.nii or bs_DKT.nii'})
        continue  # Skip to the next PID
    
    try:
        # Load original mask
        orig_mask_load = nib.load(orig_mask_path)
        orig_mask = orig_mask_load.get_fdata()
        
        # Define target ROIs
        MRX_ROI_values = [1003, 2003, 1012, 2012, 1014, 2014, 1020, 2020, 1018, 2018, 1019, 2019,
                          1027, 2027, 1028, 2028, 1002, 2002, 1010, 2010, 1023, 2023, 1026, 2026,
                          1008, 2008, 1025, 2025, 1029, 2029, 1031, 2031, 1009, 2009, 1015, 2015,
                          1030, 2030]

        # Define reference ROIs
        WC_values = [7, 8, 46, 47]
        # CG_values = [8, 47]
        # pons_values = [174]
        # WM_values = [2, 41]
        
        # Create masks for each ROI
        newmask = np.in1d(orig_mask, MRX_ROI_values).reshape(orig_mask.shape).astype(float)
        WC_mask = np.in1d(orig_mask, WC_values).reshape(orig_mask.shape).astype(float)
        # CG_mask = np.in1d(orig_mask, CG_values).reshape(orig_mask.shape).astype(float)
        # pons_mask = np.in1d(orig_mask, pons_values).reshape(orig_mask.shape).astype(float)
        # WM_mask = np.in1d(orig_mask, WM_values).reshape(orig_mask.shape).astype(float)

        # # Smooth the WM mask
        # sigma = 8 / (2 * np.sqrt(2 * np.log(2)))
        # smoothed_mask = gaussian_filter(WM_mask.astype(float), sigma=sigma)

        # # Threshold the smoothed mask at 0.7
        # thresholded_mask = (smoothed_mask > 0.7).astype(int)
        
        # Load FBB (PET) image and replace NaNs with 0
        FBB = np.array(nib.load(file_FBB).dataobj).astype(float)
        FBB = np.nan_to_num(FBB, nan=0.0)  # Replace NaN with 0
        
        # Apply masks to get ROIs
        MRX_ROI = np.multiply(FBB, newmask)
        WC_ROI = np.multiply(FBB, WC_mask)
        # CG_ROI = np.multiply(FBB, CG_mask)
        # pons_ROI = np.multiply(FBB, pons_mask)
        # WM_ROI = np.multiply(FBB, thresholded_mask)
        
        # Filter non-zero values
        MRX_ROI = MRX_ROI[MRX_ROI != 0]
        WC_ROI = WC_ROI[WC_ROI != 0]
        # CG_ROI = CG_ROI[CG_ROI != 0]
        # pons_ROI = pons_ROI[pons_ROI != 0]
        # WM_ROI = WM_ROI[WM_ROI != 0]
        
        # Calculate SUVR values for each reference region
        SUVR_WC = MRX_ROI.mean() / WC_ROI.mean() if WC_ROI.size > 0 else np.nan
        # SUVR_CG = MRX_ROI.mean() / CG_ROI.mean() if CG_ROI.size > 0 else np.nan
        # SUVR_pons = MRX_ROI.mean() / pons_ROI.mean() if pons_ROI.size > 0 else np.nan
        # SUVR_Composite = MRX_ROI.mean() / WM_ROI.mean() if WM_ROI.size > 0 else np.nan
        
        # Append the results to the list
        data_list.append({
            'PID': pid,
            'SUVR_WC': SUVR_WC,
            # 'SUVR_CG': SUVR_CG,
            # 'SUVR_pons': SUVR_pons,
            # 'SUVR_Composite': SUVR_Composite
        })
    except Exception as e:
        print(f"Error processing PID {pid}: {e}")
        error_list.append({'PID': pid, 'Error': str(e)})

# Convert the data to a DataFrame and save to Excel
df = pd.DataFrame(data_list)
output_path = '.xlsx'
df.to_excel(output_path, index=False)
print(f"Results saved to {output_path}")

# Save error list to CSV
if error_list:
    error_df = pd.DataFrame(error_list)
    error_output_path = 'error_list.csv'
    error_df.to_csv(error_output_path, index=False)
    print(f"Error list saved to {error_output_path}")