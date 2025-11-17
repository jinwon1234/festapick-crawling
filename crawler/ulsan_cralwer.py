import requests
from bs4 import BeautifulSoup
from domain import models
from repository import festival_repository
from datetime import datetime

def getSoup(url):
    baseUrl = "https://www.ulsanculture.kr"
    response = requests.get(baseUrl + url)
    html = response.text
    return BeautifulSoup(html, 'html.parser')



def ulsanCrawling():
    soup = getSoup("/webuser/exhibit/all_list.html?sch_so_show_kind=4")
    components = soup.select(".gal-box > div > div > a")
    for component in components: 
        link = component.attrs['href']
        soup = getSoup(link)
        poster = soup.select_one(".img-box > img")['src']
        title = soup.select_one(".subject").text
        overView = soup.select_one(".cont").text
        addr1 = soup.find("dt", string="장소").find_next_sibling("dd").text
        date = soup.find("dt", string="기간").find_next_sibling("dd").text.split("~")
        startDate = date[0].strip()
        endDate = date[1].strip()

        new_festival = models.Festival(
            addr1=addr1,
            addr2=None,
            areaCode=7,
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
        