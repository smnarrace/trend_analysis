from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def setup_driver():
    options = Options()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_argument('--window-size=1920,1080')
    options.binary_location = '/usr/bin/google-chrome'
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_munpia(driver):
    driver.get("https://www.munpia.com/page/best/section/real")
    time.sleep(4) 
    
    # 💡 [엑스레이] 지금 봇이 무슨 화면을 보고 있는지 확인!
    print(f"   [X-Ray] 문피아 화면 제목: {driver.title}") 
    
    titles_set = set()
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 💡 [투망 던지기] 클래스명 무시하고 모든 <a> 태그의 글씨를 다 긁어옵니다!
        for a in soup.find_all('a'):
            text = a.get_text(strip=True)
            if len(text) > 3 and '@' not in text: # 4글자 이상만 담기
                titles_set.add(text)
    return list(titles_set)

def get_naver(driver):
    driver.get("https://comic.naver.com/webtoon")
    time.sleep(3) 
    print(f"   [X-Ray] 네이버 화면 제목: {driver.title}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    titles = [t.get_text(strip=True) for t in soup.select('.ContentTitle__title--e3qXt')]
    if not titles:
        titles = [t.get_text(strip=True) for t in soup.find_all('span', class_='title')]
    return titles

def get_kakao(driver):
    driver.get("https://page.kakao.com/menu/10011/screen/94")
    time.sleep(5) 
    
    print(f"   [X-Ray] 카카오 화면 제목: {driver.title}")
    
    titles_set = set()
    for _ in range(8):
        driver.execute_script("window.scrollBy(0, 800);") 
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 💡 [투망 던지기] <span>과 <div>에 있는 모든 글씨를 무식하게 다 긁어옵니다!
        for tag in soup.find_all(['span', 'div']):
            text = tag.get_text(strip=True)
            if len(text) > 4: # 5글자 이상만 담기
                titles_set.add(text)
    return list(titles_set)

def scrape_all_to_csv(filename="webnovel_raw.csv"):
    print("🚀 무식한 투망 크롤러 출동!")
    driver = setup_driver()
    all_data = []
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    platforms = {'Munpia': get_munpia, 'Naver': get_naver, 'Kakao': get_kakao}

    try:
        for name, func in platforms.items():
            print(f"\n[{name} 수집 시작]")
            try:
                titles = func(driver)
                print(f"-> {name} 데이터 {len(titles)}건 확보!")
                for title in titles:
                    all_data.append([current_time, name, title])
            except Exception as e:
                print(f"-> 에러: {e}")
    finally:
        driver.quit() 

    df = pd.DataFrame(all_data, columns=['collected_at', 'platform', 'title'])
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n--- 🎉 엑셀 저장 완료: {filename} (총 {len(df)}건) ---")

if __name__ == "__main__":
    scrape_all_to_csv()