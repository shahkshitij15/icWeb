import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common.keys import Keys
import time, sys, os
sys.path.append(os.path.abspath("../"))
from selenium import webdriver
import stt
import speech_recognition as sr
import tts
import urllib
import requests
from bs4 import BeautifulSoup
driver = None

def run():
    global driver
    driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    driver.get("http://www.gmail.com")

    device_id, sample_rate, chunk_size, r = stt.setup()
    '''pytts.play_plain_text("Enter Email Id")
    text = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
    print(text)'''
    tts.play_plain_text("Please wait while we log you in")
    driver.find_element_by_id("identifierId").send_keys('sahil.sheth@spit.ac.in')
    driver.find_element_by_id("identifierNext").click()
    time.sleep(2)
    driver.find_element_by_name("password").send_keys('test@12345')
    driver.find_element_by_id("passwordNext").click()
    time.sleep(5)
    driver.find_element_by_class_name('z0').click()
    time.sleep(5)

    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold=1
        tts.play_plain_text("Enter Reciever's Email i d")
        text = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
    text = text.replace(" ","")
    print(text)

    actions = ActionChains(driver)
    actions.send_keys(text.lower())
    actions.perform()
    webElement = driver.find_element_by_name("subjectbox")

    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        tts.play_plain_text("Enter Subject")
        subj = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
    print(subj)

    webElement.send_keys(subj)
    actions = ActionChains(driver)
    webElement.send_keys(Keys.TAB)
    time.sleep(2)
    x=driver.find_element_by_css_selector("div[aria-label='Message Body']")

    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                                chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        tts.play_plain_text("Enter Message")
        msg = stt.listen(device_id, sample_rate, chunk_size, r, driver, source)
    print(msg)

    x.send_keys(msg)
    time.sleep(2)
    sendElem = driver.find_element_by_xpath("//div[text()='Send']")
    sendElem.click()
    time.sleep(2)
    tts.play_plain_text("Mail was sent successfully")
    

