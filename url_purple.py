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

# 크롬 옵션 최적화
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# 웹드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
})

try:
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    
    # 프레임 전환 (필요 시)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#entryIframe")))
    
    # 리뷰 영역 로딩 대기
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.fvCOw')))
    
    # 스크롤 다운 처리 (최대 20회 시도)
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # 리뷰 요소 수집
    reviews = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'li.YeINN div.ZZ4OK > a span.zPfVt')
    ))
    
    # 결과 추출
    review_list = [review.text.strip() for review in reviews if review.text.strip()]
    
    # 리뷰 출력
    for idx, review in enumerate(review_list, 1):
        print(f"[{idx}] {review}")
        
except Exception as e:
    print(f"에러 발생: {str(e)}")
finally:
    driver.quit()
