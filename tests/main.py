from data.sma import number_of_chairs

from data.students import generate_students
from data.students import get_number_of_master_students
from data.students import get_research_interest_counts

from data.projects import generate_projects_data
from data.projects import number_of_chairs_group_based
from data.projects import get_project_supervisors_group_based
from data.projects import get_project_supervisors_project_based
from data.projects import get_project_capacities_group_based

from student_preferences import build_student_preferences

from supervisor_preferences import build_supervisor_preferences

from plot import plot_example
from plot import plot_results

from matching.algorithms import student_allocation
from matching.games import StudentAllocation

class CustomDictPrinter(dict):
    def __str__(self):
        return '\n'.join([f'{key}: {value}' for key, value in self.items()])

def find_keys_by_value(data_dict, search_string):
        matching_keys = [key for key, values in data_dict.items() if any(search_string in value for value in values)]
        return matching_keys

def build_matching_example():
    # Set random seed
    user_input_str = input("Please enter the seed: ")
    try:
        seed = int(user_input_str)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

    # Set the number of students
    user_input_number_of_students = input("Please enter the number of students you want to generate: ")
    try:
        number_of_students = int(user_input_number_of_students)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

    # Generate students
    students = generate_students(seed_value=seed, count=number_of_students)
    number_of_master_students = get_number_of_master_students(students)
    number_of_bachelor_students = number_of_students - number_of_master_students

    research_interest_counts = get_research_interest_counts(students)

    with open('tests/results/texts/students.txt', 'w') as file:
        print(f'Generate {number_of_students} students.', file=file)
        print(f'There are {number_of_master_students} master students, {number_of_bachelor_students} bachelor students.', file=file)
        print(CustomDictPrinter(students), file=file)

        print('\nThe research interests of students: ', file=file)
        print(CustomDictPrinter(research_interest_counts), file=file)

    # Generate projects
    
    ## data_group_based (dict)
    ### key: name of the chair
    ### value: a tuple (number_of_projects, number_of_projects_master)

    ## data_project_based (dict)
    ### key: name of the chair
    ### value: a list of projects
    data_group_based, data_project_based = generate_projects_data(seed_value=seed)
    #print(get_number_of_projects_group_based(data_group_based))

    with open('tests/results/texts/projects.txt', 'w') as file:
        print(f'There are {number_of_chairs} chairs in SMA participating in the matching.', file=file)
        print(f'{number_of_chairs_group_based} of them choose to advertise in group-based and {number_of_chairs - number_of_chairs_group_based} of them choose to advertise in project-based.', file=file)
        
        print('\nThe group-based chairs are:', file=file)
        print(sorted(data_group_based.keys()), file=file)
        print('Details: ', file=file)
        for chair in data_group_based:
            pair = data_group_based[chair]
            print(f'{chair} has {pair[0]} projects, {pair[1]} for master and {pair[0]-pair[1]} for bachelor', file=file)
        
        print('\nThe project-based chairs are:', file=file)
        print(sorted(data_project_based.keys()), file=file)
        print('Details: ', file=file)
        for chair in data_project_based:
            list_of_projects = data_project_based[chair]
            print(f'{chair} has {len(list_of_projects)} projects', file=file)

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
    student_preferences = build_student_preferences(students, project_supervisors, seed_value=seed)
    student_preferences_printed = CustomDictPrinter(student_preferences)
    #print(student_preferences_printed)

    """Build supervisor_preferences"""
    supervisor_preferences = build_supervisor_preferences(student_preferences, supervisor_capacities, seed_value=seed)
    #print(CustomDictPrinter(supervisor_preferences))

    """Plot the matching instance"""
    plot_example(seed, number_of_students, project_supervisors, student_preferences)

    return student_preferences, supervisor_preferences, project_supervisors, project_capacities, supervisor_capacities

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
    students_matched = set()
    for studs in matching.values():
        students_matched.update(studs)
    students_matched = list(students_matched)

    #matching_edges = [(stud, str(proj)) for proj, students_matched in matching.items() for stud in students_matched]

    number_of_students = len(student_preferences.keys())

    with open('tests/results/texts/solution.txt', 'w') as file:
    # Redirect the output to the file
        print(f'There are {len(students_matched)} students got matched, out of {number_of_students}\n', file=file)

        """Print out matching results"""
        print('The student-project correspondence: ', file=file)
        matching_stud_proj = {stud: proj for proj, studs in matching.items() for stud in studs}
        print(CustomDictPrinter(matching_stud_proj), file=file)

        print('\nThe project-students correspondence: ', file=file)
        matching_proj_studs = {proj: studs for proj, studs in matching.items() if studs}
        print(CustomDictPrinter(matching_proj_studs), file=file)

        # plot the matching results
        plot_results(number_of_students, project_supervisors, student_preferences, matching)

if __name__ == '__main__':
    student_preferences, supervisor_preferences, project_supervisors, project_capacities, supervisor_capacities = build_matching_example()

    apply_matching_algorithm(student_preferences, 
                             supervisor_preferences, 
                             project_supervisors, 
                             project_capacities, 
                             supervisor_capacities)