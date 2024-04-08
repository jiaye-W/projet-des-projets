import gdown
import math
from dataclasses import dataclass
import pandas as pd
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from google.oauth2 import service_account
from googleapiclient.discovery import build

@dataclass(frozen=True)
class Project:
    title: str
    description: str
    target_students: str

@dataclass(frozen=True)
class Supervisor:
    name: str
    is_chair: bool # chair (true) or non-chair (false)
    num_projects: int
    courses: list[int] # required courses, <= 3

@dataclass(frozen=True)
class SupervisorProjectBased(Supervisor):
    projects: list[Project]

@dataclass(frozen=True)
class SupervisorGroupBased(Supervisor):
    num_master_projects: int

# Function to create supervisor selection question
def create_supervisor_selection_question(list_supervisors):
    form_id = '1BUrjIpvwT5SQzEAW61qhBTDr0XL5RP1DTRp-kkEjaEo'

    # Use gspread to access the Google Form
    # Authenticate with Google API
    
    service = build('forms', 'v1')

    # Retrieve the form
    response = service.forms().get(formId=form_id).execute()
    form = response['form']
    
    # Add a multiple-choice question
    sheet = form.get_sheet(0)
    sheet.append_row(['Please select your preferred supervisor for your project:'])
    
    # Populate options from the list_supervisors array
    for supervisor in list_supervisors:
        sheet.append_row([supervisor.name])

def prepare_file(url):
    # Download the file from Google Drive
    csv_content = gdown.download(url, quiet=False)
    df = pd.read_csv(csv_content)
    return df

def main():
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSq4ojmQailO4VAXs61pXaO8aTic2FTDLEuwKHrm5KHcShkkmxriqSDZwn9UNDwSgYvXNypWCh_SNJH/pub?output=csv'
    df = prepare_file(url)
    
    list_supervisors = []
    list_supervisors_master = []
    list_supervisors_bachelor = []

    #TODO: two things: 1. separate the bachelor and master 2. first project-based then group based (optional sorting)

    for index, row in df.iterrows():
        is_chair = True if row.iloc[2] == 'Chair' else False 

        name = row.iloc[-2] if is_chair else row.iloc[-1]

        courses = [row.iloc[-5], row.iloc[-4], row.iloc[-3]]
        courses = [int(x) for x in courses if not math.isnan(x)]

        if (row.iloc[4] == "project-based"):
            num_projects = int(row.iloc[6])

            projects = []
            master_projects = []
            bachelor_projects = []

            num_master_projects = 0
            num_bachelor_projects = 0
            
            for index in range(0, 8):
                start_col = 30 - index * 3

                target_students = row.iloc[start_col]
                if pd.notna(target_students):
                    description = row.iloc[start_col - 1]
                    title = row.iloc[start_col - 2]

                    projects.append(Project(title, description, target_students))

                    if target_students == 'Master':
                        num_master_projects += 1
                        master_projects.append(Project(title, description, target_students))

                    elif target_students == 'Bachelor':
                        num_bachelor_projects += 1
                        bachelor_projects.append(Project(title, description, target_students))

            supervisor = SupervisorProjectBased(name, is_chair, num_projects, courses, projects)
            
            if (num_master_projects != 0):
                list_supervisors_master.append(SupervisorProjectBased(name, is_chair, num_master_projects, courses, master_projects))

            if (num_bachelor_projects != 0):
                list_supervisors_bachelor.append(SupervisorProjectBased(name, is_chair, num_bachelor_projects, courses, bachelor_projects))

        else:
            num_projects = int(row.iloc[-7])
            num_master_projects = int(row.iloc[-6])
            num_bachelor_projects = num_projects - num_master_projects

            supervisor = SupervisorGroupBased(name, is_chair, num_projects, courses, num_master_projects)

            if (num_bachelor_projects != 0):
                list_supervisors_bachelor.append(supervisor)
            if (num_master_projects != 0):
                list_supervisors_master.append(supervisor)

        list_supervisors.append(supervisor)

    def sorted_key(sup):
        return 0 if isinstance(sup, SupervisorProjectBased) else 1
    
    list_supervisors_master = sorted(list_supervisors_master, key=sorted_key)
    list_supervisors_bachelor = sorted(list_supervisors_bachelor, key=sorted_key)

    # Writefile, print out the results. 
    with open('supervisor_form_1_bachelor.txt', 'w') as file:
        file.write('-' * 200 + '\n')
        sup_index = 1

        for sup in list_supervisors_bachelor:
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

    with open('supervisor_form_1_master.txt', 'w') as file:
        file.write('-' * 200 + '\n')
        sup_index = 1

        for sup in list_supervisors_master:
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
                file.write(f'{sup.num_master_projects} projects for master students.')
                file.write('\n' + '\n')

            file.write(f'Required courses: {sup.courses if sup.courses else None}' + '\n')
            file.write('\n')

            file.write('-' * 100 + '\n')

if __name__ == "__main__":
    main()