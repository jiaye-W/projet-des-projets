"""
Processing students' responses

@author: Jiaye Wei <jiaye.wei@epfl.ch>
@Date: 09.04.2024
"""

import gdown
from processing_supervisors_1 import list_supervisors_bachelor, list_supervisors_master
from processing_supervisors_1 import dict_supervisors_bachelor, dict_supervisors_master
from processing_supervisors_1 import convert_list_to_dict
from objects import *
import pandas as pd
import re

def remove_between_square_brackets_and_space(text):
    return re.sub(r'\[[^\]]*\]\s*', '', text)

#TODO: validations 
def check_grades():  # Check if the grades are the same if entered multiple times. 
    return 0

def main():
    return 0

def prepare_file(url):
    """Pre-processing of students' responses, which should work for both bachelor and master students.

    Args:
        url (string): _description_

    Returns:
        df (dataframe): _description_
    """
    # Download the file from Google Drive
    csv_content = gdown.download(url, quiet=False)
    df = pd.read_csv(csv_content)

    return df   

def get_info_columns(list_supervisors):
    """Get the information of columns of bachelor/master forms.  

    Args:
        list_supervisors (_type_): _description_

    Returns:
        _type_: _description_
    """
    list_columns = [] # index of project, course1, course2, course3 (can be NaN)
    index = 0 # the relative index, within one choice (there are 5 choices)

    for sup in list_supervisors:
        if isinstance(sup, SupervisorProjectBased):
            index += 1
            index_project = index
        else:
            index_project = -1 

        courses = sup.courses
        indices_courses = [-1, -1, -1]
        if len(courses) == 1:
            index += 1
            indices_courses = [index, -1, -1]
        elif len(courses) == 2:
            index += 1
            indices_courses[0] = index
            index += 1
            indices_courses[1] = index
        elif len(courses) == 3:
            index += 1
            indices_courses[0] = index
            index += 1
            indices_courses[1] = index
            index += 1
            indices_courses[2] = index
        
        list_columns.append((index_project, indices_courses))
            
    return list_columns

def info_extraction(df, list_supervisors, target_students):
    """Get information from the raw data

    Args:
        df (dataframe): _description_
        target_students (str): 'bachelor' or 'master'

        Columns interpretation
            Basic (0-4)
            0: timestamp
            1: email address
            2: first name
            3: last name
            4: SCIPER

        5 same units, 
        where each unit contains (can get these information from supervisor-form-1):
            1 col for choosing one supervisor, then:
                1 col for choosing projects (only for project-based),  
                0-3 cols for grades of courses

    Returns:
        _type_: _description_
    """
    dict_supervisors = convert_list_to_dict(list_supervisors)
    list_columns = get_info_columns(list_supervisors)

    students = [] #TODO What's the best way of storing students?

    num_cols = df.shape[1]
    num_cols_one_choice = int(num_cols/5) - 1 # The number of columns of one unit!

    for index, row in df.iterrows():
        email = row.iloc[1]
        name = row.iloc[2] + ' ' + row.iloc[3]
        sciper = row.iloc[4]

        # Build up preferences of student, iterate over choices from 1st to 5th
        preferences = [] 
        grades = {}

        for i in range(5):
            # The starting index of this choice
            index_choice = 5 + i * num_cols_one_choice
            supervisor_name = row.iloc[index_choice]

            if not pd.isna(supervisor_name): # if the student chooses sth for this choice, start processing
                supervisor_name = remove_between_square_brackets_and_space(supervisor_name)
                supervisor = dict_supervisors[supervisor_name]
                supervisor_index = supervisor.index

                # Extract the supervisor information
                (index_project, indices_courses) = list_columns[supervisor_index]

                if isinstance(supervisor, SupervisorProjectBased):
                    project = row.iloc[index_choice + index_project]
                else:
                    project = Project(index=-1)
                preferences.append((supervisor.index, project))

                grades[supervisor_index] = [row.iloc[index_choice + index_course] if index_course!= -1 else -1 
                                            for index_course in indices_courses]

        student = Student(index=index+1, email=email, degree=target_students, name=name, sciper=sciper, 
                          preferences=preferences, grades=grades)
        print(student.preferences)
        print(student.grades)
        students.append(student)

    return students

if __name__ == "__main__":
    # File/Share/Publish to web, then choose csv format
    bachelor_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSYD5ebGfBTe0vFr6xBmw9bn3E1zmObFjJJz6AdMJUux7NyhCXPHZZ9Ks1XAXP8zZNT8CdtaSmX8j_K/pub?output=csv'
    master_url = ''

    df = prepare_file(bachelor_url)

    bachelor_students = info_extraction(df, list_supervisors_bachelor, target_students='bachelor')

    # print(bachelor_students)
    # print(get_info_columns(list_supervisors_bachelor))
    # print(get_info_columns(list_supervisors_master))

    #TODO: 