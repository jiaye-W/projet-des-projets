"""
Generation of students test data

Created on: 13.01.2024

@author: Jiaye Wei <jiaye.wei@epfl.ch>
"""

import random
from sma import *

# The number of students to be generated
number_of_students = 50

def generate_students(count):
    """Generate two things: bachelor/master and research interest

    Args:
        count (int): the number of students to be generated

    Returns:
        dict: students
    """
    students = {}

    # set-up of RNG
    seed_value = 42
    random.seed(seed_value)

    for i in range(1, count+1):
        # genearate the degree, either bachelor (30% chance) or master (70% chance)
        degree = generate_degree_of_student(random, probability_of_master=0.7)

        # generate the research interest 
        research_interest = random.choice(research_areas)

        # choose 2 chairs from each research areas
        selected_chairs = random.sample(sma[research_interest], 2)

        students[i] = (degree, selected_chairs)

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


if __name__ == "__main__":
    generate_students(number_of_students)