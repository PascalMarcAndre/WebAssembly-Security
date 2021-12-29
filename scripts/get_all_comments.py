# This script fetches all comments for each individual answer and stores the data in separate JSON-files named after its
# question id (each JSON-file contains all comments to that particular answer).

# Import required libraries
from stackapi import StackAPI
import json

# Setup StackAPI to use Stack Overflow as its source
SITE = StackAPI('stackoverflow')

# Open text file with all answer ids to which we will collect all the comments for
with open('../data_files/answers/all_answer_id.txt') as id_file:
    # Load a list of answer ids from the text file
    lines = [line.rstrip() for line in id_file]

    # Iterate over all answer ids
    for line in lines:
        # Use StackAPI to fetch full details (incl body) of all comments using the endpoint "/answers/{id}/comments"
        new_comments = SITE.fetch('answers/{id}/comments', id={line}, sort='creation', filter='withbody')

        # Open a new JSON-file named after the answer id where all its raw comment JSON data gets saved/dumped to
        with open('comments/'+ line + '.json', 'w', encoding='utf-8') as comment_file:
            json.dump(new_comments['items'], comment_file, indent=4)
