import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영차! 트렌드 분석", layout="wide")

st.title("📊 문피아·네이버·카카오 통합 키워드 트렌드")
st.markdown("현재 가장 핫한 웹툰/웹소설 키워드를 한눈에 확인하세요.")

try:
    try:
        with open("ai_summary.txt", "r", encoding="utf-8") as f:
            ai_text = f.read()
        st.info(f"🤖 **Gemini AI 트렌드 요약 리포트**\n\n{ai_text}")
    except FileNotFoundError:
        pass
    # 💡 [핵심] 무겁게 직접 긁어오지 않고, 터미널에서 미리 만들어둔 완성본을 읽기만 합니다!
    df = pd.read_csv("trend_report.csv")
    
    st.success("🎉 통합 데이터를 성공적으로 불러왔습니다! 영차!")
    
    col1, col2 = st.columns(2)
    col1.metric("오늘의 1위 키워드 🏆", df['keyword'].iloc[0])
    col2.metric("분석된 핵심 키워드 수", f"{len(df)}개")

    st.subheader("🔥 실시간 통합 키워드 순위")
    fig = px.bar(df, x='count', y='keyword', orientation='h', 
                 color='count', color_continuous_scale='Viridis',
                 text_auto=True) # 막대그래프에 숫자도 표시해 줍니다!
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("전체 데이터 표 자세히 보기"):
        st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error("아직 데이터가 없습니다. 터미널에서 요리사(`python3 analyzer.py`)를 먼저 실행해주세요!")