import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from repository import festival_repository
from datetime import datetime
from domain import models
import re

BASE_URL = "https://fantasiafesta.or.kr/Festival-October?menuId=MENU_0000000282&searchFESTV_MONTH_DCD=CDF018.002"

def getSoup(url):
    response = requests.get(url)
    html = response.text
    return BeautifulSoup(html, 'html.parser')

def parseDateRange(date_str: str):

    if not date_str:
        return None, None

    # 공백 제거
    date_str = date_str.strip()

    # 정규식으로 날짜 부분만 추출 (예: 2025. 9. 23. ~ 12. 21.)
    pattern = r"(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})\..*?~\s*(?:(\d{4})\.\s*)?(\d{1,2})\.\s*(\d{1,2})"
    match = re.search(pattern, date_str)

    if not match:
        return None, None

    year1, month1, day1, year2, month2, day2 = match.groups()

    # 종료연도 생략 시, 시작연도 사용
    if not year2:
        year2 = year1

    # 날짜를 YYYY-MM-DD 형식으로 변환
    start_date = f"{int(year1):04d}-{int(month1):02d}-{int(day1):02d}"
    end_date = f"{int(year2):04d}-{int(month2):02d}-{int(day2):02d}"

    return start_date, end_date

def daegCrawling():
    soup = getSoup(BASE_URL)

    links = []
    for a_tag in soup.select("div.festival-list a[href]"):
        href = a_tag.get("href")
        full_url = urljoin(BASE_URL, href)
        links.append(full_url)

    for link in links:
        soup = getSoup(link)

        img_tag = soup.select_one("div.festival-thumImg img")
        img_url = img_tag["src"] if img_tag else None

        info = {}
        for li in soup.select("li.info-list"):
            key = li.find("span").get_text(strip=True)
            val = li.find("p").get_text(strip=True)
            info[key] = val

        title = info.get("축제명")
        startDate, endDate = parseDateRange(info.get("개최기간"))
        addr1 = info.get("장소")
        overView = info.get("주요프로그램")

        poster = img_url

        new_festival = models.Festival(
                addr1=addr1,
                addr2=None,
                areaCode=4,
                contentId=None,
                createdDate=datetime.now(),
                updatedDate=datetime.now(),
                startDate=startDate,
                endDate=endDate,
                festivalType="FESTAPICK",
                state="PROCESSING",
                homePage="no_hompage",
                posterInfo=poster,
                title=title,
                overView=overView,
                manager_id=None
            )

        if not festival_repository.existFestivalByTitle(new_festival.title):
            festival_repository.insertFestival(new_festival)
    
    

