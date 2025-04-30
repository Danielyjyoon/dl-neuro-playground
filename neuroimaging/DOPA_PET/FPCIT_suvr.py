import os
import nibabel as nib
from tqdm import tqdm
import numpy as np
import pandas as pd
import pydicom
base = 'sb_dcm_download'
mask_path='masks'
occipital_dir=os.path.join(mask_path,'181024_FPCIT_ROI_111_Asan_final.nii')
occ=nib.load(occipital_dir)
pids = os.listdir(base)
data_list = []
orig_mask=occ.get_fdata()
newmask = np.in1d(orig_mask, [13]).reshape( 157,189,156)
newmask=newmask.astype(float)
finalb_img=nib.Nifti1Image(newmask, occ.affine)
#maskb_path=os.path.join(mask_path, 'CIT_occi.nii')
#nib.save(finalb_img,maskb_path)
for _, pid in tqdm(enumerate(pids), total=len(pids)):
    FILE_DIR = os.path.join(base, pid)
    
    file_masked=os.path.join(FILE_DIR, 'wPET_Delay.nii')
    
    masked=nib.load(file_masked)
    masked1=np.array(masked.dataobj)
    OCC_ROI=np.multiply(masked1,newmask)
    lapmask= np.in1d(orig_mask, [5]).reshape( 157,189,156).astype(float)
    lppmask= np.in1d(orig_mask, [9]).reshape( 157,189,156).astype(float)
    lacmask= np.in1d(orig_mask, [3]).reshape( 157,189,156).astype(float)
    lpcmask=  np.in1d(orig_mask, [7]).reshape( 157,189,156).astype(float)
    rapmask= np.in1d(orig_mask, [6]).reshape( 157,189,156).astype(float)
    rppmask= np.in1d(orig_mask, [10]).reshape( 157,189,156).astype(float)
    racmask= np.in1d(orig_mask, [4]).reshape( 157,189,156).astype(float)
    rpcmask=  np.in1d(orig_mask, [8]).reshape( 157,189,156).astype(float)
    lvsmask=  np.in1d(orig_mask, [1]).reshape( 157,189,156).astype(float)
    rvsmask=  np.in1d(orig_mask, [2]).reshape( 157,189,156).astype(float)
    lvpmask=  np.in1d(orig_mask, [11]).reshape( 157,189,156).astype(float)
    rvpmask=  np.in1d(orig_mask, [12]).reshape( 157,189,156).astype(float)
    OCC_ROI=OCC_ROI[OCC_ROI>0]
    mean=OCC_ROI.mean()
    LAP_ROI=np.multiply(lapmask,masked1)
    LPP_ROI=np.multiply(lppmask,masked1)
    LAC_ROI=np.multiply(lacmask,masked1)
    LPC_ROI=np.multiply(lpcmask,masked1)
    RAP_ROI=np.multiply(rapmask,masked1)
    RPP_ROI=np.multiply(rppmask,masked1)
    RAC_ROI=np.multiply(racmask,masked1)
    RPC_ROI=np.multiply(rpcmask,masked1)
    LVS_ROI=np.multiply(lvsmask,masked1)
    RVS_ROI=np.multiply(rvsmask,masked1)
    LVP_ROI=np.multiply(lvpmask,masked1)
    RVP_ROI=np.multiply(rvpmask,masked1)
    #masked1=masked1/mean
    #maskb_path=os.path.join(FILE_DIR, 'Delay_divided.nii')
    #finalm_img=nib.Nifti1Image(masked1, masked.affine)
    #nib.save(finalm_img,maskb_path)
    #PAR_ROI=PAR_ROI[PAR_ROI!=0]
    '''dicom_folder=os.path.join(FILE_DIR, 'FDG')
    #masked_image=masked[masked!=0]
    for filename in os.listdir(dicom_folder): 
        if filename.lower().endswith('.dcm'):
            
            file_path = os.path.join(dicom_folder, filename)
            dicom_file = pydicom.dcmread(file_path)

            # Check if the required attributes are present
            patient_age=dicom_file.get('PatientAge',None)
            patient_sex=dicom_file.get('PatientSex',None)
            #FDG_acq_date=dicom_file.get('StudyDate',None)
            break'''
    data_list.append({
            'PID': pid,
            'Occipital': OCC_ROI.mean()/mean-1,
            'LAP':LAP_ROI[LAP_ROI>0].mean()/mean-1,
            'LPP':LPP_ROI[LPP_ROI>0].mean()/mean-1,
            'LAC':LAC_ROI[LAC_ROI>0].mean()/mean-1,
            'LPC':LPC_ROI[LPC_ROI>0].mean()/mean-1,
            'RAP':RAP_ROI[RAP_ROI>0].mean()/mean-1, 
            'RPP':RPP_ROI[RPP_ROI>0].mean()/mean-1,
            'RAC':RAC_ROI[RAC_ROI>0].mean()/mean-1,
            'RPC':RPC_ROI[RPC_ROI>0].mean()/mean-1,
            'LVS':LVS_ROI[LVS_ROI>0].mean()/mean-1,
            'RVS':RVS_ROI[RVS_ROI>0].mean()/mean-1,
            'LVP':LVP_ROI[LVP_ROI>0].mean()/mean-1,
            'RVP':RVP_ROI[RVP_ROI>0].mean()/mean-1
            
            })  
    
    

df = pd.DataFrame(data_list)
excel_file = 'Bpnd_Delay.xlsx'
print(df)
df.to_excel(excel_file, index=False)