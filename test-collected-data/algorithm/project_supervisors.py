"""Generate the project_supervisors dict for passing as argument into the matching algorithm"""

"""Group-based projects

    key: name of the chair
    value: a pair (number of projects, number of projects ONLY for master students)

    There will be (not implemented yet), a validation check of the pairs, so that it satisfies
    - mandatory capacity
    - bachelor obligation
"""

# naming of project of group-based projects: "ARG-1", "ARG-2", "ARG-3", "CAG-1", etc
# also have to contain the degree requirement: "ARG-1", 

def build_project_supervisors(data_group_based, data_project_based):
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

def get_group_based_project_capacities(data_group_based):
    return 0

def get_group_based_project_supervisors(data_group_based):
    """Get the data of project-supervisors correspondence, for group-based projects

    Args:
        data_group_based(dict): raw data gathered from Google forms for group-based projects

    Returns:
        project_supervisors: correspondence between projects and supervisors
    """
    group_based_project_supervisors = {}

    for chair in data_group_based:
        # read the pair of numbers: (# of projects, # of projects for only masters)
        (number_of_projects, number_of_projects_only_masters) = data_group_based[chair]

        for i in range(1, number_of_projects+1):
            if (i <= number_of_projects_only_masters):
                group_based_project_supervisors[f"{chair}, proj-{i} (only master)"] = chair
            else:
                group_based_project_supervisors[f"{chair}, proj-{i}"] = chair

    return group_based_project_supervisors

# Build up projects from dict 

"""Project-based projects

    key: name of the chair
    value: a list of projects

    There will be (not implemented yet), a validation check of the pairs, so that it satisfies
    - mandatory capacity
    - bachelor obligation
"""
data_project_based = {"EGG": [(1, "proj1-EGG", "bachelor"), (2, "proj2-EGG", "master")], 
                      "ERG": [(1, "proj1-ERG", "master"), (2, "proj2-ERG", "master"), (3, "proj3-ERG", "bachelor"), (4, "proj4-ERG", "master")]}
number_of_projects_project_based = sum(len(value) for value in data_project_based.values())

def get_project_based_project_supervisors(data_project_based):
    """Get the data of project-supervisors correspondence, for project-based projects

    Args:
        data_project_based(dict): raw data gathered from Google forms

    Returns:
        project_supervisors: correspondence between projects and supervisors
    """
    project_based_project_supervisors = {}



    return project_based_project_supervisors