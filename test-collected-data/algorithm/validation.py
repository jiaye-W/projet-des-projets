"""Validate the data passed to maching algorithm"""

# Method which checks the missing preferences. 
def find_missing_preferences(student_prefs, supervisor_prefs):
    # Extract supervisors from supervisor_preferences
    supervisors = set(supervisor_prefs.keys())
    
    # Extract projects from student_preferences (assuming project name after 'Project-' is the supervisor name)
    student_projects = {project.split('-')[1] for prefs in student_prefs.values() for project in prefs}
    
    # Check for missing supervisors
    missing_supervisors = student_projects - supervisors
    
    # Extract students from student_preferences
    students = set(student_prefs.keys())
    
    # Check for missing students in supervisor preferences
    missing_students = {}
    for supervisor, prefs in supervisor_prefs.items():
        missing_students_for_supervisor = [student for student in prefs if student not in students]
        if missing_students_for_supervisor:
            missing_students[supervisor] = missing_students_for_supervisor
    
    return missing_supervisors, missing_students

# Example usage
student_preferences = {
    'Student-1': ['Project-29', 'Project-28', 'Project-Patakfalvi-undefined'],
    'Student-94': ['Project-6', 'Project-5'],
    'Student-110': ['Project-6', 'Project-29']
}

supervisor_preferences = {
    'Supervisor-6': ['Student-94', 'Student-110', 'Student-140', 'Student-117'],
    'Supervisor-29': ['Student-1', 'Student-2'],
    'Supervisor-5': ['Student-3', 'Student-4']
}

missing_supervisors, missing_students = find_missing_preferences(student_preferences, supervisor_preferences)
print("Missing supervisors for student projects:", missing_supervisors)
print("Missing students for supervisors:", missing_students)
