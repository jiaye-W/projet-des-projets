import random

from data.students import generate_students
from data.students import get_number_of_master_students

from data.projects import generate_projects_data
from data.projects import get_number_of_projects_group_based
from data.projects import get_project_supervisors_group_based
from data.projects import get_project_supervisors_project_based
from data.projects import get_project_capacities_group_based

from student_preferences import build_student_preferences

from matching.algorithms import student_allocation
from matching.games import StudentAllocation

class CustomDictPrinter(dict):
    def __str__(self):
        return '\n'.join([f'{key}: {value}' for key, value in self.items()])

"""
students (dict)
    key: index/numbering of student
    value: (degree, selected_chairs)
"""
number_of_students = 50
students = generate_students(seed_value=42, count=number_of_students)

#print(students)
#print(get_number_of_master_students(students))

"""
data_group_based (dict)
    key: name of the chair
    value: a tuple (number_of_projects, number_of_projects_master)

data_project_based (dict)
    key: name of the chair
    value: a list of projects
"""
data_group_based, data_project_based = generate_projects_data(seed_value=1)

#print(get_number_of_projects_group_based(data_group_based))
#print(data_group_based)
#print(data_project_based)

"""Build supervisor_capacities"""
def build_supervisor_capacities(data_group_based, data_project_based):
    supervisor_capacities = {}

    for chair in data_group_based:
        supervisor_capacities[chair] = data_group_based[chair][0]

    for chair in data_project_based:
        supervisor_capacities[chair] = len(data_project_based[chair])

    return supervisor_capacities

supervisor_capacities = build_supervisor_capacities(data_group_based, data_project_based)
#print(supervisor_capacities)

"""Build project_supervisors"""
project_supervisors_group_based = get_project_supervisors_group_based(data_group_based)
project_supervisors_project_based = get_project_supervisors_project_based(data_project_based)

project_supervisors = {**project_supervisors_group_based, **project_supervisors_project_based}
#print(project_supervisors)

"""Build project_capacities"""
project_capacities_group_based = get_project_capacities_group_based(data_group_based)
project_capacities_project_based = {proj: 1 for proj in project_supervisors_project_based}

project_capacities = {**project_capacities_group_based, **project_capacities_project_based}
#print(project_capacities)

"""Build student_preferences"""
student_preferences = build_student_preferences(students, project_supervisors, seed_value=42)
student_preferences_printed = CustomDictPrinter(student_preferences)
print(student_preferences_printed)

"""Build supervisor_preferences"""
def find_keys_by_value(data_dict, search_string):
    matching_keys = [key for key, values in data_dict.items() if any(search_string in value for value in values)]
    return matching_keys

def get_part_before_parenthesis(input_string):
    parts = input_string.split('(')
    if len(parts) > 1:
        return parts[0].strip()
    else:
        return input_string

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

supervisor_preferences = build_supervisor_preferences(student_preferences, supervisor_capacities, seed_value=42)
#print(CustomDictPrinter(supervisor_preferences))


"""Apply matching algorithm"""
game = StudentAllocation.create_from_dictionaries(
    student_preferences,
    supervisor_preferences,
    project_supervisors,
    project_capacities,
    supervisor_capacities)

matching = student_allocation(game.students, game.projects, game.supervisors)

"""Extract information of the matching results"""
# Get the number of students being matched
students_matched = set()
for studs in matching.values():
    students_matched.update(studs)
students_matched = list(students_matched)

#matching_edges = [(stud, str(proj)) for proj, students_matched in matching.items() for stud in students_matched]

print(f'\nThere are {len(students_matched)} students got matched, out of {number_of_students}\n')

"""Print out matching results"""
print('The student-project correspondence: ')
matching_stud_proj = {stud: proj for proj, studs in matching.items() for stud in studs}
print(CustomDictPrinter(matching_stud_proj))
print('\n')

print('The project-students correspondence: ')
matching_proj_studs = {proj: studs for proj, studs in matching.items() if studs}
print(CustomDictPrinter(matching_proj_studs))