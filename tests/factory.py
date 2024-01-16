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
projects_group_based = {"ARG": (3, 2), "CAG": (4, 2), "TN": (3, 1), 
                        "DOLA": (3, 2), "PDE": (5, 3), "SCI-SB-JS": (4, 1),
                        "ANCHP": (6, 4), "CSFT": (4, 3), "MDS": (3, 2),
                        "DISOPT": (4, 1),
                        "UPHESS": (3, 2),
                        "CSQI": (4, 2), "MCSS": (5, 2),
                        "PROB": (4, 1), "PROPDE": (3, 2), 
                        "BIOSTAT": (3, 1), "SMAT": (4, 2)}

"""Project-based projects

    key: name of the chair
    value: a list of projects

    There will be (not implemented yet), a validation check of the pairs, so that it satisfies
    - mandatory capacity
    - bachelor obligation
"""
projects_project_based = {"EGG": [(1, "proj1-EGG", "bachelor"), (2, "proj2-EGG", "master")],
                          }

##TODO: do you want a mixed of those two types?

# Generated students
students = {}
number_of_students = 50


# generate two things: bachelor/master and research interest
def rng_degree():
    return 

def generate_students():
    number_of_students = 50
    number_of_projects = 100
    random.choice()

def generate_supervisors():
    return 0

