from dataclasses import dataclass
import pandas as pd

df_supervisor_1 = pd.read_csv('test-collected-data/data/supervisor-1.csv')
df_student = pd.read_csv('test-collected-data/data/students.csv')
df_supervisor_2 = pd.read_csv('test-collected-data/data/supervisor-2.csv')

@dataclass
class Supervisor:
    ID: str

    user_first_name: str
    user_last_name: str
    user_email: str

    project_based: int # 1=project-based, 0=group-based

    # Only for group-based
    number_bachelor: int
    number_master: int
    number_undefined: int

    # Only for project-based, separated by commas
    project_type: str
    project_title: str
    project_desc: str

@dataclass
class Student:
    ID: int

    first_choice: str
    second_choice: str
    third_choice: str
    fourth_choice: str
    fifth_choice: str
    
    master: str # 1 for master, 0 for bachelor
