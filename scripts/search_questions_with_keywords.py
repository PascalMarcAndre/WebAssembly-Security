# Fetches all Stack Overflow questions matching the search term "WebAssembly [keyword]" where the keyword gets replaced
# one by one with one of the keywords from our separate text file. Once we have a list with all unique questions matching
# at least one of our search term, we save all the available/necessary data in a CSV-file for further processing.

# Import required libraries
from stackapi import StackAPI
import datetime as dt
import csv
import json

# Create list that holds all keywords from our separate keywords text file
keywords = []
# Create empty list to which we will add all unique questions from the search results
questions = []

# Parse text file with all keywords and store them in a list
with open('../keywords/keywords.txt') as keywords_file:
    for line in keywords_file:
        keyword = line.strip("\n")
        if len(keyword) > 0:
            keywords.append(keyword)

# Setup StackAPI to use Stack Overflow as its source
SITE = StackAPI('stackoverflow')

# Search questions on Stack Overflow with each keyword as "WebAssembly [keyword]" and print them to a CSV-file
with open('all_questions.csv', 'w', encoding='utf-8', newline='') as questions_file:
    # Create CSV writer to convert data into delimited strings
    writer = csv.writer(questions_file, delimiter=';')

    # Write header row with labels/titles
    writer.writerow([
        'Index',
        'Title',
        'Score',
        'Is Answered',
        'Answer Count',
        'View Count',
        'Question ID',
        'Tags',
        'Creation Date',
        'Last Activity Date',
        'Owner Reputation',
        'Owner User ID',
        'Owner User Type',
        'Owner Profile Image',
        'Owner Display Name',
        'Owner Accept Rate',
        'Owner Link',
        'Question Link'
    ])


    # Iterate over each keyword and request questions to create final list of unique questions
    for keyword in keywords:
        # Build search term using "WebAssembly" and the currently selected keyword
        searchTerm = 'webassembly ' + keyword

        # Use StackAPI to fetch all questions matching above search term using the endpoint "search/advanced"
        # We use the 'q' parameter with our search term to tries to match it with any question property (title, body...)
        new_questions = SITE.fetch('search/advanced', q=searchTerm)
        # NOTE | Possible parameters: sort='relevance, has_more=1, max_pages=1000, page_size=100

        # Check if any of the new questions has been added before (matched in previous search)
        for new_question in new_questions['items']:
            # We assume new question is not existing in our list yet (not an old questions)
            old_question = False

            # If any existing question matches new question's ID, we mark new question as old
            for question in questions:
                if question['question_id'] == new_question['question_id']:
                    old_question = True
                    break

            # If new question is not an old/existing one, we add it to questions list
            if not old_question:
                questions.append(new_question)


    # Iterate over final list of unique Stack Overflow questions and print their data into the CSV file
    for index, question in enumerate(questions, start=1):
        # Pre-process some data including dates and nested JSON data
        creation_date = dt.date.fromtimestamp(question['creation_date']).strftime('%Y-%m-%d')
        last_activity_date = dt.date.fromtimestamp(question['last_activity_date']).strftime('%Y-%m-%d')
        owner = question['owner']

        q_title = ''
        q_score = ''
        q_is_answered = ''
        q_answer_count = ''
        q_view_count = ''
        q_question_id = ''
        q_tags = ''
        o_reputation = ''
        o_user_id = ''
        o_user_type = ''
        o_profile_image = ''
        o_display_name = ''
        o_accept_rate = ''
        o_link = ''
        q_link = ''

        try:
            q_title = question['title']
        except KeyError:
            print(str(index) + ' q_title')

        try:
            q_score = question['score']
        except KeyError:
            print(str(index) + ' q_score')

        try:
            q_is_answered = question['is_answered']
        except KeyError:
            print(str(index) + ' q_is_answered')

        try:
            q_answer_count = question['answer_count']
        except KeyError:
            print(str(index) + ' q_answer_count')

        try:
            q_view_count = question['view_count']
        except KeyError:
            print(str(index) + ' q_view_count')

        try:
            q_question_id = question['question_id']
        except KeyError:
            print(str(index) + ' q_question_id')

        try:
            q_tags = question['tags']
        except KeyError:
            print(str(index) + ' q_tags')

        try:
            o_reputation = owner['reputation']
        except KeyError:
            print(str(index) + ' o_reputation')

        try:
            o_user_id = owner['user_id']
        except KeyError:
            print(str(index) + ' o_user_id')

        try:
            o_user_type = owner['user_type']
        except KeyError:
            print(str(index) + ' o_user_type')

        try:
            o_profile_image = owner['profile_image']
        except KeyError:
            print(str(index) + ' o_profile_image')

        try:
            o_display_name = owner['display_name']
        except KeyError:
            print(str(index) + ' o_display_name')

        try:
            o_accept_rate = owner['accept_rate']
        except KeyError:
            print(str(index) + ' o_accept_rate')

        try:
            o_link = owner['link']
        except KeyError:
            print(str(index) + ' o_link')

        try:
            q_link = question['link']
        except KeyError:
            print(str(index) + ' q_link')

        # Extract question properties from JSON-fields (only writes them if no error exists)
        writer.writerow([
            index,
            q_title,
            q_score,
            q_is_answered,
            q_answer_count,
            q_view_count,
            q_question_id,
            q_tags,
            creation_date,
            last_activity_date,
            o_reputation,
            o_user_id,
            o_user_type,
            o_profile_image,
            o_display_name,
            o_accept_rate,
            o_link,
            q_link,
        ])

# Print raw JSON data into separate file for further inspection
with open('all_questions.json', 'w', encoding='utf-8') as json_file:
     json.dump(questions, json_file, indent=4)

# Success message
print('Process completed successfully. Printed data of ' + str(len(questions)) + ' questions to CSV-file.')
