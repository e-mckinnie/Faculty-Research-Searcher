import re
import requests
import webbrowser
from bs4 import BeautifulSoup

def is_professor_official_webpage(tag):
    return tag.name == 'a' and tag.has_attr('href') \
        and tag.contents[0].name == 'img' and tag.img.has_attr('alt') \
        and tag.img['alt'].replace(" ", "-").lower() in tag['href'].lower()

def is_professor_personal_webpage(tag):
    return tag.name == 'a' and tag.has_attr('href') \
        and tag.text == 'Personal Webpage'

def is_professor(tag):
    tag.contents = [t for t in tag.contents if t != '\n']
    return tag.name == 'div' and len(tag.contents) >= 3 \
        and tag.contents[0].name == 'p' and len(tag.contents[0].contents) >=1 \
        and tag.contents[1].name == 'p' \
        and tag.contents[2].name == 'p' and len(tag.contents[2].contents) >= 1 \
        and is_professor_official_webpage(tag.contents[0].contents[0]) \
        and is_professor_personal_webpage(tag.contents[2].contents[0])

def search_page(url, search_words):
    try:
        individual_page = BeautifulSoup(requests.get(url).content, 'html.parser')
    except Exception:
        return False
    
    page_text = individual_page.find_all("p")
    for word in search_words:
        for x in page_text:
            if word.lower() in x.text.lower():
                return True
    return False
    
def search_prof(prof, search_words):
    urls = [prof.contents[0].contents[0]['href'], prof.contents[2].contents[0]['href']]
    for url in urls:
        word_found = search_page(url, search_words)
        if word_found:
            webbrowser.open(url, new=2)

if __name__ == '__main__':
    main_url = 'https://ic.gatech.edu/content/artificial-intelligence-machine-learning'
    search_words = ['equity']
    
    all_profs_page = BeautifulSoup(requests.get(main_url).content, 'html.parser')
    profs = all_profs_page.find_all(is_professor)

    for prof in profs:
        search_prof(prof, search_words)
