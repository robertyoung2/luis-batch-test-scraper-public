# Luis Batch Test Results Scraper

Python application that:

* Navigates to the Luis platform and logs in
* Opens the batch testing panel and runs all batch tests (maximum of 10)
* Opens the results of each batch test and saves to a csv or json

## Known Issues

* Timeout error if webpage does not load - add logic to reload current page and try step again
* Several functions are using time.sleep() - need to try to implement an explicit wait

## Future Features

* Packaged as a full interactive application
* Option to load in new batch tests
* Option to remove batch tests 
