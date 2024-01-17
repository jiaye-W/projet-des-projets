"""
The matching factory which contains tests data 

Created on: 13.01.2024

@author: Jiaye Wei <jiaye.wei@epfl.ch>
"""

import random

# All chairs at SMA
# source: https://www.epfl.ch/schools/sb/research/math/research/
research = {"Algebra and Number Theory": ["ARG", "CAG", "EGG", "ERG", "GR-TES", "TAN", "TN"],
            "Analysis": ["AMCV", "CSFT", "DOLA", "PDE", "TAN", "CMGR", "ERG", "SCI-SB-JS", "PROPDE"],
            "Data Science and Learning": ["ANCHP", "BIOSTAT", "CSFT", "DOLA", "Deparis-Group", "LCVMM", "MCSS", "MDS", "OPTIM", "SDS", "SMAT", "STAT"],
            "Discrete Mathematics": ["DISOPT", "ERG", "MDS"],
            "Geometry and Topology": ["ARG", "CAG", "EGG", "CMGR", "GR-TR", "UPHESS"],
            "Mathematics in Computational Sciences": ["ANCHP", "CSQI", "Deparis-Group", "GR-PI", "LCVMM", "MCSS", "MNS", "OPTIM"],
            "Probability and Statistics": ["CSFT", "PROB", "PRST", "RGM", "SMAT", "STOAN", "PROPDE"],
            "Statistics": ["BIOSTAT", "DOLA", "MDS", "OPTIM", "SDS", "SMAT", "STAT"]}
#TODO maybe a relation matrix between research areas?? (incidence matrix)

research_areas = list(research.keys())
chairs = list(set(value for values_list in research.values() for value in values_list))


"""Group-based projects

    key: name of the chair
    value: a pair (number of projects, number of projects ONLY for master students)

    There will be (not implemented yet), a validation check of the pairs, so that it satisfies
    - mandatory capacity
    - bachelor obligation
"""
# The raw data from the Google form
data_group_based = {"ARG": (3, 2), "CAG": (4, 2), "TN": (3, 1), 
                    "DOLA": (3, 2), "PDE": (5, 3), "SCI-SB-JS": (4, 1),
                    "ANCHP": (6, 4), "CSFT": (4, 3), "MDS": (3, 2),
                    "DISOPT": (4, 1),
                    "UPHESS": (3, 2),
                    "CSQI": (4, 2), "MCSS": (5, 2),
                    "PROB": (4, 1), "PROPDE": (3, 2), 
                    "BIOSTAT": (3, 1), "SMAT": (4, 2)}
number_of_projects_group_based = sum(value[0] for value in data_group_based.values())
# naming of project of group-based projects: "ARG-1", "ARG-2", "ARG-3", "CAG-1", etc
# also have to contain the degree requirement: "ARG-1", 

def get_group_based_project_supervisors(data_group_based):
    """_summary_

    Args:
        data_group_based (_type_): raw data gathering from Google forms

    Returns:
        _type_: _description_
    """
    group_based_project_supervisors = {}

    for chair in data_group_based:
        # read the pair of numbers: (# of projects, # of projects for only masters)
        (number_of_projects, number_of_projects_only_masters) = data_group_based[chair]

        for i in range(1, number_of_projects+1):
            if (i <= number_of_projects_only_masters):
                group_based_project_supervisors[f"{chair}-proj-{i} (only master)"] = chair
            else:
                group_based_project_supervisors[f"{chair}-proj-{i}"] = chair

    return group_based_project_supervisors

# Build up projects from dict 

"""Project-based projects

    key: name of the chair
    value: a list of projects

    There will be (not implemented yet), a validation check of the pairs, so that it satisfies
    - mandatory capacity
    - bachelor obligation
"""
projects_project_based = {"EGG": [(1, "proj1-EGG", "bachelor"), (2, "proj2-EGG", "master")], 
                          "ERG": [(1, "proj1-ERG", "master"), (2, "proj2-ERG", "master"), (3, "proj3-ERG", "bachelor"), (4, "proj4-ERG", "master")]}
number_of_projects_project_based = sum(len(value) for value in projects_project_based.values())

number_of_projects = number_of_projects_group_based + number_of_projects_project_based

##TODO: do you want a mixed of those two types?

# Generated students
number_of_students = 50

# generate two things: bachelor/master and research interest
def generate_students(count):
    """_summary_

    Args:
        count (_type_): _description_

    Returns:
        _type_: _description_
    """

    students = {}

    # Set-up of RNG
    seed_value = 42
    random.seed(seed_value)

    for i in range(1, count+1):
        degree = generate_degree_of_student(random, probability_of_master=0.7)
        research_interest = random.choice(research_areas)
        students[i] = (degree, research_interest)

    #print(students)
    return students


def generate_degree_of_student(random, probability_of_master):
    """A biased coin which generates the degree of student, either bachelor or master

    Args:
        random (_type_): _description_
        probability_of_master (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Generate a random float in the range [0.0, 1.0)
    random_value = random.random()

    # Check if the random value is less than the probability_of_heads
    if random_value < probability_of_master:
        return "master"
    else:
        return "bachelor"

if __name__ == "__main__":
    #generate_students(number_of_students)
    get_group_based_project_supervisors(data_group_based)