"""Generate projects information, which should in real case be read from Google forms of professor preferences."""

import random
import math
from sma import chairs

number_of_chairs_group_based = 19 # guess: more prof will choose group-based over project-based
bachelor_obligation = 0.25 # the precentage of projects which are available to bachelors

# empirical data
min_number_of_projects = 3
max_number_of_projects = 6

def generate_projects(seed_value):
    # set-up random
    random.seed(seed_value)

    # generate chairs who wish to choose group_based, sort the list
    chairs_group_based = sorted(random.sample(chairs, number_of_chairs_group_based))

    # take the set difference to get the chairs who wish to choose project_based, sort the list
    chairs_project_based = sorted(set(chairs).difference(set(chairs_group_based)))

    # create dict for storing generated data
    data_group_based = {}
    data_project_based = {}

    # group-based projects generation
    for chair in chairs_group_based:
        # generate the pair of numbers: (# of projects, # of projects for only masters)
        number_of_projects = random.randint(min_number_of_projects, max_number_of_projects) # depends on the capacity of chair but for now we don't have data
        number_of_projects_master_only = random.randint(0, math.floor(number_of_projects * (1-bachelor_obligation)))
        data_group_based[chair] = (number_of_projects, number_of_projects_master_only)

    # project-based projects generation
    

"""An example"""
example_data_group_based = {"ARG": (3, 2), "CAG": (4, 2), "TN": (3, 1), 
                    "DOLA": (3, 2), "PDE": (5, 3), "SCI-SB-JS": (4, 1),
                    "ANCHP": (6, 4), "CSFT": (4, 3), "MDS": (3, 2),
                    "DISOPT": (4, 1),
                    "UPHESS": (3, 2),
                    "CSQI": (4, 2), "MCSS": (5, 2),
                    "PROB": (4, 1), "PROPDE": (3, 2), 
                    "BIOSTAT": (3, 1), "SMAT": (4, 2)}
example_number_of_projects_group_based = sum(value[0] for value in example_data_group_based.values())

if __name__ == "__main__":
    generate_projects(seed_value=42)