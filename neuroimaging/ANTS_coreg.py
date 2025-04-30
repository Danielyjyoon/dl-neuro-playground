import os
import ants
import dicom2nifti
import dicom2nifti.settings as settings
settings.disable_validate_slice_increment()

import nibabel as nib
from tqdm import tqdm

base = r'C:\Users\byeby\Desktop\test\FMM'
pids = os.listdir(base)

def register_pet_to_mr(patient_dir, pet_file, ref_file, output_file):
    """
    Perform ants.registration to align PET to MR image.

    Parameters:
        patient_dir (str): Path to the patient directory.
        pet_file (str): Name of the PET file to register.
        ref_file (str): Name of the reference MR file.
        output_file (str): Name of the output resliced PET file.
    """
    file_PET = os.path.join(patient_dir, pet_file)
    file_MR_256 = os.path.join(patient_dir, ref_file)
    file_output = os.path.join(patient_dir, output_file)

    # Check if reference and PET files exist and the output file does not already exist
    if not os.path.exists(file_PET):
        print(f"PET file not found: {file_PET}. Skipping...")
        return
    if not os.path.exists(file_MR_256):
        print(f"Reference MR file not found: {file_MR_256}. Skipping...")
        return
    if os.path.exists(file_output):
        print(f"Output file already exists: {file_output}. Skipping...")
        return

    try:
        # Load PET and MR images
        src_image = ants.image_read(file_PET)
        dst_image = ants.image_read(file_MR_256)

        # Perform rigid registration
        registration = ants.registration(fixed=dst_image, moving=src_image, type_of_transform='Rigid')
        ants.image_write(registration['warpedmovout'], file_output)
        print(f"Registered {pet_file} to {ref_file}, saved as {output_file}")
    except Exception as e:
        print(f"Failed to register {pet_file} for {os.path.basename(patient_dir)}: {e}")
    
# Iterate over patient IDs
for pid in tqdm(pids, total=len(pids)):
    patient_dir = os.path.join(base, pid)
    file_ST_256 = 'orig.nii'  # Reference MR file

    # Register FDG_1.nii
    register_pet_to_mr(patient_dir, 'FDG_1.nii', file_ST_256, 'rFDG_1.nii')

    # Register FDG_2.nii
    register_pet_to_mr(patient_dir, 'FDG_2.nii', file_ST_256, 'rFDG_2.nii')

    # Optionally, add more registrations here if needed