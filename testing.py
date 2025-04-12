# example.py

from gradescopeapi.classes.connection import GSConnection
from datetime import datetime
from zoneinfo import ZoneInfo

# create connection and login
connection = GSConnection()
connection.login("khender8@terpmail.umd.edu", "KesarPip01!!")

"""
Fetching all courses for user
"""
courses = connection.account.get_courses()

spring_2025_courses = {}

for course_id, course in courses["student"].items():
    if course.semester == "Spring" and course.year == "2025":
        spring_2025_courses[course_id] = course


unsubmitted = {}
late_submission = {}
course_names = []

# Print them
for course_id, course in spring_2025_courses.items():
    course_names.append(course.name)
    assignments = connection.account.get_assignments(course_id)
    unsub_assign = []
    late_sub = []
    for assignment in assignments:
        # if has not yet been submitted
        if assignment.due_date != None and assignment.submissions_status == "No Submission":
            if assignment.late_due_date != None:
                if datetime.now(ZoneInfo("America/New_York")) < assignment.late_due_date: 
                    unsub_assign.append(assignment)
            else: 
                if datetime.now(ZoneInfo("America/New_York")) < assignment.due_date:
                    unsub_assign.append(assignment)
            # if late submission if still an option
        else:
            if assignment.late_due_date != None and datetime.now(ZoneInfo("America/New_York")) < assignment.late_due_date: 
                late_sub.append(assignment)
    unsubmitted[course.name] = unsub_assign
    late_submission[course.name] = late_sub
    print('\n')
print(unsubmitted)
print("\n")
print(late_submission)
print(course_names)