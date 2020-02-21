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
    """
    Logs in to EU Luis portal using username and password

    :parameter: config.username is the username var loaded from the config file
    :parameter: config.password is the password var loaded from the config file
    :return: None
    """

    browser.get("https://eu.luis.ai")
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
    browser.find_element_by_link_text('Sign in').click()
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    browser.find_element_by_id('i0116').send_keys(config.username)
    browser.find_element_by_id('idSIButton9').click()
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    browser.find_element_by_id('i0118').send_keys(config.password)
    browser.find_element_by_id('idSIButton9').click()


def batch_test_open():
    """
    Navigates Luis portal and opens the batch testing pane

    :return: None
    """

    ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    browser.find_element_by_link_text('myapp_v01').click()
    buttons = browser.find_elements_by_class_name('nav-section')
    buttons[1].click()
    browser.find_element_by_xpath('//button[contains(text(), "Batch testing")]').click()


def batch_test_run():
    """
    Runs all available batch tests in the batch testing pane

    :return: none
    """
    batch_run_button = browser.find_elements_by_xpath('//button[contains(text(), "Run")]')

    for test in batch_run_button:
        test.click()


def main():
    """
    Runs all functions

    :return: None
    """
    login_luis()
    # batch_test_open()
    # batch_test_run()


if __name__ == '__main__':
    main()
