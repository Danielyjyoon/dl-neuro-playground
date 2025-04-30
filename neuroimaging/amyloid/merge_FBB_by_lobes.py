import pandas as pd

# ✅ Lobe Group Define (1000: Lt, 2000: Rt)
lobe_MRX_ROI = {
    "Frontal_Lt": [1003, 1012, 1014, 1018, 1019, 1020, 1027, 1028],
    "Frontal_Rt": [2003, 2012, 2014, 2018, 2019, 2020, 2027, 2028],
    "Parietal_Lt": [1008, 1025, 1029, 1031],
    "Parietal_Rt": [2008, 2025, 2029, 2031],
    "Lateral_Temporal_Lt": [1009, 1015, 1030],
    "Lateral_Temporal_Rt": [2009, 2015, 2030],
    "Anterior_Cingulate_Lt": [1002, 1026],
    "Anterior_Cingulate_Rt": [2002, 2026],
    "Posterior_Cingulate_Lt": [1010, 1023],
    "Posterior_Cingulate_Rt": [2010, 2023]
}

# ✅ WC ROIs (7,8,46,47)
WC_ROI = [7, 8, 46, 47]

# ✅ Whole ROI list (WC + All MRX_ROI)
all_ROIs = WC_ROI + [roi for sublist in lobe_MRX_ROI.values() for roi in sublist]

def process_excel(file_path, output_file):
    # ✅ CSV read
    df = pd.read_csv(file_path)

    # ✅ Check required columns
    required_columns = {"no.", "ROI_intensity_sum", "ROI_cnt"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV 파일에 {required_columns} 컬럼이 있어야 합니다.")

    # ✅ WC ROI 처리
    df_WC = df[df["no."].isin(WC_ROI)]
    WC_intensity_sum = df_WC["ROI_intensity_sum"].sum()
    WC_cnt_sum = df_WC["ROI_cnt"].sum()
    ROI_average_WC = WC_intensity_sum / WC_cnt_sum if WC_cnt_sum > 0 else None

    # ✅ MRX ROI 처리 (lobe별로)
    lobe_results = []
    for lobe, roi_list in lobe_MRX_ROI.items():
        df_lobe = df[df["no."].isin(roi_list)]
        lobe_intensity_sum = df_lobe["ROI_intensity_sum"].sum()
        lobe_cnt_sum = df_lobe["ROI_cnt"].sum()
        ROI_average_lobe = lobe_intensity_sum / lobe_cnt_sum if lobe_cnt_sum > 0 else None

        lobe_results.append({
            "Lobe": lobe,
            "ROI_intensity_sum": lobe_intensity_sum,
            "ROI_cnt_sum": lobe_cnt_sum,
            "ROI_average": ROI_average_lobe
        })

    # ✅ WC 결과도 같은 리스트에 추가
    lobe_results.append({
        "Lobe": "WC",
        "ROI_intensity_sum": WC_intensity_sum,
        "ROI_cnt_sum": WC_cnt_sum,
        "ROI_average": ROI_average_WC
    })

    # ✅ 결과 데이터프레임 생성 (WC와 Lobe ROI 결과 통합)
    df_results = pd.DataFrame(lobe_results)

    # ✅ 요청된 모든 ROI 값들만 필터링한 데이터프레임 생성
    df_filtered = df[df["no."].isin(all_ROIs)]

    # ✅ openpyxl 엔진을 사용하여 엑셀 파일로 저장 (두 개의 시트)
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_results.to_excel(writer, sheet_name="Lobe_ROI_Results", index=False)  # Lobe ROI + WC 결과
        df_filtered.to_excel(writer, sheet_name="Filtered_ROI_Results", index=False)  # 필터링된 ROI 값

    print(f"처리된 데이터가 '{output_file}' 파일로 저장되었습니다.")

# ✅ 사용 예시
file_path = "/nas/yj/centiloid/2025/new_list/2578139_CT/RAW_Parc_2578139_manual.csv"  # 입력할 CSV 파일 경로
output_file = "/nas/yj/centiloid/2025/new_list/2578139_CT/RAW_Parc_2578139_manual_processed_results.xlsx"  # 저장할 엑셀 파일 이름
process_excel(file_path, output_file)
