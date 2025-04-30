import os
import dicom2nifti

# Disable validation of slice increment
dicom2nifti.settings.disable_validate_slice_increment()

# Path to the root directory containing patient subdirectories
start_path = '.'

# Get a list of all subdirectories in the start path
data = [os.path.join(start_path, x) for x in os.listdir(start_path) if os.path.isdir(os.path.join(start_path, x))]

# Loop through each patient directory
for i in data:
    # Patient ID for future reference
    PID = os.path.basename(i)  # Extract the last part of the path, e.g., 'Patient1'

    # Early conversion
    file_MR = os.path.join(i, 'Early.nii')
    dir_DICOM = os.path.join(i, 'Early')
    if not os.path.exists(file_MR) and os.path.exists(dir_DICOM):
        try:
            dicom2nifti.dicom_series_to_nifti(dir_DICOM, file_MR, reorient_nifti=False)
            print("Early NIfTI file written:", file_MR)
        except Exception as e:
            print(f"Failed to convert Early DICOM series for {PID}: {e}")

    # Delay conversion
    file_PT = os.path.join(i, 'Delay.nii')
    dir_DICOM = os.path.join(i, 'Delay')
    if not os.path.exists(file_PT) and os.path.exists(dir_DICOM):
        try:
            dicom2nifti.dicom_series_to_nifti(dir_DICOM, file_PT, reorient_nifti=False)
            print("Delay NIfTI file written:", file_PT)
        except Exception as e:
            print(f"Failed to convert Delay DICOM series for {PID}: {e}")