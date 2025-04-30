import os
import pandas as pd
from tqdm import tqdm
import pickle
import numpy as np
import nibabel as nib

##전체 ROI를 Pons혹은 weighted average로 merge하는 코드
# 경로 설정
base = '/nas/seungbeom/FDGFBB_res_NC'

# 모든 결과 저장용 리스트
rows = []
pids = os.listdir(base)

# 모든 PID 폴더 순회
for pid in tqdm(pids, total=len(pids)):
    FILE_DIR = os.path.join(base, pid)

    # ROI 데이터 CSV 경로 확인
    file_CSV_ROI = os.path.join(FILE_DIR, 'RAW_Parc_MR_FDG.csv')

    #1. Weighted average만 구하거나
    if os.path.exists(file_CSV_ROI):
        raw_data = pd.read_csv(file_CSV_ROI)
        weighted_average = (raw_data['ROI_intensity_sum']).sum() / raw_data['ROI_cnt'].sum()
        series = pd.Series(data=raw_data['ROI_average'].values/weighted_average, index=raw_data['no.'].values).to_dict()
        row = {k: v for k, v in series.items()}  # series의 내용 복사
        row['pid'] = pid
        rows.append(row)

    #2. Pons average 구하거나
    if os.path.exists(file_CSV_ROI) and os.path.exists(os.path.join(FILE_DIR, 'Brainstem.nii')):
        raw_data = pd.read_csv(file_CSV_ROI)
        # 기준 ROI (174) 평균 강도 값 가져오기
        if 174 in raw_data['no.'].values:
            value_174 = raw_data.loc[raw_data['no.'] == 174, 'ROI_average'].values[0]
        else:
            ##Brainstem.nii, FDG.nii로 새로 계산
            orig_mask_path=os.path.join(FILE_DIR, 'Brainstem.nii')
            file_FDG = os.path.join(FILE_DIR, 'FDG.nii')     
            if not os.path.exists(orig_mask_path) or not os.path.exists(file_FDG):
                print(f"PID {pid}: Missing necessary files (Brainstem.nii or FDG.nii). Skipping.")
                continue  

            orig_mask_load=nib.load(orig_mask_path)
            orig_mask=orig_mask_load.get_fdata()
            newmask = np.in1d(orig_mask, [174]).reshape(256, 256, 256).astype(float)
            FDG=nib.load(file_FDG).get_fdata()
            ROI=np.multiply(FDG,newmask)
            ROI=ROI[ROI>0]
            if len(ROI) > 0:
                value_174 = ROI.mean()    
            else:
                print(f"PID {pid}: No valid ROI 174 values found in FDG.nii. Skipping Pons average calculation.")
                continue

        if value_174 > 0:  # Division by zero 방지
            series = (raw_data['ROI_average'] / value_174).to_dict()
            row = {k: v for k, v in series.items()}
            row['pid'] = pid
            row['method'] = 'Pons'
            rows.append(row)
        else:
            print(f"PID {pid}: Invalid Pons reference value (zero or negative). Skipping.")


# 결과 데이터프레임 생성 및 저장
df_med = pd.DataFrame(rows).fillna(0)
output_path = '/nas/seungbeom/FDGFBBres_FDG_NC.xlsx'
df_med.to_excel(output_path, index=False)

print(f"Results saved to {output_path}")

# label2region = {
#     0: "Unknown",
#     2: "Left-Cerebral-White-Matter",
#     4: "Left-Lateral-Ventricle",
#     5: "Left-Inf-Lat-Vent",
#     7: "Left-Cerebellum-White-Matter",
#     8: "Left-Cerebellum-Cortex",
#     9: "Left-Thalamus",
#     10: "Left-Thalamus-Proper",
#     11: "Left-Caudate",
#     12: "Left-Putamen",
#     13: "Left-Pallidum",
#     14: "3rd-Ventricle",
#     15: "4th-Ventricle",
#     16: "Brain-Stem",
#     17: "Left-Hippocampus",
#     18: "Left-Amygdala",
#     24: "CSF",
#     26: "Left-Accumbens-area",
#     27: "Left-Substancia-Nigra",
#     28: "Left-VentralDC",
#     29: "Left-undetermined",
#     30: "Left-vessel",
#     31: "Left-choroid-plexus",
#     32: "Left-F3orb",
#     41: "Right-Cerebral-White-Matter",
#     42: "Right-Cerebral-Cortex",
#     43: "Right-Lateral-Ventricle",
#     44: "Right-Inf-Lat-Vent",
#     45: "Right-Cerebellum-Exterior",
#     46: "Right-Cerebellum-White-Matter",
#     47: "Right-Cerebellum-Cortex",
#     48: "Right-Thalamus",
#     49: "Right-Thalamus-Proper",
#     50: "Right-Caudate",
#     51: "Right-Putamen",
#     52: "Right-Pallidum",
#     53: "Right-Hippocampus",
#     54: "Right-Amygdala",
#     55: "Right-Insula",
#     56: "Right-Operculum",
#     57: "Right-Lesion",
#     58: "Right-Accumbens-area",
#     59: "Right-Substancia-Nigra",
#     60: "Right-VentralDC",
#     61: "Right-undetermined",
#     62: "Right-vessel",
#     63: "Right-choroid-plexus",
#     72: "5th-Ventricle",
#     77: "WM-hypointensities",
#     78: "Left-WM-hypointensities",
#     79: "Right-WM-hypointensities",
#     80: "non-WM-hypointensities",
#     81: "Left-non-WM-hypointensities",
#     82: "Right-non-WM-hypointensities",
#     83: "Left-F1",
#     84: "Right-F1",
#     85: "Optic-Chiasm",
#     192: "Corpus_Callosum",
#     251: "CC_Posterior",
#     252: "CC_Mid_Posterior",
#     253: "CC_Central",
#     254: "CC_Mid_Anterior",
#     255: "CC_Anterior",
#     1000: "ctx-lh-unknown",
#     1001: "ctx-lh-bankssts",
#     1002: "ctx-lh-caudalanteriorcingulate",
#     1003: "ctx-lh-caudalmiddlefrontal",
#     1004: "ctx-lh-corpuscallosum",
#     1005: "ctx-lh-cuneus",
#     1006: "ctx-lh-entorhinal",
#     1007: "ctx-lh-fusiform",
#     1008: "ctx-lh-inferiorparietal",
#     1009: "ctx-lh-inferiortemporal",
#     1010: "ctx-lh-isthmuscingulate",
#     1011: "ctx-lh-lateraloccipital",
#     1012: "ctx-lh-lateralorbitofrontal",
#     1013: "ctx-lh-lingual",
#     1014: "ctx-lh-medialorbitofrontal",
#     1015: "ctx-lh-middletemporal",
#     1016: "ctx-lh-parahippocampal",
#     1017: "ctx-lh-paracentral",
#     1018: "ctx-lh-parsopercularis",
#     1019: "ctx-lh-parsorbitalis",
#     1020: "ctx-lh-parstriangularis",
#     1021: "ctx-lh-pericalcarine",
#     1022: "ctx-lh-postcentral",
#     1023: "ctx-lh-posteriorcingulate",
#     1024: "ctx-lh-precentral",
#     1025: "ctx-lh-precuneus",
#     1026: "ctx-lh-rostralanteriorcingulate",
#     1027: "ctx-lh-rostralmiddlefrontal",
#     1028: "ctx-lh-superiorfrontal",
#     1029: "ctx-lh-superiorparietal",
#     1030: "ctx-lh-superiortemporal",
#     1031: "ctx-lh-supramarginal",
#     1032: "ctx-lh-frontalpole",
#     1033: "ctx-lh-temporalpole",
#     1034: "ctx-lh-transversetemporal",
#     1035: "ctx-lh-insula",
#     2000: "ctx-rh-unknown",
#     2001: "ctx-rh-bankssts",
#     2002: "ctx-rh-caudalanteriorcingulate",
#     2003: "ctx-rh-caudalmiddlefrontal",
#     2004: "ctx-rh-corpuscallosum",
#     2005: "ctx-rh-cuneus",
#     2006: "ctx-rh-entorhinal",
#     2007: "ctx-rh-fusiform",
#     2008: "ctx-rh-inferiorparietal",
#     2009: "ctx-rh-inferiortemporal",
#     2010: "ctx-rh-isthmuscingulate",
#     2011: "ctx-rh-lateraloccipital",
#     2012: "ctx-rh-lateralorbitofrontal",
#     2013: "ctx-rh-lingual",
#     2014: "ctx-rh-medialorbitofrontal",
#     2015: "ctx-rh-middletemporal",
#     2016: "ctx-rh-parahippocampal",
#     2017: "ctx-rh-paracentral",
#     2018: "ctx-rh-parsopercularis",
#     2019: "ctx-rh-parsorbitalis",
#     2020: "ctx-rh-parstriangularis",
#     2021: "ctx-rh-pericalcarine",
#     2022: "ctx-rh-postcentral",
#     2023: "ctx-rh-posteriorcingulate",
#     2024: "ctx-rh-precentral",
#     2025: "ctx-rh-precuneus",
#     2026: "ctx-rh-rostralanteriorcingulate",
#     2027: "ctx-rh-rostralmiddlefrontal",
#     2028: "ctx-rh-superiorfrontal",
#     2029: "ctx-rh-superiorparietal",
#     2030: "ctx-rh-superiortemporal",
#     2031: "ctx-rh-supramarginal",
#     2032: "ctx-rh-frontalpole",
#     2033: "ctx-rh-temporalpole",
#     2034: "ctx-rh-transversetemporal",
#     2035: "ctx-rh-insula"
# }