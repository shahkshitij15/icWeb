import requests
from bs4 import BeautifulSoup
import time, sys, os
sys.path.append(os.path.abspath("../"))
import tts

def scrape(link):
    url = link
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style'
    # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name in ['p','h1', "title", "h2", "h5", "h6"]:
            output += '{} '.format(t)

    print(output)
    tts.play_plain_text(output)