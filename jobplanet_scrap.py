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

    # 기술 스택 추출
    stack_elements = soup.find_all("dd", class_="recruitment-summary__dd")
    stack = [el.get_text(strip=True) for el in stack_elements]
    
    # 경력 추출
    career = None
    career_element = soup.find("dd", class_="recruitment-summary__dd")
    if career_element:
        career = career_element.get_text(strip=True)

    # 지역 추출
    region = None
    region_element = soup.find("span", class_="recruitment-summary__location")
    if region_element:
        region = region_element.get_text(strip=True)

    driver.quit()

    return {
        "stack": stack,
        "career": career,
        "region": region
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
scroll_limit = 2

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

    # 추가 정보를 병렬로 가져오기
    additional_info = scrape_additional_info(job_data["detail_url"])
    job_data["stack"] = additional_info["stack"]
    job_data["career"] = additional_info["career"]
    job_data["region"] = additional_info["region"]

    return job_data

# 스레드 풀을 사용하여 병렬 처리
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_job, job, link) for job, link in zip(job_elements, links)]
    for future in as_completed(futures):
        jobs_data.append(future.result())

# 결과 출력 (예시)
for job in jobs_data:
    print(job)

# 5. 브라우저 종료
driver.quit()