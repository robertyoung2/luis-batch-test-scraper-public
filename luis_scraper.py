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

browser = webdriver.Chrome(executable_path=config.home_path, options=option)


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


def batch_test_open():
    
    ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    browser.find_element_by_link_text('myapp_v01').click()
    time.sleep(5)
    buttons = browser.find_elements_by_class_name('nav-section')
    buttons[1].click()
    time.sleep(5)
    browser.find_element_by_xpath('//button[contains(text(), "Batch testing")]').click()


def main():
    login_luis()
    batch_test_open()


if __name__ == '__main__':
    main()
