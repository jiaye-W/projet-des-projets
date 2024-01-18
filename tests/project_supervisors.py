"""Generate the project_supervisors dict for passing as argument into the matching algorithm"""

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

def get_project_supervisors(data_group_based, data_project_based):
    """_summary_

    Args:
        data_group_based (_type_): _description_
        data_project_based (_type_): _description_

    Returns:
        _type_: _description_
    """
    group_based_project_supervisors = get_group_based_project_supervisors(data_group_based)
    project_based_project_supervisors = get_project_based_project_supervisors(data_project_based)

    project_supervisors = {**group_based_project_supervisors, **project_based_project_supervisors}
    return project_supervisors


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

def get_project_based_project_supervisors(data_project_based):
    """_summary_

    Returns:
        _type_: _description_
    """
    project_based_project_supervisors = {}

    return project_based_project_supervisors

