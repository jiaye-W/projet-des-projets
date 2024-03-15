import gdown
import math
from dataclasses import dataclass
import pandas as pd

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

# Download the file from Google Drive
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT2TSn3joZFFrBeGShjgUHeTm5Zw1v3vPhxl53Wht0OVXDWAOtnZ_JbNrAgakmpJBOThZ00hUG5pyVV/pub?output=csv'
csv_content = gdown.download(url, quiet=False)

# Data processing!
df = pd.read_csv(csv_content)

list_supervisors = []

for index, row in df.iterrows():
    is_chair = True if row.iloc[2] == 'Chair' else False 

    name = row.iloc[-2] if is_chair else row.iloc[-1]

    courses = [row.iloc[-5], row.iloc[-4], row.iloc[-3]]
    courses = [int(x) for x in courses if not math.isnan(x)]

    if (row.iloc[4] == "project-based"):
        num_projects = int(row.iloc[6])

        projects = []
        
        for index in range(0, 8):
            start_col = 30 - index * 3

            target_students = row.iloc[start_col]
            if pd.notna(target_students):
                description = row.iloc[start_col - 1]
                title = row.iloc[start_col - 2]

                projects.append(Project(title, description, target_students))

        supervisor = SupervisorProjectBased(name, is_chair, num_projects, courses, projects)

    else:
        num_projects = int(row.iloc[-7])
        num_master_projects = int(row.iloc[-6])
        supervisor = SupervisorGroupBased(name, is_chair, num_projects, courses, num_master_projects)

    list_supervisors.append(supervisor)

for sup in list_supervisors:
    print(sup)
    print()

with open('supervisor_form_1.txt', 'w') as file:
    file.write('-' * 200 + '\n')
    sup_index = 1

    for sup in list_supervisors:
        sup_type = 'project-based' if isinstance(sup, SupervisorProjectBased) else 'group-based'
        file.write('\n')
        file.write(f'{sup_index}. {sup.name} ({sup_type})' + '\n')
        sup_index += 1

        file.write('\n')
        file.write(f'There are {sup.num_projects} many projects.' + '\n')

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
            file.write(f'{sup.num_master_projects} projects for master students, {sup.num_projects - sup.num_master_projects} projects for bachelor students.')
            file.write('\n' + '\n')

        file.write(f'Required courses: {sup.courses if sup.courses else None}' + '\n')
        file.write('\n')

        file.write('-' * 100 + '\n')