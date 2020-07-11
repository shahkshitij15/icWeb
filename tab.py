from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time 
from google import main as google

# driver = webdriver.Chrome('./chromedriver')
# driver.get("http://www.google.com/")
# time.sleep(2)

def open_tab(driver):
    #driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    ActionChains(driver).key_down(Keys.COMMAND).send_keys("t").key_up(Keys.COMMAND).perform()
    # You can use (Keys.CONTROL + 't') on other OSs
    driver.execute_script('''window.open("http://google.com","_blank");''')
    time.sleep(3)
    google.run()

# Load a page 
#driver.get('http://stackoverflow.com/')
# Make the tests...

# close the tab
# (Keys.CONTROL + 'w') on other OSs.
#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 

def close_tab(driver):
    driver.switch_to_window(driver.window_handles[1])
    print(type(driver.window_handles[1]))
    print(type(driver))
    #driver.close()
    time.sleep(1)
    driver.close()

# open_tab(driver)
# time.sleep(10)
# driver.switch_to_window(driver.window_handles[1])
# driver.execute_script("window.history.go(-1)")  
# time.sleep(5)
# close_tab(driver)
