"""
This is a simple example of how to use the matching library to solve a stable matching problem.
@author: Jiaye Wei <jiaye.wei@epfl.ch>
@Date: 28.04.2024
"""
from matching.algorithms import student_allocation
from matching.games import StudentAllocation

from collections import Counter

"""
The central objects are students and projects. 
Supervisors are created based on projects.

Projects
    Project-based projects: capacity = 1, corresponding to a single pseudo-supervisor.
    Group-based projects
        Bachelor projects: capacity = number of bachelor projects offered by the supervisor, corresponding to a single pseudo-supervisor.
        Master projects: capacity = number of master projects offered by the supervisor, corresponding to a single pseudo-supervisor.
        Undefined projects: capacity = number of undefined projects offered by the supervisor, corresponding to a single pseudo-supervisor.
"""

# Each student picks 3-5 projects
# We can use SCIPER as the key for each student
student_preferences = {
    "A": ["X3", "X2", "Z2"],
    "B": ["Y1", "X1", "Y2", "X2"],
    "C": ["X1", "Z1", "Z3"],
    "D": ["Z2", "Z4", "Y1", "Y2"],
    "E": ["X2", "X1", "X3", "Z3", "Y2"],
    "F": ["Z4", "X1", "X2", "Z1"]
}

supervisor_preferences = {
    "X": ["B", "C", "F", "A", "E"], 
    "Y": ["B", "E", "D"], 
    "Z": ["E", "F", "A", "C", "D"]
}

project_supervisors = {"X1": "X", "X2": "X", "X3": "X", 
                       "Y1": "Y", "Y2": "Y", 
                       "Z1": "Z", "Z2": "Z", "Z3": "Z", "Z4": "Z"}
project_capacities = {proj: 1 for proj in project_supervisors} # all-one
supervisor_capacities = dict(Counter(project_supervisors.values())) # should be the same as the name of project offered

game = StudentAllocation.create_from_dictionaries(
    student_preferences,
    supervisor_preferences,
    project_supervisors,
    project_capacities,
    supervisor_capacities)

matching = student_allocation(game.students, game.projects, game.supervisors, optimal='supervisor')

# result matching
print(matching)

# the size of matching
matching_size = sum(1 for value in matching.values() if value)
print(f"The size of the matching = {matching_size}")

# count the number of blocking edges


#TODO we need number of blocking edges, and size of the matching as information to evaluate it
#TODO from dictionary output (matching), draw a graph