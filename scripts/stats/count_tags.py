# Lists all tags from the relevant questions including their count how often they appear in questions
# Creates separate CSV file where results are exported to

# Import required libraries
from operator import itemgetter
import json
import csv

# Create empty list that holds all tags and the total number of times the tags was identified within a question
tags = []

# Open text file containing all question ids of the relevant questions to be processed
with open('../../data_files/questions/all_relevant_question_id.txt') as text_file:
    # Each 'line' corresponds to one question id in the text file to be processed
    for line in text_file:
        # Open the JSON-file of the question related to the current question id ('line' variable)
        with open('../../data_files/questions/json_files/' + line.strip() + '.json')as json_file:
            # Loads the JSON-file content into the 'question' variable
            question = json.load(json_file)

        # Iterate over all tags from the current question
        for new_tag in question['tags']:
            # Assume this tag appears for the first time
            is_new_tag = True

            # Iterate over all tags within our 'tags' list
            for existing_tag in tags:
                # If a tag in our list matches the currently processed tag...
                if existing_tag[0] == new_tag:
                    # ...increase its counter of questions by one
                    existing_tag[1] += 1
                    # ...update that the currently processed tag is not a new one
                    is_new_tag = False
                    break

            # If the currently processed tag is a new one...
            if is_new_tag:
                # ...add it to our list of tags and set its question count to 1
                tags.append([new_tag, 1])

    # Sort all tags according to their count
    tags.sort(key=itemgetter(1))
    # Reverse order to have results in descending order
    tags.reverse()

    # Open CSV-file to write the results
    with open('all_tags.csv', 'w', encoding='utf-8', newline='') as csv_file:
        # Create CSV writer to convert data into delimited strings
        writer = csv.writer(csv_file, delimiter=';')

        # Set column headers to 'Tag' and 'Count'
        writer.writerow([
            'Tag',
            'Count'
        ])

        # Iterate over all identified tags
        for tag in tags:
            # Write each tag with its count to the CSV writer
            writer.writerow([
                tag[0],
                tag[1]
            ])
