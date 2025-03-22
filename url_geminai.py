from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 네이버 플레이스 리뷰 URL
url = "https://pcmap.place.naver.com/restaurant/21306384/review/visitor"

# Selenium WebDriver 설정
options = Options()
options.add_argument("--headless")  # 창 없이 실행 (옵션)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 웹드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

# 페이지 로드 대기
wait = WebDriverWait(driver, 10)
time.sleep(3)  # 기본 대기

# 스크롤을 내려서 리뷰 더 불러오기
try:
    # 리뷰 요소가 로드될 때까지 대기
    review_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".YeOkE"))) # 리뷰 클래스 찾기

    # 모든 리뷰가 로드될 때까지 스크롤
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 스크롤 후 로딩 대기
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

    # 리뷰 요소 다시 찾기
    review_elements = driver.find_elements(By.CSS_SELECTOR, ".YeOkE")
    review_list = [review.text.strip() for review in review_elements]

    # 리뷰 출력
    for i, review in enumerate(review_list, 1):
        print(f"{i}. {review}")

except Exception as e:
    print("리뷰를 가져오는 데 실패했습니다:", e)

# 드라이버 종료
driver.quit()