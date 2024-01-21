import random

def build_supervisor_preferences(student_preferences, supervisor_capacities, seed_value):
        # initialize
        supervisor_preferences = {}
        random.seed(seed_value)

        for chair in supervisor_capacities: #TODO do we need to truncate by capacity?
            applicants = [stud for stud, selected_projects in student_preferences.items()
                        if any(chair == get_part_before_parenthesis(proj) for proj in selected_projects)]
            
            random.shuffle(applicants)

            supervisor_preferences[chair] = applicants

        return supervisor_preferences

def get_part_before_parenthesis(input_string):
    parts = input_string.split('(')
    if len(parts) > 1:
        return parts[0].strip()
    else:
        return input_string