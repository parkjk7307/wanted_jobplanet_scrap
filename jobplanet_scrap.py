# **공고제목 - title**
# **회사이름 - company_name**
# **디테일 페이지로 가는 주소 - detail_url **
# **마감일 - end_date**
# ** 참고한 플랫폼 이름 - platform_name**
# ** 카테고리 - category_name**
# ** 기술 스택 - stack **
# ** 지역  - region **
# ** 신입/경력 - career **

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# 추가 정보를 스크래핑하는 함수
def scrape_additional_info(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(3)  # 페이지 로딩 대기
    
    # BeautifulSoup으로 페이지 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 마감일 추출 (end_date)
    end_date_element = soup.find("span", class_="recruitment-summary__end")
    end_date = None
    if end_date_element:
        end_date = end_date_element.get_text(strip=True)
    
    # 경력 추출 (career)
    career_element = None
    for dt in soup.find_all("dt", class_="recruitment-summary__dt"):
        if "경력" in dt.get_text(strip=True):
            career_element = dt.find_next_sibling("dd")
            break
    career = None
    if career_element:
        career = career_element.get_text(strip=True)

    # 지역 추출 (region)
    region_element = soup.find("span", class_="recruitment-summary__location")
    region = None
    if region_element:
        region = region_element.get_text(strip=True)

    # 기술 스택 추출 (stack)
    stack_element = None
    for dt in soup.find_all("dt", class_="recruitment-summary__dt"):
        if "스킬" in dt.get_text(strip=True):
            stack_element = dt.find_next_sibling("dd")
            break
    stack = []
    if stack_element:
        stack = [tech.strip() for tech in stack_element.get_text(strip=True).split(",")]

    driver.quit()

    return {
        "end_date": end_date,
        "career": career,
        "region": region,
        "stack": stack
    }



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

# 데이터 전체 버튼 클릭
engineer_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='데이터 전체']"))
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
scroll_limit = 1

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

# 4. 멀티스레딩으로 각 공고의 추가 정보를 병렬로 스크래핑
def process_job(job, link):
    # 각 공고 정보를 저장할 딕셔너리
    job_data = {}
    
    # 제목 (h2 태그 사용)
    title = job.find("h2", "line-clamp-2 break-all text-h7 text-gray-800 group-[.small]:text-h8")
    if title:
        job_data["title"] = title.get_text(strip=True)

    # 회사명 (em 태그 사용)
    company_name = job.find("em", "inline-block w-full truncate text-body2 font-medium text-gray-800")
    if company_name:
        job_data["company_name"] = company_name.get_text(strip=True)

    # 링크 (a 태그에서 href 속성 추출)
    job_data["detail_url"] = link.get("href")

    # 플랫폼 이름
    job_data["platform_name"] = "Jobplanet"

    # 추가 정보를 병렬로 가져오기
    additional_info = scrape_additional_info(job_data["detail_url"])
    job_data["stack"] = additional_info["stack"]
    job_data["career"] = additional_info["career"]
    job_data["region"] = additional_info["region"]
    job_data["end_date"] = additional_info["end_date"]

    return job_data

# 스레드 풀을 사용하여 병렬 처리 (성능향상...)
with ThreadPoolExecutor(max_workers=7) as executor:
    futures = [executor.submit(process_job, job, link) for job, link in zip(job_elements, links)]
    for future in as_completed(futures):
        jobs_data.append(future.result())

# 결과 출력 (예시)
for job in jobs_data:
    print(job)

# 5. 브라우저 종료
driver.quit()
