import gdown
import math
import pandas as pd
from objects import *

#TODO: validations 
def automated_emails():
    return 0

def repetition_courses(): # check if the required courses are repeated
    
    return 0

def check_submission(): # check if someone has submitted or not
    """Need a list of supervisors who are supposed to submit the form.

    Returns:
        _type_: _description_
    """
    return 0

#TODO: separate these dataclasses into a new file and try to use them elsewhere (e.g., in the script processing-students.py)
def prepare_file(url):
    # Download the file from Google Drive
    csv_content = gdown.download(url, quiet=False)
    df = pd.read_csv(csv_content)
    return df

def sorted_key(sup):
    return 0 if isinstance(sup, SupervisorProjectBased) else 1

def build_supervisors():
    """
    File name: Supervisors-1 (Responses)
    Last update: 12.04.24

    There are 51 columns (0-50). 

    Basic information (0-6)
    0: timestamp
    1: email address
    2: chair or non-chair
    3: research areas (optional, could be deleted)
    4: identification for chair
    5: identification for non-chair
    6: project-based or group-based

    Project-based
    7: range of the number of projects, either 1~4 or 5~8
    8-15:
        Range 1~4 
            Required bachelor project (8-10)
            8: title
            9: description
            10: number of other projects, between 0 and 3
        Range 5~8:
            Required bachelor projects (11-15)
            11: title of 1st
            12: description of 1st
            13: title of 2nd
            14: description of 2nd
            15: number of other projects, between 3 and 6

    16-33: Details of other projects
    Each has 3 columns: 16-18, 19-21, 22-24, 25-27, 28-30, 31-33

    Group-based
    34: number of projects
    35-41: number of bachelor projects, for capacity from 2 to 8
    42-47: number of master projects
    
    Courses
    48: 1st course
    49: 2nd course
    50: 3rd course
    """

    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQMBJ__CI_S02nVV7citWOt15oVU21--nOuyHrJi0JnVN2bJqWUg5ElPy3ZY_7adBXfkxfTaHXvojCg/pub?output=csv'
    df = prepare_file(url)

    list_supervisors = []
    list_supervisors_master = []
    list_supervisors_bachelor = []

    index_bachelor_supervisor = 0
    index_master_supervisor = 0

    for index, row in df.iterrows(): # Index: unique label of supervisor
        # Email
        email = row.iloc[1]

        # Chair or non-chair
        is_chair = True if row.iloc[2] == 'Chair' else False 

        # Research areas (tracks)
        tracks = row.iloc[3]

        # Name (identification)
        name = row.iloc[4] if is_chair else row.iloc[5]

        # Three courses
        courses = [row.iloc[48], row.iloc[49], row.iloc[50]]
        courses = [int(x) for x in courses if not math.isnan(float(x))]

        if (row.iloc[6] == "project-based"):
            # Indices of projects
            index_bachelor = 0
            index_master = 0
            index_undefined = 0

            range_num_projects = row.iloc[7]

            bachelor_projects = []
            master_projects = []
            undefined_projects = []
            
            num_other_projects = 0
            # Add required bachelor project(s)
            if range_num_projects == '1 ~ 4':
                index_bachelor += 1
                bachelor_projects.append(Project(
                                        index=index_bachelor,
                                        title=row.iloc[8], 
                                        description=row.iloc[9], 
                                        target_students='bachelor'))
                num_other_projects = row.iloc[10]
            elif range_num_projects == '5 ~ 8':
                index_bachelor += 1
                bachelor_projects.append(Project(
                                        index=index_bachelor,
                                        title=row.iloc[11], 
                                        description=row.iloc[12], 
                                        target_students='bachelor'))
                index_bachelor += 1
                bachelor_projects.append(Project(
                                        index=index_bachelor,
                                        title=row.iloc[13], 
                                        description=row.iloc[14], 
                                        target_students='bachelor'))
                num_other_projects = row.iloc[15]
            
            # Add other projects, iterate backwards
            for index in range(0, int(num_other_projects)):
                start_col = 31 - 3 * index

                title = row.iloc[start_col]
                description = row.iloc[start_col + 1]
                target_students = row.iloc[start_col + 2]

                if target_students == 'Bachelor':
                    index_bachelor += 1
                    bachelor_projects.append(Project(index_bachelor, title, description, 'bachelor'))
                elif target_students == 'Master':
                    index_master += 1
                    master_projects.append(Project(index_master, title, description, 'master'))
                else: # undefined projects
                    index_undefined += 1
                    undefined_projects.append(Project(index_undefined, title, description, 'undefined'))
            
            projects = bachelor_projects + master_projects + undefined_projects
            num_projects = len(projects)
                
            supervisor_bachelor = SupervisorProjectBased(index, email, name, is_chair, tracks, num_projects - len(master_projects), courses, 
                                                         len(bachelor_projects), 0, len(undefined_projects), bachelor_projects + undefined_projects)
            supervisor_master = SupervisorProjectBased(index, email, name, is_chair, tracks, num_projects - len(bachelor_projects), courses, 
                                                       0, len(master_projects), len(undefined_projects), master_projects + undefined_projects)

        else:
            num_projects = int(row.iloc[34])
            num_bachelor_projects = int(row.iloc[33 + num_projects]) 
            num_master_projects = int(row.iloc[41 + num_projects - num_bachelor_projects])
            num_undefined_projects = num_projects - num_bachelor_projects - num_master_projects

            supervisor_bachelor = SupervisorGroupBased(index, email, name, is_chair, tracks, num_projects - num_master_projects, courses, 
                                                       num_bachelor_projects, 0, num_undefined_projects)
            supervisor_master = SupervisorGroupBased(index, email, name, is_chair, tracks, num_projects - num_bachelor_projects, courses, 
                                                     0, num_master_projects, num_undefined_projects)

        if (supervisor_bachelor.num_projects != 0):
            supervisor_bachelor.index = index_bachelor_supervisor
            list_supervisors_bachelor.append(supervisor_bachelor)
            index_bachelor_supervisor += 1

        if (supervisor_master.num_projects != 0):
            supervisor_master.index = index_master_supervisor
            list_supervisors_master.append(supervisor_master)
            index_master_supervisor += 1

    # Sort the supervisors: first project-based then group-based
    # list_supervisors_master = sorted(list_supervisors_master, key=sorted_key)
    # list_supervisors_bachelor = sorted(list_supervisors_bachelor, key=sorted_key)

    return list_supervisors_bachelor, list_supervisors_master

def results_writefile(list_supervisors, students):
    """Write the information of all supervisors to a file.
       Work for both bachelor and master projects. 

    Args:
        list_supervisors (list[Supervisor])
        students (str): either 'bachelor' or 'master'
    """
    
    address = f'src/interfaces/textual-outputs/supervisor_form_1_{students}.txt'

    with open(address, 'w') as file:
        file.write('-' * 200 + '\n')
        sup_index = 1

        for sup in list_supervisors:
            sup_type = 'project-based' if isinstance(sup, SupervisorProjectBased) else 'group-based'
            file.write('\n')
            file.write(f'{sup_index}. {sup.name} [{sup_type}]' + '\n')
            sup_index += 1

            file.write('\n')
            file.write(f'Research areas (tracks): {sup.tracks}' + '\n')

            file.write('\n')
            number_of_projects = sup.num_bachelor_projects if students == 'bachelor' else sup.num_master_projects
            number_of_projects += sup.num_undefined_projects
            file.write(f'There are {number_of_projects} projects for {students} students.' + '\n')

            if sup_type == 'project-based':
                file.write('\n')
                for proj in sup.projects:
                    if proj.target_students == students or proj.target_students == 'undefined':
                        file.write('\t' + f'Project {proj.index+1} ({proj.target_students})' + '\n')
                        file.write('\t' + f'Title: {proj.title}' + '\n')
                        file.write('\t' + f'Description: {proj.description}' + '\n\n')
            else:
                file.write('\n')

            file.write(f'Required courses: {sup.courses if sup.courses else None}' + '\n')
            file.write('\n')

            file.write('-' * 100 + '\n')

def convert_list_to_dict(list_supervisors):
    dict_supervisors = {}
    for sup in list_supervisors:
        dict_supervisors[sup.name] = sup
    return dict_supervisors

# if __name__ == "__main__":
#     list_supervisors_bachelor, list_supervisors_master = build_supervisors()

#     results_writefile(list_supervisors=list_supervisors_bachelor, students='bachelor')
#     results_writefile(list_supervisors=list_supervisors_master, students='master')

list_supervisors_bachelor, list_supervisors_master = build_supervisors()
dict_supervisors_bachelor = convert_list_to_dict(list_supervisors_bachelor)
dict_supervisors_master = convert_list_to_dict(list_supervisors_master)