"""
Processing students' responses

@author: Jiaye Wei <jiaye.wei@epfl.ch>
@Date: 09.04.2024
"""

import gdown
from processing_supervisors_1 import dict_supervisors_bachelor, dict_supervisors_master
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

def info_extraction(df, dict_supervisors, target_students):
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
    students = [] #TODO what's the best way of storing students?

    num_cols = df.shape[1]
    num_cols_one_choice = int(num_cols/5) -1 # The number of columns of one unit!

    for index, row in df.iterrows():
        email = row.iloc[1]
        name = row.iloc[2] + ' ' + row.iloc[3]
        sciper = row.iloc[4]

        # Build up preferences of student, iterate over choices from 1st to 5th
        preferences = {}
        for i in range(5):
            supervisor_name = row.iloc[5 + i * num_cols_one_choice]

            if not pd.isna(supervisor_name):
                supervisor_name = remove_between_square_brackets_and_space(supervisor_name)
                supervisor = dict_supervisors[supervisor_name]

                is_project_based = isinstance(supervisor, SupervisorProjectBased)
                #TODO to get project from there we then need to make sure the title is unique
                project = 0 # all string entries, other are grades.
                preferences[i+1] = (supervisor, ) 

        student = Student(index=index+1, email=email, degree=target_students, name=name, sciper=sciper, 
                          preferences=preferences)
        students.append(student)

    return students

if __name__ == "__main__":
    # File/Share/Publish to web, then choose csv format
    bachelor_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRXVXgoqAlirUatREsroSNSnpRofqJXqrT5S5YPC1NhNzkuL2u_MBj8TmOWtW8PSYX7EkRcJr8lgYU_/pub?output=csv'
    master_url = ''

    df = prepare_file(bachelor_url)

    info_extraction(df, dict_supervisors_bachelor, target_students='bachelor')

    