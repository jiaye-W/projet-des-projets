from dataclasses import dataclass

@dataclass
class SupervisorBase:
    ID: str
    user_first_name: str
    user_last_name: str
    user_email: str
    project_based: int  # 1=project-based, 0=group-based

"""
Example of supervisor
ID = 1729
user_first_name = Jiaye
user_last_name = Wei
user_email = jiaye.wei@epfl.ch
project_based = 0
"""

@dataclass
class GroupBasedSupervisor(SupervisorBase):
    number_bachelor: int
    bachelor_id: int
    number_master: int
    master_id: int
    number_undefined: int
    undefined_id: int

"""
Example of group-based supervisor
ID = 1729
user_first_name = Jiaye
user_last_name = Wei
user_email = jiaye.wei@epfl.ch
project_based = 0

number_bachelor = 2
bachelor_id = 14
number_master = 0
master_id = None
number_undefined = 3
undefined_id = 15
"""

@dataclass
class ProjectBasedSupervisor(SupervisorBase):
    project_ids: str
    project_types: str
    project_titles: str

"""
Example of project-based supervisor
ID = 1729
user_first_name = Jiaye
user_last_name = Wei
user_email = jiaye.wei@epfl.ch
project_based = 0

project_id = [5; 6; 7]
project_type = [bachelor; master; undefined]
project_title = [Brownian Motion; Category Theory; Functional Analysis]
"""

@dataclass
class Student:
    ID: int
    first_name: str
    last_name: str
    email: str
    sciper: int
    master: int  # 1 for master, 0 for bachelor

    first_choice: str
    second_choice: str
    third_choice: str
    fourth_choice: str
    fifth_choice: str

    # first_project_id: int
    # first_group_id: int

    # second_project_id: int
    # second_group_id: int

    # third_project_id: int
    # third_group_id: int

    # fourth_project_id: int
    # fourth_group_id: int

    # fifth_project_id: int
    # fifth_group_id: int