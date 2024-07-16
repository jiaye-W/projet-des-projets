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

def get_ordinal_suffix(number):
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return suffix

class CustomDictPrinter(dict):
    def __str__(self):
        return '\n'.join([f'{key}: {value}' for key, value in self.items()])

def apply_matching_algorithm(student_preferences,
                             supervisor_preferences,
                             project_supervisors,
                             project_capacities,
                             supervisor_capacities):
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
    number_of_students = len(student_preferences.keys())

    students_matched = set()
    for studs in matching.values():
        students_matched.update(studs)

    students_unmatched = set(game.students).difference(students_matched)
    students_unmatched = list(students_unmatched)
    students_matched = list(students_matched)

    #matching_edges = [(stud, str(proj)) for proj, students_matched in matching.items() for stud in students_matched]

    with open('solution.txt', 'w') as file:
    # Redirect the output to the file
        print(f'There are {len(students_matched)} students got matched, out of {number_of_students}\n', file=file)

        print(f'Unmatched student(s): {", ".join(map(str, students_unmatched))}' if students_unmatched
              else 'Every students are matched!', 
              file=file)

        """Print out matching results"""
        print('\nThe student-project correspondence: ', file=file)

        number_of_students_got_first_pick = 0
        number_of_students_got_second_pick = 0
        number_of_students_got_third_pick = 0

        matching_stud_proj = {stud: proj for proj, studs in matching.items() for stud in studs}
        for stud in matching_stud_proj:
            proj = matching_stud_proj[stud]
            prefs_list = student_preferences[f'{stud}']
            which_pick = prefs_list.index(f'{proj}')+1

            if which_pick == 1:
                number_of_students_got_first_pick += 1
            if which_pick == 2:
                number_of_students_got_second_pick += 1
            if which_pick == 3:
                number_of_students_got_third_pick += 1

            print(f'{stud} : {proj}, his/her {which_pick}{get_ordinal_suffix(which_pick)} choice', file=file)
        
        print(f'\nNumber of students got matched = {len(students_matched)} ({round(len(students_matched) * 100 / number_of_students, 2)}%)', file=file)
        print(f'Number of students got matched to their 1st choice = {number_of_students_got_first_pick} ({round(number_of_students_got_first_pick * 100 / number_of_students, 2)}%)', file=file)
        print(f'Number of students got matched to their 2nd choice = {number_of_students_got_second_pick} ({round(number_of_students_got_second_pick * 100 / number_of_students, 2)}%)', file=file)
        print(f'Number of students got matched to their 3rd choice = {number_of_students_got_third_pick} ({round(number_of_students_got_third_pick * 100 / number_of_students, 2)}%)', file=file)

        file.write('\n' + '-' * 100 + '\n')

        print('\nThe project-students correspondence: ', file=file)
        matching_proj_studs = {proj: studs for proj, studs in matching.items() if studs}
        print(CustomDictPrinter(matching_proj_studs), file=file)

        file.write('\n' + '-' * 100 + '\n')

if __name__ == '__main__':
    apply_matching_algorithm(student_preferences, 
                             supervisor_preferences, 
                             project_supervisors, 
                             project_capacities, 
                             supervisor_capacities)