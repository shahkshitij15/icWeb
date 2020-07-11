import wikipedia as w
import time, sys, os
sys.path.append(os.path.abspath("../"))
from selenium import webdriver
import stt
import speech_recognition as sr
import tts
from deeppavlov import build_model, configs

driver = None

def run():
    global driver
    tts.play_plain_text("loading please wait")
    print("bert model loading started")
    model = build_model(configs.squad.squad, download=False)
    print("bert model loaded")
    device_id, sample_rate, chunk_size, r = stt.setup()
    tts.play_plain_text("loading please wait")
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    driver.get('https://www.wikipedia.org/')
    # time.sleep(5) # Let the user actually see something!
    search_box = driver.find_element_by_id("searchInput")
    time.sleep(3) # Let the user actually see something!
    # text="cricket"
    # # speak(text)
    # search_box.send_keys(text)
    # search_box.submit()
    time.sleep(5) # Let the user actually see something!
# driver.execute_script("window.history.go(-1)")
    #time.sleep(3) # Let the user actually see something!

    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        tts.play_plain_text("What do you want to search ?")
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
            tts.play_plain_text("Repeat your search")
            text = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
            time.sleep(2)
            stt.speak(text)
            tts.play_plain_text("Are you sure you want to search for "+text)
            resp = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)

    tts.play_plain_text("Searching results")
    search_box.send_keys(text)
    search_box.submit()
    #time.sleep(5) # Let the user actually see something!
    #sdriver.quit()

    while(True) :
        with sr.Microphone(device_index = device_id, sample_rate = sample_rate,
                        chunk_size = chunk_size) as source: 
            r.adjust_for_ambient_noise(source)
            tts.play_plain_text("""Do you want 1. summary or 2. full content or 
            3. start a question answering session""")
            # tts.play_plain_text("start question answering session?")
            resp1 = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)

        if "summary" in resp1 or "one" in resp1 or "1" in resp1:
            article_summary = w.summary(text)
            tts.play_plain_text("Starting summary")
            tts.play_plain_text(article_summary)
            break
        elif "two" in resp1 or "2" in resp1:
            full_content = w.WikipediaPage(text).content
            tts.play_plain_text("Starting full content")
            tts.play_plain_text(full_content)
            break
        elif "three" in resp1 or "3" in resp1 or "tree" in resp1:
            q="yes"
            while q != "no":
                with sr.Microphone(device_index = device_id, sample_rate = sample_rate,
                                    chunk_size = chunk_size) as source:                            
                    r.adjust_for_ambient_noise(source)
                    tts.play_plain_text("Please utter your question after the beep")
                    q = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
                    pred = model([w.summary(text, sentences=10)], [q])
                    pred = pred[0][0]
                    tts.play_plain_text("The best match answer found is " + pred)

                    tts.play_plain_text("do you have another question ?")
                    q = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
                    q=q.strip()
                    q=q.lower()
            break
        else:
            tts.play_plain_text("Invalid option")
