import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_to_csv(filename="webnovel_raw.csv"):
    url = "https://www.munpia.com/page/best/section/real"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 제목 데이터 추출
    titles = [t.get_text(strip=True) for t in soup.select('.title > a')]
    
    # 데이터프레임 생성 (수집 시간 추가)
    df = pd.DataFrame({
        'title': titles,
        'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # CSV 저장 (utf-8-sig: 엑셀에서 한글 안 깨지게 하는 옵션)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"저장 완료: {filename} (총 {len(df)}건)")

if __name__ == "__main__":
    scrape_to_csv()