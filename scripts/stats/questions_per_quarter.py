# Lists the number of questions that have been posted during a quarter of a year

# Import required libraries
import json
import datetime as dt
import pandas as pd

# Create empty list that holds all quarters and the total number of questions in each quarter
quarters = []

# Open text file containing all question ids of the relevant questions to be processed
with open('../question_id.txt') as text_file:
    # Each 'line' corresponds to one question id in the text file to be processed
    for line in text_file:
        # Open the JSON-file of the question related to the current question id ('line' variable)
        with open('../questions/' + line.strip() + '.json')as json_file:
            # Loads the JSON-file content into the 'question' variable
            question = json.load(json_file)

            # Creates proper date-variable from the creation date timestamp of the current question
            date = dt.date.fromtimestamp(question['creation_date'])

            # Finds the year from the creation date timestamp
            year = date.strftime('%Y')
            # Finds the quarter number from the creation date timestamp
            quarter_number = pd.Timestamp(date).quarter

            # Build quarter name based on previously found year and quarter number
            quarter_name = str(year) + "-Q" + str(quarter_number)

            # Assume this is the first question within this quarter
            is_new_quarter = True

            # Iterate over all quarters in our list
            for quarter in quarters:
                # If a quarter in our list matches the currently identified quarter...
                if quarter[0] == quarter_name:
                    # ...increase its counter of questions by one
                    quarter[1] += 1
                    # ...update that the currently identified quarter is not a new one
                    is_new_quarter = False
                    break

            # If the currently identified quarter is a new one...
            if is_new_quarter:
                # ...add it to our list of quarters and set its question count to 1
                quarters.append([quarter_name, 1])

    # Print the results of all quarters
    print(quarters)
