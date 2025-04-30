import os
import pandas as pd
from tqdm import tqdm
import pickle

##관심있는 ROI만 merge, weighted average구하는 코드
# 경로 및 파일 설정
base = r"C:\Users\byeby\Desktop\test\sb_LBD\Revision\sb_dcm_download"
suvr_csv = r"C:\Users\byeby\Desktop\test\sb_LBD\Revision\SUVR_hypo.xlsx"

FDG_list=[1005, 1007, 1008, 1009, 1011, 1013, 1021, 2005, 2007, 2008, 2009, 2011, 2013, 2021]

rows=[]
pids = os.listdir(base)
for pid in tqdm(pids, desc="Processing PIDs"):
    FILE_DIR = os.path.join(base, pid)
    file_CSV_ROI = os.path.join(FILE_DIR, 'RAW_Parc_MR_Early.csv')

    # ROI CSV 파일이 존재하는 경우만 처리
    if os.path.exists(file_CSV_ROI):
        # CSV 파일 읽기
        raw_data = pd.read_csv(file_CSV_ROI)
        raw_data=raw_data.iloc[1:]
        # 전체 Total_weighted_average 계산
        total_intensity_sum = raw_data['ROI_intensity_sum'].sum()
        total_count_sum = raw_data['ROI_cnt'].sum()
        if total_count_sum > 0:
            total_weighted_average = total_intensity_sum / total_count_sum
        else:
            total_weighted_average = 0  # Division by zero 방지

        # 관심 있는 ROI만 필터링
        filtered_df = raw_data[raw_data['no.'].isin(FDG_list)]
        filtered_intensity_sum = filtered_df['ROI_intensity_sum'].sum()
        filtered_count_sum = filtered_df['ROI_cnt'].sum()
        if filtered_count_sum > 0:
            filtered_weighted_average = filtered_intensity_sum / filtered_count_sum
        else:
            filtered_weighted_average = 0  # Division by zero 방지

        # 관심 있는 부분의 weighted average를 Total_weighted_average로 나눈 값 계산
        if total_weighted_average > 0:
            normalized_weighted_average = filtered_weighted_average / total_weighted_average
        else:
            normalized_weighted_average = 0  # Division by zero 방지

        # 결과 저장
        rows.append({
            'pid': pid,
            'Total_weighted_average': total_weighted_average,
            'Filtered_weighted_average': filtered_weighted_average,
            'Normalized_weighted_average': normalized_weighted_average
        })

result_df = pd.DataFrame(rows)

# 결과 저장
result_df.to_excel(suvr_csv, index=False)

print(f"Total weighted averages saved to {suvr_csv}")

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


