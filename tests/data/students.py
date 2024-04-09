"""
Data of students, which is randomly generated.

Created on: 13.01.2024

@author: Jiaye Wei <jiaye.wei@epfl.ch>
"""

import random
from data.sma import *

def get_number_of_master_students(students):
    number_of_students = len(students)
    number_of_master_students = sum(1 for i in range(1, number_of_students+1) if students[i][0] == "master")
    return number_of_master_students

def generate_students(seed_value, count):
    """Generate two things: bachelor/master and research interest

    Args:
        count (int): the number of students to be generated

    Returns:
        dict: students
        key: index
        value: (degree, selected_chairs)
    """
    random.seed(seed_value)
    students = {}
    for i in range(1, count+1):
        # genearate the degree, either bachelor (30% chance) or master (70% chance)
        degree = generate_degree_of_student(random, probability_of_master=0.7)

        # generate the research interest 
        biased_weights = [0.1, 0.05, 0.4, 0.05, 0.05, 0.05, 0.25, 0.05] # biased list of weights
        unbiased_weights = [0.125] * 8

        use_biased_weights = False # can choose to use bias or not

        weights = biased_weights if use_biased_weights else unbiased_weights
        research_interest = random.choices(research_areas, weights)[0]

        # choose 2 chairs from each research areas
        selected_chairs = random.sample(sma[research_interest], 2)

        students[i] = (degree, research_interest, selected_chairs)

    #print(students)
    return students

def generate_degree_of_student(random, probability_of_master):
    """A biased coin which generates the degree of student, either bachelor or master

    Args:
        random (random): RNG
        probability_of_master (double): the probability of a student instance being master

    Returns:
        str: master or bachelor
    """
    # generate a random float in the range [0.0, 1.0)
    random_value = random.random()

    # check if the random value is less than the probability_of_heads
    if random_value < probability_of_master:
        return "master"
    else:
        return "bachelor"


def get_research_interest_counts(students):
    research_interest_counts = {}

    for index, information in students.items():
        research_area = information[1]
        if research_area in research_interest_counts:
            research_interest_counts[research_area] += 1
        else:
            research_interest_counts[research_area] = 1

    sorted_dict = {key: research_interest_counts[key] for key in research_areas if key in research_interest_counts}

    return sorted_dict