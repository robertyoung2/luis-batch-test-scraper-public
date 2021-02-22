import config
import time
import pandas as pd
from variable_names import list_of_headers, intent_entity_titles, batch_test_set
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
# browser = webdriver.Chrome(executable_path=config.home_path, options=option)
browser = webdriver.Chrome(options=option)


def login_luis():
    """
    Logs in to EU Luis portal using username and password

    :parameter: config.username is the username var loaded from the config file
    :parameter: config.password is the password var loaded from the config file
    :return: None
    """
    browser.get("https://www.luis.ai/")
    browser.find_element_by_id('id__10').click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    browser.find_element_by_id('i0116').send_keys(config.username)
    browser.find_element_by_id('idSIButton9').click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))

    if browser.find_element_by_link_text('Other ways to sign in'):
        browser.find_element_by_link_text('Other ways to sign in').click()
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Use my password']")))
        browser.find_element_by_xpath("//div[@aria-label='Use my password']").click()

    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    browser.find_element_by_id('i0118').send_keys(config.password)
    browser.find_element_by_id('idSIButton9').click()


def authoring_resource():

    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Welcome to the Language Understanding Intelligent Service (LUIS)!"]')))
    browser.find_element_by_xpath('//*[text()="Select subscription"]').click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search subscription"]')))
    browser.find_element_by_xpath('//*[@title="%s"]' % config.subscription).click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Select or create an authoring resource"]')))
    browser.find_element_by_xpath('//*[text()="Select or create an authoring resource"]').click()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Select an authoring resource ..."]')))
    browser.find_element_by_xpath('//*[@placeholder="Select an authoring resource ..."]').click()
    browser.find_element_by_xpath('//*[text()="%s"]' % config.authoring_resource).click()
    browser.find_element_by_xpath('//*[text()="Done"]').click()


def batch_test_open():
    """
    Navigates Luis portal and opens the batch testing pane

    :return: None
    """

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="%s"]' % config.app_name)))
    browser.find_element_by_xpath('//button[text()="%s"]' % config.app_name).click()

    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[text()="How to create an effective LUIS app"]')))
        ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    except:
        print("No intro pop-up")

    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Upgrade your composite entities"]')))
        browser.find_element_by_xpath('//span[text()="Remind me later"]').click()
    except:
        print("No composite entities pop-up")

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Test"]')))
    browser.find_element_by_xpath('//span[text()="Test"]').click()
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), '
                                                                                '"Batch testing")]')))
    browser.find_element_by_xpath('//span[contains(text(), "Batch testing")]').click()


def batch_test_run():
    """
    Runs all available batch tests in the batch testing panel

    :return: none
    """
    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), ''"get_job_information")]')))
    batch_run_button = browser.find_elements_by_xpath('//span[(text()="Run")]')
    for index, button in enumerate(batch_run_button):
        if index > 0:
            button.click()

    while len(browser.find_elements_by_xpath('//span[(text()="See results")]')) < len(batch_run_button) - 1:
        time.sleep(1)


def batch_tests_results():
    """
    Opens each batch test and extracts the results information from it. NB: This goes through each of the intents in
    the 'overview' table of links and extracts the score. Eg. (78/123). It does not currently extract the confusion
    matrix scores. If required, the code can be adapted to do this. It then outputs these results to csv file.
    The list of intents and entities, csv headers and all batch tests to be run should be provided in variable_names.py.

    :return: None
    """
    df = pd.DataFrame(columns=list_of_headers)
    loaded_batch_tests = []
    batch_results_button = browser.find_elements_by_xpath('//span[contains(text(), "See results")]')

    for results_number in range(len(batch_results_button)):
        scores_dict = {}
        batch_results_button = browser.find_elements_by_xpath('//span[contains(text(), "See results")]')
        batch_results_button[results_number].click()
        time.sleep(3)
        back = browser.find_element_by_xpath('//button[contains(text(), "Back to list")]')
        title_batch_test = browser.find_element_by_xpath('//span[contains(text(), "Dataset")]').text.split()[1][1:-1]
        loaded_batch_tests.append(title_batch_test)
        scores_dict['Intent'] = title_batch_test
        # utterances = browser.find_element_by_xpath('//*[contains(text(), "utterances passed")]').text[1:-1].split()
        # utterances = utterances[0].split('/')[1]
        utterances = 5
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
        remaining_batch_tests(loaded_batch_tests)
        back.click()
        time.sleep(1)
        break
    df.to_csv("batch_test_results.csv", index=False)


def remaining_batch_tests(loaded_batch_tests):
    """
    Uses the batch tests names set from variable_names.py to determine which batch tests have been run and which remain.
    The remaining batch tests are outputted to a text file 'remaining_tests.txt' for the user to review.

    :param loaded_batch_tests:
    :return: None
    """
    remaining_tests = batch_test_set - set(loaded_batch_tests)
    with open('remaining_tests.txt', mode='w') as outfile:
        for batch_test in remaining_tests:
            outfile.write("%s\n" % batch_test)


def main():
    """
    Runs all functions

    :return: None
    """
    login_luis()
    authoring_resource()
    batch_test_open()
    batch_test_run()
    batch_tests_results()


if __name__ == '__main__':
    main()
