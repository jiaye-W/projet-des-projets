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


# Function to write dictionaries to a file
def write_dictionaries_to_file(filename, dictionaries):
    with open(filename, 'w') as file:
        for dict_name, dictionary in dictionaries.items():
            file.write(f"{dict_name}:\n")
            for key, value in dictionary.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")  # Add a newline to separate dictionaries

# Dictionary containing all dictionaries to be written
all_dictionaries = {
    "student_preferences": student_preferences,
    "supervisor_preferences": supervisor_preferences,
    "project_supervisors": project_supervisors,
    "project_capacities": project_capacities,
    "supervisor_capacities": supervisor_capacities
}

# Writing dictionaries to the file
write_dictionaries_to_file('dictionaries.txt', all_dictionaries)