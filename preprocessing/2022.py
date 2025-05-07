import pandas as pd

# 파일 경로 및 csv 파일 불러오기
data_path = "2022년 청소년 매체이용 및 유해환경 실태조사(데이터).csv"
df = pd.read_csv(data_path, encoding="cp949", na_values=["#NULL!", "#N/A", ""])

# 컬럼명을 문자열로 통일
df.columns = df.columns.astype(str)

# 지역 코드 정제 및 변환
df = df[df["372"].isin([str(i) for i in range(1, 18)])].copy()
df["372"] = df["372"].astype(int)

# 지역 코드 → 한글 매핑
region_map = {
    1: "서울", 2: "부산", 3: "대구", 4: "인천", 5: "광주", 6: "대전", 7: "울산", 8: "세종",
    9: "경기", 10: "강원", 11: "충북", 12: "충남", 13: "전북", 14: "전남", 15: "경북", 16: "경남", 17: "제주"
}

# 항목별 문항코드
categories = {
    "성인물": ["26", "41"],
    "도박": ["70"],
    "폭력": ["91", "92", "93", "94", "95", "96", "97", "98", "99", "100"],
    "성폭력": ["118", "119", "120", "121", "122", "123", "124", "125"],
    "가출": ["156"],
    "음주": ["175"],
    "흡연": ["195"],
    "약물": ["231", "234"],
    "유해업소": ["246", "247", "248", "249", "250", "251", "252", "263", "265", "267", "269", "271", "273"]
}

# 응답 값 판단 함수
def is_yes(val):
    try:
        return int(float(val)) == 1
    except:
        return False

# 특정 종목 응답자 수 세는 함수
def count_yes(df_region, codes):
    return df_region[codes].apply(lambda row: any(is_yes(val) for val in row), axis=1).sum()

# 결과 저장 리스트
rows = []

for cat, codes in categories.items():
    for code, name in region_map.items():
        region_df = df[df["372"] == code]
        total = len(region_df)
        yes = count_yes(region_df, codes)

        rows.append({
            "종목": cat,
            "지역": name,
            "전체_응답자수": total,
            "있다고_응답한수": yes
        })

# 표로 만들고 CSV 저장
pd.DataFrame(rows).to_csv("2022_유해환경_정리.csv", index=False, encoding="utf-8-sig")
