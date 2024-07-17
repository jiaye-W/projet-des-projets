import pandas as pd
import numpy as np
import math
from objects import Student
from helper import print_dict_items, download_and_process_csv

# URLs
url_supervisor_1 = 'https://sma-semester-projects.epfl.ch/export'
url_student = 'https://sma-semester-projects.epfl.ch/export_student'
url_supervisor_2 = 'https://sma-semester-projects.epfl.ch/export_results'

df_supervisor_1 = download_and_process_csv(url_supervisor_1)
df_student = download_and_process_csv(url_student)

# print(df_student)

def build_project_supervisors(df):
    return 0

def single_choice(project_id, group_id):
    if not np.isnan(project_id):
        return f"Project-based-{int(project_id)}"
    else:
        return f"Group-based-{int(group_id)}"
    
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
    """
    student_preferences = {}

    for _, row in df.iterrows():
        # student = Student(
        #     ID=row['ID'],
        #     first_name=row['First Name'],
        #     last_name=row['Last Name'],
        #     email=row['Email'],
        #     sciper=row['Sciper'],
        #     master=row['Master'],
            
        #     first_choice = single_choice(row['First ID'], row['First Group ID']),
        #     second_choice=single_choice(row['Second ID'], row['Second Group ID']),
        #     third_choice=single_choice(row['Third ID'], row['Third Group ID']),
        #     fourth_choice=single_choice(row['Fourth ID'], row['Fourth Group ID']),
        #     fifth_choice=single_choice(row['Fifth ID'], row['Fifth Group ID'])
        # )

        print(row['First ID'], row['First Group ID'])

        id = row['ID']
        first_choice = classify_pair(row['First ID'], row['First Group ID'])
        second_choice=classify_pair(row['Second ID'], row['Second Group ID'])
        third_choice=classify_pair(row['Third ID'], row['Third Group ID'])
        fourth_choice=classify_pair(row['Fourth ID'], row['Fourth Group ID'])
        fifth_choice=classify_pair(row['Fifth ID'], row['Fifth Group ID'])

        student_preferences[f"Student-{id}"] = [first_choice, 
                                                second_choice,
                                                third_choice,
                                                fourth_choice,
                                                fifth_choice]
        
    return student_preferences

if __name__ == '__main__':
    print(df_student)
    print_dict_items(build_student_preferences(df_student))