import requests

# Global configuration
CURRENT_TERM = 4710  # Set your desired current term here
CANVAS_API_URL = "https://umd.instructure.com/api/v1"  # Canvas API base URL for UMD

def get_courses(headers):
    """
    Retrieve all active courses for the user.
    Courses are then filtered by the course term.
    """
    url = f"{CANVAS_API_URL}/courses?enrollment_state=active&per_page=100"
    courses = []
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching courses: {response.status_code} {response.text}")
        return courses

    try:
        courses.extend(response.json())
    except Exception as e:
        print("Error parsing JSON from courses response:", e)
        return courses

    # Handle pagination if more courses are available.
    while 'next' in response.links:
        url = response.links['next']['url']
        response = requests.get(url, headers=headers)
        try:
            courses.extend(response.json())
        except Exception as e:
            print("Error parsing JSON on pagination for courses:", e)
            break

    # Filter courses based on the current term
    filtered_courses = []
    # print(courses)
    for course in courses:
        # Canvas course object may include a 'term' dictionary containing 'name'
        term = course.get("enrollment_term_id")
        # print(term)
        if term == CURRENT_TERM:
            filtered_courses.append(course)
    # print(filtered_courses)
    return filtered_courses

def get_assignments(headers, course_id):
    """
    Retrieve all assignments for a given course.
    Request submission information by including it in the query parameters.
    """
    # Note the include[]=submission parameter to fetch submission details
    url = f"{CANVAS_API_URL}/courses/{course_id}/assignments?per_page=100&include[]=submission"
    assignments = []
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching assignments for course {course_id}: {response.status_code} {response.text}")
        return assignments

    try:
        assignments.extend(response.json())
    except Exception as e:
        print("Error parsing JSON from assignments response:", e)
        return assignments

    # Handle pagination for assignments
    while 'next' in response.links:
        url = response.links['next']['url']
        response = requests.get(url, headers=headers)
        try:
            assignments.extend(response.json())
        except Exception as e:
            print("Error parsing JSON on pagination for assignments:", e)
            break

    return assignments

def get_user_info(access_token):
    # HTTP headers for authentication
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    courses = get_courses(headers)
    if not courses:
        print("No courses found for term:", CURRENT_TERM)
        return

    submitted = {}
    unsubmitted = {}
    for course in courses:
        course_id = course.get('id')
        course_name = course.get('name')
        print(f"\nCourse: {course_name} (ID: {course_id})")
        assignments = get_assignments(headers, course_id)
        submitted_assignments = []
        unsubmitted_assignments = []
        if not assignments:
            print("  No assignments found.")
        else:
            assignments = [assignment for assignment in assignments if assignment["published"] and assignment['submission_types'] != ['none'] and assignment["due_at"] != None]
            # print(assignments)
            for assignment in assignments:
                # print(assignment)
                assignment_id = assignment.get('id')
                assignment_name = assignment.get('name')
                due_date = assignment.get('due_at')  # May be None if no due date is set
                turned_in = assignment.get('has_submitted_submissions')
                # late_due_date = assignment.get("")
                print(f"  Assignment: {assignment_name} (ID: {assignment_id})")
                print(f"    Due Date: {due_date}")
                print(f"    Turned In: {'Yes' if turned_in else 'No'}")
                if turned_in:
                    submitted_assignments.append({"name": assignment_name, "due_date": due_date})
                else:
                    unsubmitted_assignments.append({"name": assignment_name, "due_date": due_date})
                if assignment_name == "HW4":
                    print(assignment)
        submitted[course_name] = submitted_assignments
        unsubmitted[course_name] = unsubmitted_assignments
    return submitted, unsubmitted


get_user_info("1133~xGC6cyJVKPZ79umQAuzWRD7UAvPLNNrveVwDut84cEfzcrB9YKFJXYM7yvLMcQkw")