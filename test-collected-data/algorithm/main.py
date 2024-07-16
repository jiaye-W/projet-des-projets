from project_supervisors import project_supervisors, project_capacities, supervisor_capacities
from student_preferences import student_preferences
from supervisor_preferences import supervisor_preferences

from matching.algorithms import student_allocation
from matching.games import StudentAllocation


def print_dict_items(dictionary):
    """
    Print each item of the dictionary one per line.
    
    Parameters:
    dictionary (dict): The dictionary to print.
    """
    for key, value in dictionary.items():
        print(f"{key}: {value}")

# print(student_preferences)
# print(supervisor_preferences)
# print(project_supervisors)
# print(project_capacities)
# print(supervisor_capacities)

game = StudentAllocation.create_from_dictionaries(
    student_preferences,
    supervisor_preferences,
    project_supervisors,
    project_capacities,
    supervisor_capacities)

matching = student_allocation(game.students, game.projects, game.supervisors, optimal='student')

# result matching
print(matching)

# the size of matching
matching_size = sum(1 for value in matching.values() if value)
print(f"The size of the matching = {matching_size}")
