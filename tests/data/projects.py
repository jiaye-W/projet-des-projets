"""Generate projects information, which should in real case be read from Google forms of professor preferences."""

import random
import math
from data.sma import chairs

number_of_chairs_group_based = 20 # guess: more prof will choose group-based over project-based
bachelor_obligation = 0.25 # the precentage of projects which are available to bachelors

# empirical data
min_number_of_projects = 3
max_number_of_projects = 6

def generate_projects_data(seed_value):
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
        number_of_projects_master_only = random.randint(2, math.floor(number_of_projects * (1-bachelor_obligation)))
        data_group_based[chair] = (number_of_projects, number_of_projects_master_only)

    # project-based projects generation
    for chair in chairs_project_based:
        # generate a list of projects
        list_of_projects = []
        number_of_projects = random.randint(min_number_of_projects, max_number_of_projects) # depends on the capacity of chair but for now we don't have data
        number_of_projects_master_only = random.randint(2, math.floor(number_of_projects * (1-bachelor_obligation)))

        for i in range(1, number_of_projects+1):
            if i <= number_of_projects_master_only:
                list_of_projects.append((f"{chair}(master)-{i}"))
            else:
                list_of_projects.append((f"{chair}(bachelor)-{i}"))

        data_project_based[chair] = list_of_projects

    return data_group_based, data_project_based

def get_project_supervisors_project_based(data_project_based):
    """Only group-based projects are concerned"""
    # initialize
    project_supervisors_group_based = {}

    for chair in data_project_based.keys():
        list_of_projects = data_project_based[chair]
        for proj in list_of_projects:
            project_supervisors_group_based[proj] = chair

    return project_supervisors_group_based

def get_project_supervisors_group_based(data_group_based):
    """Only group-based projects are concerned"""
    # initialize
    project_supervisors_group_based = {}

    for chair in data_group_based.keys():
        number_projects = data_group_based[chair][0]
        number_projects_master = data_group_based[chair][1]
        number_projects_bachelor = number_projects - number_projects_master

        if number_projects_master > 0:
            project_supervisors_group_based[f"{chair}(master)"] = chair

        if number_projects_bachelor > 0:
            project_supervisors_group_based[f"{chair}(bachelor)"] = chair

    return project_supervisors_group_based

def get_project_capacities_project_based(data_project_based):
    project_capacities_project_based = {}

    for chair in data_project_based.keys():
        list_of_projects = data_project_based[chair]
        for proj in list_of_projects:
            project_capacities_project_based[proj] = 1
    
    return project_capacities_project_based

def get_project_capacities_group_based(data_group_based):
    """Only group-based projects are concerned"""
    # initialize
    project_capacities_group_based = {}

    for chair in data_group_based.keys():
        number_projects = data_group_based[chair][0]
        number_projects_master = data_group_based[chair][1]
        number_projects_bachelor = number_projects - number_projects_master

        if number_projects_master > 0:
            project_capacities_group_based[f"{chair}(master)"] = number_projects_master

        if number_projects_bachelor > 0:
            project_capacities_group_based[f"{chair}(bachelor)"] = number_projects_bachelor

    return project_capacities_group_based

def get_number_of_projects_group_based(data_group_based):
    return sum(value[0] for value in data_group_based.values())
