# Luis Batch Test Results Scraper

At present, the Microsoft service Luis (Language Understanding) does not provide a means to download the results of
batch tests. The results are all provided visually via the batch testing dashboard interface.

It can be time consuming to review and extract these results by hand. As a workaround to this problem, this repo is a 
Python script integrated with the Selenium Webdriver which can previously uploaded batch tests and extract the results
to a csv for further data analysis and interrogation. This script has been tailored to my own needs, so modification
may be needed for obtained other interactions and outputs with the batch testing Dashboard. 

In its current form, the scraper works with a batch test for each intent. For example, if your intents are [GetJobInformation, EmployeeFeedback, ApplyForJob] you should have batch tests with utterances which test each of these intents individually:

![Batch Testing Panel](https://github.com/robertyoung2/luis-batch-test-scraper-public/blob/master/images/batch_test_panel.png "Batch Test Panel and Tests")

![Intent Batch Test Results](https://github.com/robertyoung2/luis-batch-test-scraper-public/blob/master/images/getjobinfo_results.png "Intent Batch Test Results")



## Configuration and Variable files

There are two core files for configuration and operation of this script:

* [config.py](https://github.com/robertyoung2/luis-batch-test-scraper-public/blob/master/config.py)
* [variable_names.py](https://github.com/robertyoung2/luis-batch-test-scraper-public/blob/master/variable_names.py)

### config.py

This file is the configuration settings for running the Selenium web driver and logging into the Luis portal. It 
contains four variables to be defined. These are:

* username: the account username for Luis, as a string, for example "billgates@microsoft.com".
* password: the associated password for the username, as a string, for example "i-love-cortana".
* home_path: defines the user path on their local machine to the [Chrome web driver](https://chromedriver.chromium.org/downloads), for example "~/chromedriver".
* app-name: the name of the Luis app to be loaded on the "My Apps" page in Luis, for example "myapp_v01".
* subscription: the azure subscription you wish to use (handles pop-up prompt if it appears).
* authoring-resource: the resource name for [authoring](https://docs.microsoft.com/en-us/azure/cognitive-services/luis/luis-how-to-azure-subscription) and query prediction runtime resources.

### variable_names.py 

* list_of_headers: Defines the list of headers for the csv file where results will be saved to. Intent headers should
match exactly the names of the intent in the Luis App Build screen. 
* intent_entity_titles: List all the names of the Intents and Entities for score extraction in the batch testing
panel results pages. Ensure that all Intents and Entities are exactly the same as those listed under your App Assests.
* batch_test_set: A complete list of all the names of the batch tests you wish to run. Luis limits uploaded batch
tests to a total of 10. If you have more than 10, this will allow a comparison between batch tests run and batch tests 
remaining. 


## Explanation of functions in the script 'luis_scraper.py' 

### login_luis()

Function to log the user into their Luis platform account. Executes the following step:

* Navigates to the Luis home page, in this implementation www.eu.luis.ai is used.
* Clicks on the 'Sign in" button'.
* On the sign in page, enters the users account email address and clicks 'Next'.
* Then enters the password associated with this account and clicks 'Sign in'.

Some key points to note about the function and its selenium interactions:

The element_id used for the "Next" button and "Sign in" button are 'i0116' and 'i0118' respectively. This may be 
different for other luis portals so may need adjustment.

### batch_test_open()

Function to navigate to and open the batch testing panel. Executes the following steps:

* Checks if the migration pop appears, uses keystroke 'esc' to bypass the message. If no pop appears, do nothing.
* Clicks on and navigates to the desired app, details of the name should be entered in the 'config.py' file.
* Collects the buttons in the nav-bar, clicks on the 'Test' button. 
* Clicks on the 'Batch testing' link presented on the 'Test' panel.

### batch_test_run()

Function to run all the uploaded JSON batch tests. Executes the following steps:

* Collects all the 'Run' button link elements.
* Runs each test one-by-one until complete. 

### batch_tests_results()

This is the core function within the script. It accesses each of the batch tests results, and extracts the information
within the intent results and adds it to a dataframe, which on completion is saved as a csv of all results. Executes 
the following steps:

* Initialises the dataframe to save results to, and a list to track the names of batch tests with generated results.
* For each set of results, clicks on the results link.
* On the results page, records the name of the batch test and how many utterances were passed to it.
* Still on the current batch test results page, the script will now try to find each of the intents and entities listed
in variable_names.intent_entity_titles and save the score in a dictionary. The scores are stored in the format 
"=123/456", as this calculates the percentage when transferred into a spreadsheet notebook. 
* After each score has been saved for each element in the batch test results page, this dictionary of elements and 
scores is appended to the dataframe. 
* remaining_batch)tests() is called which subtracts the current batch test  from the set of remaining batch tests, 
thereby keeping track of which batch test are left to be loaded if the user wishes to load and run more than the Luis
limit of 10.
* This is carried out until all batch test results have been retrieved. 

### remaining_batch_tests()

Function which takes as input the batch test name just completed. Subtracts this from the set of all batch tests
to be run and writes to a text file. In this way at the end of the scripts execution the user can check to see
which batch tests are left to upload and run (if the user has defined more than the Luis limit of 10 batch tests for 
execution).

## Known Issues/Bugs

* Timeout error if webpage does not load - add logic to reload current page and try step again
* Several functions are using time.sleep() - need to try to implement an explicit wait

## Future Features (Ideas)

* Packaged as a full interactive application
* Option to load in new batch tests
* Option to remove batch tests 

