import streamlit as st
import pandas as pd
import plotly.express as px # pip install plotly 추천

st.set_page_config(page_title="콘텐츠 트렌드 분석", layout="wide")

st.title("🚀 웹툰/웹소설 키워드 트렌드")
st.sidebar.header("설정")

# 데이터 불러오기
try:
    df = pd.read_csv("trend_report.csv")
    
    # 상단 지표 (Metric)
    col1, col2 = st.columns(2)
    col1.metric("최고 인기 키워드", df['keyword'].iloc[0])
    col2.metric("분석된 키워드 수", len(df))

    # 메인 차트
    st.subheader("🔥 실시간 키워드 빈도수")
    fig = px.bar(df, x='keyword', y='count', 
                 color='count', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

    # 상세 데이터 표
    if st.checkbox("전체 데이터 보기"):
        st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error("분석 결과 파일(trend_report.csv)이 없습니다. analyzer.py를 먼저 실행해주세요!")