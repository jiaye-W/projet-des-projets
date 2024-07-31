import pandas as pd
import numpy as np
import math
from typing import Union, List
from objects import Student
from helper import print_dict_items, download_and_process_csv

def processing_project_ids(item: Union[str, int, float]) -> List[int]:
    """
    Split the field of project IDs by semicolon and convert each element to an integer.

    Args:
        item (Union[str, int, float]): A string containing project IDs separated by semicolons,
                                       or a single float or int.

    Returns:
        List[int]: A list of project IDs as integers. If there is only one ID, it returns a list
                   with that single ID as an integer.

    Raises:
        ValueError: If the input is a float NaN or contains non-integer values in string format.
    """
    if isinstance(item, (int, float)):
        if math.isnan(item):
            raise ValueError("Input cannot be NaN.")
        # If item is a float or int, convert to int and return as a single-element list
        return [int(item)]
    elif isinstance(item, str):
        if ';' in item:
            try:
                # Split by semicolon and convert each element to an integer
                return [int(x) for x in item.split(';')]
            except ValueError:
                raise ValueError("String contains non-integer values.")
        else:
            try:
                # Convert the single item to an integer and return it as a single-element list
                return [int(item)]
            except ValueError:
                raise ValueError("String contains non-integer value.")
            
# Example usage:
# processing_project_ids("1;2;3") -> [1, 2, 3]
# processing_project_ids("4") -> [4]
# processing_project_ids(5) -> [5]
# processing_project_ids(6.0) -> [6]
# processing_project_ids(float('nan')) -> Raises ValueError

def build_project_supervisors(df):
    """Build up the three required dicts for matching and some other useful info

    Args:
        df (dataframe): data collected from the 1st supervisor form, df_supervisor_1

    Returns:
        Required by the matching algorithm:
            project_supervisors (dict)
            project_capacities (dict)
            supervisor_capacities (dict)

        Required to retrieve information:
            TBD (do it after you have found a stable matching! Then you can retrieve data without worrying about the results.)
    """

    project_supervisors = {}
    project_capacities = {}
    supervisor_capacities = {}

    for _, row in df.iterrows():
        #TODO create Supervisor object

        id = int(row['User ID'])
        last_name = str(row['User Last Name'])
        project_based = int(row['Project Based'])

        # Project-based
        if project_based == 1: 
            project_ids = processing_project_ids(row['Project Ids'])

            # Add "Project-" in front of each project ID
            projects = [f"Project-{num}" for num in project_ids]

            for proj in projects:
                project_supervisors[proj] = f"Supervisor-{proj}"
                project_capacities[proj] = 1
                supervisor_capacities[f"Supervisor-{proj}"] = 1
        
        # Group-based
        else: 
            if not pd.isna(row['Group Id Bachelor']):
                bachelor_project = f"Group-{int(row['Group Id Bachelor'])}"
                bachelor_capacity = int(row['Number Bachelor'])

                project_supervisors[bachelor_project] = f"Supervisor-{bachelor_project}"
                project_capacities[bachelor_project] = bachelor_capacity
                supervisor_capacities[f"Supervisor-{bachelor_project}"] = bachelor_capacity

            if not pd.isna(row['Group Id Master']):
                master_project = f"Group-{int(row['Group Id Master'])}"
                master_capacity = int(row['Number Master'])

                project_supervisors[master_project] = f"Supervisor-{master_project}"
                project_capacities[master_project] = master_capacity
                supervisor_capacities[f"Supervisor-{master_project}"] = master_capacity

            if not pd.isna(row['Group Id Undefined']):
                undefined_project = f"Group-{int(row['Group Id Undefined'])}"
                undefined_capacity = int(row['Number Undefined'])

                project_supervisors[undefined_project] = f"Supervisor-{undefined_project}"
                project_capacities[undefined_project] = undefined_capacity
                supervisor_capacities[f"Supervisor-{undefined_project}"] = undefined_capacity

    return project_supervisors, project_capacities, supervisor_capacities

# def single_choice(project_id, group_id):
#     if not np.isnan(project_id):
#         return f"Project-based-{int(project_id)}"
#     else:
#         return f"Group-based-{int(group_id)}"
    
def classify_pair(first, second):
    if not math.isnan(first):
        return f"Project-based-{int(first)}"
    elif not math.isnan(second):
        return f"Group-based-{int(second)}"
    else:
        return "Both values are nan"
    
def build_student_preferences(df):
    """Build the dict student_preferences from the dataframe of df_student

    Args:
        df (dataframe): _description_

    Returns:
        _type_: _description_
    """
    student_preferences = {}

    for _, row in df.iterrows():

        id = row['ID']
        first_choice=classify_pair(row['First ID'], row['First Group ID'])
        second_choice=classify_pair(row['Second ID'], row['Second Group ID'])
        third_choice=classify_pair(row['Third ID'], row['Third Group ID'])
        fourth_choice=classify_pair(row['Fourth ID'], row['Fourth Group ID'])
        fifth_choice=classify_pair(row['Fifth ID'], row['Fifth Group ID'])

        student = Student(
            ID=id,
            first_name=row['First Name'],
            last_name=row['Last Name'],
            email=row['Email'],
            sciper=row['Sciper'],
            master=row['Master'],
            first_choice=first_choice,
            second_choice=second_choice,
            third_choice=third_choice,
            fourth_choice=fourth_choice,
            fifth_choice=fifth_choice
        )

        student_preferences[f"Student-{id}"] = [first_choice, 
                                                second_choice,
                                                third_choice,
                                                fourth_choice,
                                                fifth_choice]
        
    return student_preferences

if __name__ == '__main__':
    # URLs (Need EPFL VPN to download!)
    url_supervisor_1 = 'https://sma-semester-projects.epfl.ch/export'
    url_student = 'https://sma-semester-projects.epfl.ch/export_student'
    url_supervisor_2 = 'https://sma-semester-projects.epfl.ch/export_results'

    df_supervisor_1 = download_and_process_csv(url_supervisor_1)
    df_student = download_and_process_csv(url_student)
    
    print(df_supervisor_1)
    # print(df_student)

    # Build up dicts and writefile
    project_supervisors, project_capacities, supervisor_capacities = build_project_supervisors(df_supervisor_1)
    with open('src/actual_run/results/algo_inputs.txt', 'w') as file:
        file.write('-' * 100 + '\n')
        file.write("Project-Supervisors\n\n")
        for key, value in project_supervisors.items():
            file.write(f"{key}: {value}\n")
        
        file.write('\n' + '-' * 100 + '\n')
        file.write("Project-Capacities\n\n")
        for key, value in project_capacities.items():
            file.write(f"{key}: {value}\n")

        file.write('\n' + '-' * 100 + '\n')
        file.write("Supervisor-Capacities\n\n")
        for key, value in supervisor_capacities.items():
            file.write(f"{key}: {value}\n")
    