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

def update_preferences(student_prefs, supervisor_prefs):

    # Iterate over each student's project preferences
    for student, projects in student_prefs.items():
        for project in projects:
            supervisor_id = project.split('-', 1)[1]  # Split by the first "-"
            supervisor_key = f'Supervisor-{supervisor_id}'

            # Check if the supervisor has ranked the student
            if student not in supervisor_prefs[supervisor_key]:
                # Append the student to the end of the supervisor's preferences
                supervisor_prefs[supervisor_key].append(student)

    # # Iterate over each supervisor's student preferences
    # for supervisor, students in supervisor_prefs.items():
    #     for student in students:
    #         # Check if the student has ranked the supervisor
    #         if supervisor not in student_prefs[student]:
    #             # Append the student to the end of the supervisor's preferences
    #             student_prefs[student].append(supervisor)

    return student_prefs, supervisor_prefs

student_preferences, supervisor_preferences = update_preferences(student_preferences, supervisor_preferences)


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
write_dictionaries_to_file('results.txt', all_dictionaries)

# print("Missing supervisors for student projects:", missing_supervisors)
# print("Added students to supervisors' preference lists:")
# for student, project in added_to_supervisors:
#     print(f"{student} chose {project}, and was added to {project.split('-')[1]}'s preference list")

# print("\nUpdated supervisor preferences:")
# for supervisor, prefs in supervisor_preferences.items():
#     print(f"{supervisor}: {prefs}")

game = StudentAllocation.create_from_dictionaries(
    student_preferences,
    supervisor_preferences,
    project_supervisors,
    project_capacities,
    supervisor_capacities)

matching = student_allocation(game.students, game.projects, game.supervisors, optimal='student')

# result matching
print(len(student_preferences.keys()))

print_dict_items(matching)

# the size of matching
matching_size = sum(1 for value in matching.values() if value)
print(f"The size of the matching = {matching_size}")
