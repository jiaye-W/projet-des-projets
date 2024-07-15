from objects import Supervisor
from objects import df_supervisor_2

# if df_supervisor_1 is not None:
#     supervisors = []
#     for _, row in df_supervisor_1.iterrows():
#         supervisor = Supervisor(
#             user_id=row['User ID'],
#             user_first_name=row['User First Name'],
#             user_last_name=row['User Last Name'],
#             user_email=row['User Email'],
#             chair=row['Chair'],
#             chair_name=row['Chair Name'],
#             number_phd=row['Number phd'],
#             number_postdocs=row['Number postdocs'],
#             number_pdm=row['Number pdm'],
#             track=row['Track'],
#             course_req_1=row['Course req 1'],
#             course_req_2=row['Course req 2'],
#             course_req_3=row['Course req 3'],
#             course_req_4=row['Course req 4'],
#             course_req_5=row['Course req 5'],
#             course_req_6=row['Course req 6'],
#             project_based=row['Project Based'],
#             number_bachelor=row['Number Bachelor'],
#             number_master=row['Number Master'],
#             number_undefined=row['Number Undefined'],
#             project_type=row['Project Type'],
#             project_title=row['Project Title'],
#             project_desc=row['Project Desc']
#         )
#         supervisors.append(supervisor)
    
#     # Print out the first few Supervisor instances to verify
#     # for supervisor in supervisors[:5]:
#     #     print(supervisor)

# Filter out project-based rows
df_supervisor_2_project_based = df_supervisor_2.dropna(subset=['Project ID'])

# Filter out group-based rows
df_supervisor_2_group_based = df_supervisor_2.dropna(subset=['Group Based'])

supervisor_preferences = {}
supervisor_preferences_project_based = {}
supervisor_preferences_group_based = {}

# Group by Project ID and sort each group by Rank
for project_id, group in df_supervisor_2_project_based.groupby('Project ID'):
    sorted_group = group.sort_values(by='Rank')
    supervisor_preferences_project_based[f'Project-{int(project_id)}'] = ["Student-" + str(student_id) for student_id in sorted_group['Student ID']]

print(supervisor_preferences_project_based)
"""Project-Supervisors"""