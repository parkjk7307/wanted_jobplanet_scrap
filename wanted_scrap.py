# **공고제목 - title** -
# **회사이름 - company_name** -
# **디테일 페이지로 가는 주소 - detail_url ** -
# **마감일 - end_date** -
# ** 참고한 플랫폼 이름 - platform_name** 
# ** 카테고리 - category_name** 
# ** 기술 스택 - stack ** -
# ** 지역  - region ** -
# ** 신입/경력 - career ** -

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# 추가 정보를 스크래핑하는 함수
def scrape_additional_info(url):
    # 각 스레드에서 별도의 driver 인스턴스를 생성
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        # BeautifulSoup으로 페이지 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 경력 추출 (career)
        career_element = soup.find("span", string=lambda text: text is not None and ("경력" in text or "신입" in text))
        career = career_element.get_text(strip=True) if career_element else "경력 정보 없음"

        # 기술 스택 추출 (stack)
        stack_heading = soup.find("h2", text="기술 스택 • 툴")
        stack_elements = stack_heading.find_next("ul").find_all("span", class_="Typography_Typography__root__RdAI1 Typography_Typography__label2__svmAA Typography_Typography__weightMedium__GXnOM") if stack_heading else None
        stack = [el.get_text(strip=True) for el in stack_elements] if stack_elements else ["기술 스택 없음"]

        # 마감일 추출 (end_date)
        end_date_element = soup.find("span", class_="Typography_Typography__root__RdAI1 Typography_Typography__body1-reading__3pEGb Typography_Typography__weightRegular__jzmck")
        end_date = end_date_element.get_text(strip=True) if end_date_element else "마감일 정보 없음"

        # 근무 지역 추출 (region)
        region_element = soup.find("span", class_="Typography_Typography__root__RdAI1 Typography_Typography__body2__5Mmhi Typography_Typography__weightMedium__GXnOM")
        region = region_element.get_text(strip=True) if region_element else "근무 지역 정보 없음"

        return {
            "end_date": end_date,
            "career": career,
            "region": region,
            "stack": stack
        }

    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return {
            "end_date": "마감일 정보 없음",
            "career": "경력 정보 없음",
            "region": "근무 지역 정보 없음",
            "stack": ["기술 스택 없음"]
        }
    finally:
        driver.quit()

##### 스크랩 시작 #####

# 웹 드라이버 설정 (메인 페이지에서 데이터 가져오기)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.wanted.co.kr/search?query=%EB%8D%B0%EC%9D%B4%ED%84%B0&tab=position")
driver.implicitly_wait(5)

# 페이지가 완전히 로드될 때까지 잠시 대기
time.sleep(5)

# 스크롤을 일정 횟수만큼 수행 (예: 5번)
scroll_pause_time = 1
scroll_limit = 20  # 스크롤 한계 설정

for _ in range(scroll_limit):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

# BeautifulSoup으로 페이지 파싱
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 공고 목록 추출
job_cards = soup.find_all("div", class_="JobCard_container__REty8")

# 결과를 저장할 리스트
jobs_data = []

# 스크랩할 각 공고를 처리하는 함수
def process_job(job_card):
    base_url = "https://www.wanted.co.kr"  # 실제 도메인으로 변경

    # 공고 제목 추출
    title_tag = job_card.find("strong", class_="JobCard_title__HBpZf")
    title = title_tag.get_text(strip=True) if title_tag else "제목 없음"

    # 회사 이름 추출
    company_name_tag = job_card.find("span", class_="JobCard_companyName__N1YrF")
    company_name = company_name_tag.get_text(strip=True) if company_name_tag else "회사명 없음"

    # 상세 URL 추출
    detail_url_tag = job_card.find("a", href=True)
    detail_url = base_url + detail_url_tag['href'] if detail_url_tag else "URL 없음"

    # 기본 공고 데이터 저장
    job_data = {
        "title": title,
        "company_name": company_name,
        "detail_url": detail_url,
        "platform_name": "wanted"
    }

    # 상세 페이지의 추가 정보를 병렬로 가져오기
    additional_info = scrape_additional_info(job_data["detail_url"])
    job_data.update(additional_info)

    return job_data

# 스레드 풀을 사용하여 병렬 처리
with ThreadPoolExecutor(max_workers=7) as executor:
    futures = [executor.submit(process_job, job_card) for job_card in job_cards]
    for future in as_completed(futures):
        jobs_data.append(future.result())

# 결과 출력
for job in jobs_data:
    print(job)

# 메인 페이지의 드라이버 종료
driver.quit()


