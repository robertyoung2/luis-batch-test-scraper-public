# Headers to be used to populate the csv output file
list_of_headers = ['Intent', 'Model Version', 'Commments', 'Size', 'Result', 'Arabic', 'ChangeLanguage', 'Complete',
                   'Confirmation', 'Delete_and_Restart', 'Gibberish', 'HowAreYouResponse', 'How_are_you', 'Ignore',
                   'None', 'Preferences', 'Question', 'Restart', 'command', 'end_conversation', 'greeting', 'learning',
                   'suggestion', 'Language', 'No', 'Subtopics 1', 'Topics', 'Yes', 'TP', 'FP', 'FN', 'TN',
                   'Precision', 'Recall', 'F-Score']

# For your Luis model, this should contain the names of all intents and entities. This is used to iterate over the
# batch test results and collect the outputted scores for each intent and entity
intent_entity_titles = ['Arabic', 'ChangeLanguage', 'Complete', 'Confirmation', 'Delete_and_Restart', 'Gibberish',
                        'HowAreYouResponse', 'How_are_you', 'Ignore', 'None', 'Preferences', 'Question', 'Restart',
                        'command', 'end_conversation', 'greeting', 'learning', 'suggestion', 'Language', 'No',
                        'Subtopics 1', 'Topics', 'Yes']

# This is a list of all the batch tests to be run. Luis can accept a maximum of 10 batch tests at a time.
# This list allows the script to produce a text file listing which batch tests have not been run yet.
batch_test_set = {'ChangeLanguage', 'command', 'Confirmation', 'Delete_and_Restart', 'end_conversation', 'greeting',
                  'How_are_you', 'learning', 'None', 'Preferences', 'Restart', 'suggestion'}
