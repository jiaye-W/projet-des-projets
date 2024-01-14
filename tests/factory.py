"""
The matching factory which contains tests data 

Created on: 13.01.2024

@author: Jiaye Wei <jiaye.wei@epfl.ch>
"""

import random

from src.builder.objects.project import Project
from src.builder.objects.student import Student

def test():
    students = [("Alice", "bachelor"),
                ("")]

def generate_students():
    number_of_students = 50
    number_of_projects = 100
    random.choice()

def generate_supervisors():
    # All chairs at SMA
    chairs = {"Algebra and Number Theory": ["ARG", "CAG", "EGG", "ERG", "GR-TES", "TAN", "TN"],
              "Analysis": ["AMCV", "CSFT", "DOLA", "PDE", "TAN", "CMGR", "ERG", "SCI-SB-JS", "PROPDE"],
              "Data Science and Learning": ["ANCHP", "BIOSTAT", "CSFT", "DOLA", "Deparis-Group", "LCVMM", "MCSS", "MDS", "OPTIM", "SDS", "SMAT", "STAT"],
              "Discrete Mathematics": ["DISOPT", "ERG", "MDS"],
              "Geometry and Topology": ["ARG", "CAG", "EGG", "CMGR", "GR-TR", "UPHESS"],
              "Mathematics in Computational Sciences": ["ANCHP", "CSQI", "Deparis-Group", "GR-PI", "LCVMM", "MCSS", "MNS", "OPTIM"],
              "Probability and Statistics": ["CSFT", "PROB", "PRST", "RGM", "SMAT", "STOAN", "PROPDE"],
              "Statistics": ["BIOSTAT", "DOLA", "MDS", "OPTIM", "SDS", "SMAT", "STAT"]}