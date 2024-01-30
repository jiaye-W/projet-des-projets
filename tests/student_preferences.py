import random

def build_student_preferences(students, project_supervisors, seed_value):
    random.seed(seed_value)
    student_preferences = {}

    for i in students:
        (degree, research_interest, selected_chairs) = students[i]

        # from the selected_chairs, randomly choose projects which are acceptable
        accpetable_projects = [proj for proj, sup in project_supervisors.items() 
                               if sup in selected_chairs]
        
        accpetable_projects = [proj for proj in accpetable_projects 
                               if degree in proj]
        #print(accpetable_projects)

        number_of_projects_to_choose = random.randint(2, len(accpetable_projects))
        selected_projects = random.sample(accpetable_projects, number_of_projects_to_choose)
        random.shuffle(selected_projects)

        student_preferences[i] = selected_projects

    return student_preferences