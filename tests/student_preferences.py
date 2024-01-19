from project_supervisors import project_supervisors
from tests.data.students import students

# from project_supervisors, get the list of projects
projects = list(project_supervisors.keys())

def generate_student_prefs(index):
    # get information of student of index
    (degree, selected_chairs) = students[index]

    # 


generate_student_prefs(1)