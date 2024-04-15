from dataclasses import dataclass

#TODO the interaction issue between the Project and Supervisor, because they use each other in their properties.
@dataclass(frozen=True)
class Project:
    index: int
    title: str = ''
    description: str = ''
    target_students: str = '' # bachelor, master, or undefined

@dataclass
class Supervisor:
    index: int
    email: str
    name: str
    is_chair: bool # chair (true) or non-chair (false)
    tracks: str
    num_projects: int
    courses: list[int] # required courses, <= 3

@dataclass
class SupervisorProjectBased(Supervisor):
    num_bachelor_projects: int
    num_master_projects: int
    num_undefined_projects: int
    projects: list[Project]

@dataclass
class SupervisorGroupBased(Supervisor):
    num_bachelor_projects: int
    num_master_projects: int
    num_undefined_projects: int

@dataclass(frozen=True)
class Student:
    index: int
    email: str
    degree: str # 'bachelor' or 'master'
    name: str # full name
    sciper: int # 6-digit number

    preferences: list[(int, str)] # sorted based on preferences
    grades: list[int] # key: Supervisor, value: list of grades (can be empty)