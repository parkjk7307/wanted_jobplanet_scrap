# **공고제목 - title**
# **회사이름 - company_name**
# **디테일 페이지로 가는 주소 - detail_url **
# **마감일 - end_date**
# ** 참고한 플랫폼 이름 - platform_name**

# scraping.py

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def scrape_jobs():
    ##### 마우스 이벤트 시작 #####

    # 웹 드라이버 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.jobplanet.co.kr/welcome/index/")
    driver.implicitly_wait(5)

    # 채용 버튼 클릭
    button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "job_posting"))
    )
    ActionChains(driver).click(button).perform()

    # 직종 버튼 클릭
    job_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '직종')]"))
    )
    ActionChains(driver).click(job_button).perform()

    # 데이터 버튼 클릭
    data_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='데이터']"))
    )
    ActionChains(driver).click(data_button).perform()

    # 데이터 엔지니어 체크박스 버튼 클릭
    engineer_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='데이터 엔지니어']"))
    )
    ActionChains(driver).click(engineer_button).perform()

    # 적용 버튼 클릭
    apply_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='적용']"))
    )
    ActionChains(driver).click(apply_button).perform()

    ##### 마우스 이벤트 종료 #####

    ##### 스크랩 시작 #####

    # 페이지가 완전히 로드될 때까지 잠시 대기
    time.sleep(10)

    # 스크롤을 일정 횟수만큼 수행 (예: 5번)
    scroll_pause_time = 1
    scroll_limit = 5

    for _ in range(scroll_limit):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

    # BeautifulSoup으로 페이지 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 1. a 태그에서 href 속성을 추출
    links = soup.find_all("a", "group z-0 block medium", title="페이지 이동")

    # 2. 공고 정보 추출
    job_elements = soup.find_all("div", "group mt-[16px] group-[.small]:mt-[14px] medium")

    # 3. 결과를 저장할 리스트
    jobs_data = []

    # 4. 링크와 공고 정보를 함께 저장
    for job, link in zip(job_elements, links):
        job_data = {}

        # 제목 (h2 태그 사용)
        title = job.find("h2", "line-clamp-2 break-all text-h7 text-gray-800 group-[.small]:text-h8")
        if title:
            job_data["title"] = title.get_text(strip=True)

        # 회사명 (em 태그 사용)
        company_name = job.find("em", "inline-block w-full truncate text-body2 font-medium text-gray-800")
        if company_name:
            job_data["company_name"] = company_name.get_text(strip=True)

        # 기술 스택 (span 태그 사용)
        skills = job.find("span", "mt-[6px] inline-block w-full truncate text-small1 text-gray-500")
        if skills:
            job_data["skills"] = skills.get_text(strip=True)

        # 링크 (a 태그에서 href 속성 추출)
        job_data["detail_url"] = link.get("href")

        # 마감일 (임의로 상시 채용으로 설정)
        job_data["end_date"] = "상시 채용"

        # 플랫폼 이름
        job_data["platform_name"] = "Jobplanet"

        # 저장된 공고 데이터를 리스트에 추가
        jobs_data.append(job_data)

    # 브라우저 종료
    driver.quit()

    return jobs_data
