import gdown
import math
import pandas as pd
from objects import *

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
    There are 45 columns (0-44). 

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
    35-41: number of bachelor projects for capacity from 2 to 8
    
    Courses
    42: 1st course
    43: 2nd course
    44: 3rd course
    """

    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSq4ojmQailO4VAXs61pXaO8aTic2FTDLEuwKHrm5KHcShkkmxriqSDZwn9UNDwSgYvXNypWCh_SNJH/pub?output=csv'
    df = prepare_file(url)

    list_supervisors = []
    list_supervisors_master = []
    list_supervisors_bachelor = []

    for index, row in df.iterrows():
        # email
        email = row.iloc[1]

        # chair or non-chair
        is_chair = True if row.iloc[2] == 'Chair' else False 

        # name (identification)
        name = row.iloc[4] if is_chair else row.iloc[5]

        # three courses
        courses = [row.iloc[42], row.iloc[43], row.iloc[44]]
        courses = [int(x) for x in courses if not math.isnan(float(x))]

        if (row.iloc[6] == "project-based"):
            range_num_projects = row.iloc[7]

            # num_projects = int(row.iloc[6])

            # projects = []
            master_projects = []
            bachelor_projects = []

            # num_master_projects = 0
            # num_bachelor_projects = 0

            num_other_projects = 0

            # Add required bachelor project(s)
            if range_num_projects == '1 ~ 4':
                bachelor_projects.append(Project(title=row.iloc[8], 
                                        description=row.iloc[9], 
                                        target_students='Bachelor'))
                num_other_projects = row.iloc[10]

                # num_bachelor_projects += 1

            elif range_num_projects == '5 ~ 8':
                bachelor_projects.append(Project(title=row.iloc[11], 
                                        description=row.iloc[12], 
                                        target_students='Bachelor'))
                bachelor_projects.append(Project(title=row.iloc[13], 
                                        description=row.iloc[14], 
                                        target_students='Bachelor'))
                num_other_projects = row.iloc[15]

                # num_bachelor_projects += 2
            
            # Add other projects, iterate backwards
            for index in range(0, int(num_other_projects)):
                start_col = 31 - 3 * index

                title = row.iloc[start_col]
                description = row.iloc[start_col + 1]
                target_students = row.iloc[start_col + 2]

                # projects.append(Project(title, description, target_students))

                if target_students == 'Master':
                    num_master_projects += 1
                    master_projects.append(Project(title, description, target_students))

                elif target_students == 'Bachelor':
                    num_bachelor_projects += 1
                    bachelor_projects.append(Project(title, description, target_students))
            
            projects = bachelor_projects + master_projects
            num_projects = len(projects)

            supervisor = SupervisorProjectBased(email, name, is_chair, num_projects, courses, projects)
            
            if (num_master_projects != 0):
                list_supervisors_master.append(SupervisorProjectBased(email, name, is_chair, num_master_projects, courses, master_projects))

            if (num_bachelor_projects != 0):
                list_supervisors_bachelor.append(SupervisorProjectBased(email, name, is_chair, num_bachelor_projects, courses, bachelor_projects))

        else:
            num_projects = int(row.iloc[34])
            num_bachelor_projects = int(row.iloc[33 + num_projects])
            num_master_projects = num_projects - num_bachelor_projects

            supervisor = SupervisorGroupBased(email, name, is_chair, num_projects, courses, num_master_projects)

            if (num_bachelor_projects != 0):
                list_supervisors_bachelor.append(supervisor)
            if (num_master_projects != 0):
                list_supervisors_master.append(supervisor)

        list_supervisors.append(supervisor)

    # Sort the supervisors: first project-based then group-based
    list_supervisors_master = sorted(list_supervisors_master, key=sorted_key)
    list_supervisors_bachelor = sorted(list_supervisors_bachelor, key=sorted_key)

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
            file.write(f'{sup_index}. {sup.name} ({sup_type})' + '\n')
            sup_index += 1

            file.write('\n')
            file.write(f'There are {sup.num_projects} projects.' + '\n')

            if sup_type == 'project-based':
                file.write('\n')
                proj_index = 1
                for proj in sup.projects:
                    file.write('\t' + f'Project {proj_index} ({proj.target_students})' + '\n')
                    file.write('\t' + f'Title: {proj.title}' + '\n')
                    file.write('\t' + f'Description: {proj.description}' + '\n')
                    file.write('\n')
                    proj_index += 1

            else:
                file.write(f'{sup.num_projects - sup.num_master_projects} projects for bachelor students.')
                file.write('\n' + '\n')

            file.write(f'Required courses: {sup.courses if sup.courses else None}' + '\n')
            file.write('\n')

            file.write('-' * 100 + '\n')

if __name__ == "__main__":
    list_supervisors_bachelor, list_supervisors_master = build_supervisors()

    results_writefile(list_supervisors=list_supervisors_bachelor, students='bachelor')
    results_writefile(list_supervisors=list_supervisors_master, students='master')