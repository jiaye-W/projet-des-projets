# Remark: so far the information are retrieved from the last csv file (supervisor-2.csv), only for the testing
# Eventually we will get this information directly from the first csv file (supervisor-1.csv)

import pandas as pd
from objects import df_supervisor_1, df_supervisor_2

# Initialize the required dictionaries
project_supervisors = {}
project_capacities = {}
supervisor_capacities = {}

# Group-based, from supervisor-1.csv
df_supervisor_1_group_based = df_supervisor_1[df_supervisor_1['Project Based'] == 0]
for _, row in df_supervisor_1_group_based.iterrows():
    name = row['User Last Name']

    if pd.notna(row['Number Bachelor']):
        num_bachelor_projects = row['Number Bachelor']
        bachelor_project = f'Project-{name}-bachelor'

        project_supervisors[bachelor_project] = f'Supervisor-{name}-bachelor'
        project_capacities[bachelor_project] = int(num_bachelor_projects)
        supervisor_capacities[f'Supervisor-{name}-bachelor'] = int(num_bachelor_projects)

    if pd.notna(row['Number Master']):
        num_master_projects = row['Number Master']
        master_project = f'Project-{name}-master'

        project_supervisors[master_project] = f'Supervisor-{name}-master'
        project_capacities[master_project] = int(num_master_projects)
        supervisor_capacities[f'Supervisor-{name}-master'] = int(num_master_projects)

    if pd.notna(row['Number Undefined']):
        num_undefined_projects = row['Number Undefined']
        undefined_project = f'Project-{name}-undefined'

        project_supervisors[undefined_project] = f'Supervisor-{name}-undefined'
        project_capacities[undefined_project] = int(num_undefined_projects)
        supervisor_capacities[f'Supervisor-{name}-undefined'] = int(num_undefined_projects)

# Project-based, from supervisor-2.csv
project_based_projects = df_supervisor_2['Project ID'].dropna().unique()
project_based_projects = [int(id) for id in project_based_projects]

## Manually fixing
project_based_projects.append(int(21))

for project in project_based_projects:
    project_supervisors[f'Project-{project}'] = f'Supervisor-{project}'
    project_capacities[f'Project-{project}'] = 1
    supervisor_capacities[f'Supervisor-{project}'] = 1