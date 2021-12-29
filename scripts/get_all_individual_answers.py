# After previously fetching basic details for the questions that matched during at least one of our search terms, this
# script fetches full details for all answers of each individual question in the search results and stores the data in
# separate JSON-files named after its question id.

# Import required libraries
from stackapi import StackAPI
import json

# Setup StackAPI to use Stack Overflow as its source
SITE = StackAPI('stackoverflow')

# Open text file with all question ids that were matched for at least one of our search terms
with open('../data_files/questions/all_relevant_question_id.txt') as id_file:
    # Load a list of question ids from the text file
    lines = [line.rstrip() for line in id_file]

    # Iterate over all question ids
    for line in lines:
        # Use StackAPI to fetch full question details (incl. body) using the endpoint "/questions/{ids}/answers"
        new_answer = SITE.fetch('questions/{ids}/answers', ids={line}, sort='creation', filter='withbody')

        # Open a new JSON-file named after the question id where all the raw JSON data gets saved/dumped to
        with open('../data_files/answers/json_files/' + line + '.json', 'w', encoding='utf-8') as answer_file:
            json.dump(new_answer['items'], answer_file, indent=4)
