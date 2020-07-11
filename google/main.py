import time, sys, os
sys.path.append(os.path.abspath("../"))
from selenium import webdriver
import stt
import speech_recognition as sr
import tts
import urllib
import requests
from bs4 import BeautifulSoup
from google import scraper

driver=None
# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

def get_data(query):
    #query = "cricket"
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "title": title,
                    "link": link
                }
                results.append(item)
                print(item['title'])
    return results

#print(sr.Microphone.list_microphone_names())

def run():
    global driver
    device_id, sample_rate, chunk_size, r = stt.setup()
    tts.play_plain_text("Loading google")
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    driver.get('https://www.google.com')
    # time.sleep(5) # Let the user actually see 
    search_box = driver.find_element_by_name('q')
    #time.sleep(3) # Let the user actually see something!

    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        tts.play_plain_text("Hey! Welcome What do you want to search")
        # #main 
        text = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
    # time.sleep(2)
    stt.speak(text)

    # #confirmation from the user
    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        tts.play_plain_text("Are you sure you want to search for "+text)
        resp = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
    while resp != "yes":
        with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
            r.adjust_for_ambient_noise(source)
            tts.play_plain_text("repeat your search")
            text = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
        time.sleep(2)
        with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
            stt.speak(text)
            tts.play_plain_text("Are you sure you want to search for "+text)
            resp = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)

    tts.play_plain_text("Searching results")
    search_box.send_keys(text)
    search_box.submit()
    # time.sleep(5) # Let the user actually see something!
    #sdriver.quit()
    tts.play_plain_text("Loading")



    results = get_data(text)
    print(results)

    def find(lst, key, value):
        for i, dic in enumerate(lst):
            if dic[key] == value:
                return i
        return -1
    print("Length of results : " + str(len(results)))
    for index, result in enumerate(results):
        # index = find(results, "title", result['title'])
        index+=1
        with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
            r.adjust_for_ambient_noise(source)
            tts.play_plain_text(str(index)+"."+ result['title'])
            resp = stt.listen(device_id, sample_rate, chunk_size, r, driver, source, flag=True)

        if resp == 'next':
            continue

        elif resp.isdigit() and int(resp) in range(1, len(results)):
            #go to that link
            print(resp+results[int(resp)-1]['title'])
            driver.get(results[int(resp)-1]['link'])
            a = results[int(resp)-1]['link']
            scraper.scrape(a)
        else:
            print("Invalid index")
            tts.play_plain_text("Invalid index")