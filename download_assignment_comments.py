#!/usr/bin/env python
import os
import csv
from canvasapi import Canvas


STRING_IN_NAME='Agnt_With_Comments'
OUTPUT_FILE=f'{STRING_IN_NAME} comments.tab'

course = Canvas(MyKeys['Canvas']['site'], MyKeys['Canvas']['token']).get_course(MyKeys['Canvas']['course_id'])

# Get Students
enrollments = course.get_enrollments()
# Build a map of student ID to their name
id_to_name = dict( (e.user_id, e.user['name'])  for e in enrollments )

assignments = course.get_assignments()

for a in assignments:
    if STRING_IN_NAME in a.name:
        comments = []
        print(f'Comments in {a.name}')
        for s in a.get_submissions(include=['submission_comments']):
            for c in s.submission_comments:
                student_name = id_to_name[s.user_id]
                last_name = student_name.split(' ')[-1]
                comments.append([last_name, student_name, c['comment']])
        print(f'Found {len(comments)} comments')
        if comments:
            comments.sort()
            with open(OUTPUT_FILE, 'w') as f:
                writer = csv.writer(f, delimiter='\t')
                for rw in comments:
                    writer.writerow(rw[1:])
            print(f'Saved {len(comments)} comments to {OUTPUT_FILE}')
        break  # only do one assignment
