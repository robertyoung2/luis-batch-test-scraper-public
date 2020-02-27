# Headers to be used to populate the csv output file
list_of_headers = ['App_Version', 'Date', 'Comments', 'Intent_1', 'Intent_2', 'Intent_3', 'Entity_1', 'Entity_2',
                   'Entity_3', 'TP', 'FP', 'TN', 'FN', 'F1-Score']

# For your Luis model, this should contain the names of all intents and entities. This is used to iterate over the
# batch test results and collect the outputted scores for each intent and entity
intent_entity_titles = ['Intent_1', 'Intent_2', 'Intent_3', 'Entity_1', 'Entity_2', 'Entity_3']

# This is a list of all the batch tests to be run. Luis can accept a maximum of 10 batch tests at a time.
# This list allows the script to produce a text file listing which batch tests have not been run yet.
batch_test_set = {'Intent_1', 'Intent_2', 'Intent_3'}
