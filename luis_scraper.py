import config
from variable_names import list_of_headers, intent_entity_titles
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

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
    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "cdk-overlay-pane")))
        ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    except:
        print("No migration pop-up")

    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, config.app_name)))
    browser.find_element_by_link_text(config.app_name).click()
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'nav-section')))
    buttons = browser.find_elements_by_class_name('nav-section')
    buttons[1].click()
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), '
                                                                                '"Batch testing")]')))
    browser.find_element_by_xpath('//button[contains(text(), "Batch testing")]').click()


def batch_test_run():
    """
    Runs all available batch tests in the batch testing panel

    :return: none
    """
    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), ''"Run")]')))
    batch_run_button = browser.find_elements_by_xpath('//button[contains(text(), "Run")]')
    for test in batch_run_button:
        test.click()
        time.sleep(5)


def batch_tests_results():
    """
    :return:
    """
    df = pd.DataFrame(columns=list_of_headers)
    batch_results_button = browser.find_elements_by_xpath('//a[contains(text(), "See results")]')

    for i in range(len(batch_results_button)):
        scores_dict = {}
        batch_results_button = browser.find_elements_by_xpath('//a[contains(text(), "See results")]')
        batch_results_button[i].click()
        time.sleep(3)
        back = browser.find_element_by_xpath('//button[contains(text(), "Back to list")]')
        title_batch_test = browser.find_element_by_xpath('//h3[contains(text(), "Dataset")]').text.split()[1][1:-1]
        scores_dict['Intent'] = title_batch_test
        utterances = browser.find_element_by_xpath('//*[contains(text(), "utterances passed")]').text[1:-1].split()
        utterances = utterances[0].split('/')[1]
        scores_dict['Size'] = utterances

        for intent_entity in intent_entity_titles:
            try:
                xpath_string = '//*[@title="' + intent_entity + '"]'
                batch_result = browser.find_element_by_xpath(xpath_string)
                element, score = batch_result.text.split("(")
                element = element.strip()
                scores_dict[element] = "=" + (score[:-1])
            except (NoSuchElementException, ValueError):
                print(intent_entity, "not in batch test, continuing to iterate over Intents provided")

        df = df.append(scores_dict, ignore_index=True)
        back.click()
        time.sleep(3)
    df.to_csv("tester.csv", index=False)


def main():
    """
    Runs all functions

    :return: None
    """
    login_luis()
    batch_test_open()
    batch_test_run()
    batch_tests_results()


if __name__ == '__main__':
    main()
