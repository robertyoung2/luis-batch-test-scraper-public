import time
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

browser = webdriver.Chrome(executable_path=config.home_path, chrome_options=option)


def login_luis():
    browser.get("https://eu.luis.ai")
    time.sleep(3)
    browser.find_element_by_link_text('Sign in').click()
    time.sleep(3)
    browser.find_element_by_id('i0116').send_keys(config.username)
    browser.find_element_by_id('idSIButton9').click()
    time.sleep(3)
    browser.find_element_by_id('i0118').send_keys(config.password)
    browser.find_element_by_id('idSIButton9').click()
    time.sleep(5)
    ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    browser.find_element_by_link_text('myapp_v01').click()
    time.sleep(5)


login_luis()
