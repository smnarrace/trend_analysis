
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
import google.generativeai as genai

# 💡 여기에 발급받은 API 키를 따옴표 안에 꼭! 붙여넣어 주세요!
GEMINI_API_KEY = "AIzaSyB3fFBrWapzWd7xPS77rlm4PgjMFXOBsbs" 
genai.configure(api_key=GEMINI_API_KEY)

def analyze_csv_to_report(input_file="webnovel_raw.csv", output_file="trend_report.csv"):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("❌ 에러: webnovel_raw.csv 파일이 없습니다.")
        return

    print("⚙️ [1/2] 기존 방식: 핵심 키워드 30개를 뽑는 중입니다...")
    okt = Okt()
    all_nouns = []
    stop_words = ['웹툰', '소설', '무료', '결제', '보기', '연재', '에피소드', '더보기', '단행본', '웹소설', '플러스', '독점', '판타지', '웹툰판']
    
    for title in df['title']:
        nouns = [n for n in okt.nouns(str(title)) if len(n) > 1]
        for noun in nouns:
            if noun not in stop_words:
                all_nouns.append(noun)

    counts = Counter(all_nouns)
    report_df = pd.DataFrame(counts.most_common(30), columns=['keyword', 'count'])
    report_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print("🤖 [2/2] Gemini AI 셰프 출동! 1,600개 제목의 숨은 트렌드를 분석합니다...")
    # 💡 1,600개 제목을 하나의 거대한 텍스트로 합쳐서 AI에게 던져줍니다!
    all_titles_text = "\n".join(df['title'].astype(str).tolist())
    
    prompt = f"""
    너는 웹소설과 웹툰 트렌드를 꿰뚫어보는 10년 차 수석 데이터 분석가야.
    아래에 네이버, 카카오, 문피아에서 방금 긁어온 최신 인기작 제목 리스트 1,600개를 줄게.
    이 제목들을 싹 분석해서, 현재 독자들이 열광하는 '장르, 핵심 소재, 전개 트렌드'를 딱 3~4줄로 멋지게 요약해 줘.
    말투는 전문가처럼, 핵심만 짚어서 출력해. (예: "최근에는 '악녀 빙의'와 '전문직 회귀' 소재가 강세입니다...")

    [제목 리스트]
    {all_titles_text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # AI가 써준 멋진 리포트를 텍스트 파일로 저장합니다.
        with open("ai_summary.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("\n🎉 AI 분석 완료! [ai_summary.txt] 리포트가 생성되었습니다.")
        print(f"👉 AI 요약 미리보기: \n{response.text}")
    except Exception as e:
        print(f"\n❌ AI 분석 중 에러 발생 (API 키를 확인하세요!): {e}")

if __name__ == "__main__":
    analyze_csv_to_report()