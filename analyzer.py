import pandas as pd
from konlpy.tag import Okt
from collections import Counter

def analyze_csv_to_report(input_file="webnovel_raw.csv", output_file="trend_report.csv"):
    try:
        # CSV 읽기
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("수집된 데이터 파일이 없습니다.")
        return

    okt = Okt()
    all_nouns = []
    
    for title in df['title']:
        # 2글자 이상의 명사만 추출
        nouns = [n for n in okt.nouns(str(title)) if len(n) > 1]
        all_nouns.extend(nouns)

    # 빈도수 계산 후 데이터프레임 변환
    counts = Counter(all_nouns)
    report_df = pd.DataFrame(counts.most_common(20), columns=['keyword', 'count'])
    
    # 분석 결과 저장
    report_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"분석 완료: {output_file} (상위 20개 키워드)")
    print(report_df.head(10)) # 터미널에서도 확인

if __name__ == "__main__":
    analyze_csv_to_report()