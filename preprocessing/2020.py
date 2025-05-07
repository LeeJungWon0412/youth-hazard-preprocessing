import pandas as pd

# 엑셀 파일 불러오기
df = pd.read_excel("2020년 청소년 매체이용 및 유해환경 실태조사(데이터).xlsx", na_values=["#NULL!", "#N/A", ""])

# 항목별 문항코드
categories = {
    "성인물": ["YM02", "YM03"],
    "도박": ["YM0502"],
    "폭력": ["YM1101", "YM1102", "YM1103", "YM1104", "YM1105", "YM1106", "YM1107"],
    "성폭력": ["YM1501", "YM1502", "YM1503", "YM1504", "YM1505", "YM1506", "YM1507"],
    "가출": ["YM21"],
    "음주": ["YM26"],
    "흡연": ["YM28", "YM30"],
    "약물": ["YM32"],
    "유해업소": ["YM3401", "YM3402", "YM3403", "YM3404", "YM3405", "YM3406", "YM3407",
              "YM3501", "YM3502", "YM3503", "YM3504", "YM3505"]
}

# 지역 코드 → 한글 매핑
region_map = {
    1: "서울", 2: "부산", 3: "대구", 4: "인천", 5: "광주", 6: "대전", 7: "울산", 8: "세종",
    9: "경기", 10: "강원", 11: "충북", 12: "충남", 13: "전북", 14: "전남", 15: "경북", 16: "경남", 17: "제주"
}

# DM7 정제 (1~17만 남기고 정수형 변환)
df = df[df["DM7"].isin(region_map.keys())].copy()
df["DM7"] = df["DM7"].astype(int)

# 특정 카테고리 응답 수 세는 함수
def count_yes(df_region, codes):
    if codes[0] == "YM21":
        return df_region[codes[0]].isin([2, 3, 4, 5]).sum()
    return (df_region[codes] == 1).any(axis=1).sum()

# 결과 저장 리스트
rows = []

for cat, codes in categories.items():
    for code, name in region_map.items():
        region_df = df[df["DM7"] == code]
        total = len(region_df)
        yes = count_yes(region_df, codes)

        rows.append({
            "종목": cat,
            "지역": name,
            "전체_응답자수": total,
            "있다고_응답한수": yes
        })

# 표로 만들고 CSV 저장
pd.DataFrame(rows).to_csv("2020_유해환경_정리.csv", index=False, encoding="utf-8-sig")
