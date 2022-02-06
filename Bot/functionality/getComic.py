from bs4 import BeautifulSoup 
import requests

def getComic():
    # get comic
    url = "https://dilbert.com/"
    # get url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # get comic
    comic = soup.find('img', {'class': 'img-responsive img-comic'})
    comic_url = comic['src']

    date = soup.find('date', {'class': 'comic-title-date'})
    # remove day 
    final_date = ""
    date.text.split(" ")[-1].strip(",")
    for el in date.text.split(' ')[1:]:
        final_date += el.rstrip().lstrip() + " "
    final_date = final_date.split(",")[0] + ", " + date.find_all('span')[1].text
    return [comic['alt'], comic_url, final_date]