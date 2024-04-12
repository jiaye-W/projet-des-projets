from dataclasses import dataclass

@dataclass(frozen=True)
class Project:
    title: str
    description: str
    target_students: str # bachelor, master, or undefined

@dataclass(frozen=True)
class Supervisor:
    email: str
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

@dataclass(frozen=True)
class Student:
    degree: str # 'bachelor' or 'master'
    name: str # full name
    sciper: int # 6-digit number

    projects: list[Project] # sorted based on preferences
    