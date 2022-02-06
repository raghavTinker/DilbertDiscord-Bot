from bs4 import BeautifulSoup
import requests
from database import engine, SessionLocal
import models
from datetime import datetime

db = SessionLocal()
models.Base.metadata.create_all(bind=engine)

dilbert_start = 1989

def getAllPages(year):
        url = "https://dilbert.com/search_results?page={page_number}&sort=date_asc&year={year}"
        r = requests.get(url.format(page_number=1, year=year))
        soup = BeautifulSoup(r.text, "html.parser")
        # number of total pages
        # get the ul class pagination pagination
        ul = soup.find("ul", {"class": "pagination pagination"})
        # find all li tags in ul
        li_tags = ul.find_all("li")
        total_pages = len(li_tags)-2
        return total_pages

def get_comics():
    current_month = datetime.now().month
    current_year = datetime.now().year
    url = "https://dilbert.com/search_results?page={page_number}&sort=date_asc&year={year}"
    for year in range(current_year, dilbert_start-1, -1):
        total_pages = getAllPages(year)
        for page in range(1, total_pages+1):
            print(page)
            r = requests.get(url.format(page_number=page, year=year))
            soup = BeautifulSoup(r.text, "html.parser")
            # get all comic-item-container
            comic_item_containers = soup.find_all("div", {"class": "comic-item-container"})
            for comic_item_container in comic_item_containers:
                # <div accountableperson="Andrews McMeel Syndication" class="comic-item-container js-comic js-comic-container-2022-01-31" creator="Scott Adams" data-creator="Scott Adams" data-date="January 31, 2022" data-description="" data-id="2022-01-31" data-image="https://assets.amuniversal.com/438fa7e05d30013a93c2005056a9545d" data-itemtype="" data-tags="" data-title="Wait And See " data-url="https://dilbert.com/strip/2022-01-31?creator=Dilbert_Daily">
                try:
                    # get data-date
                    date = comic_item_container["data-date"]
                    # get data-title
                    title = comic_item_container["data-title"]
                    # get data-image
                    image = comic_item_container["data-image"]
                    print(title, image)
                    # check if image is already in database
                    if db.query(models.Comics).filter(models.Comics.url == image).first() is None:
                        # insert into database
                        comic = models.Comics(title, image, date)
                        db.add(comic)
                        db.commit()
                    else:
                        continue
                except:
                    continue
get_comics()
