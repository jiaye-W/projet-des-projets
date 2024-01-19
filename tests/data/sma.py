"""
Data of SMA chairs. (All data here is deterministic, without random generation.)
Source: https://www.epfl.ch/schools/sb/research/math/research/

Created on: 18.01.2024

@author: Jiaye Wei <jiaye.wei@epfl.ch>
"""

sma = {"Algebra and Number Theory": ["ARG", "CAG", "EGG", "ERG", "GR-TES", "TAN", "TN"],
       "Analysis": ["AMCV", "CSFT", "DOLA", "PDE", "TAN", "CMGR", "ERG", "SCI-SB-JS", "PROPDE"],
       "Data Science and Learning": ["ANCHP", "BIOSTAT", "CSFT", "DOLA", "Deparis-Group", "LCVMM", "MCSS", "MDS", "OPTIM", "SDS", "SMAT", "STAT"],
       "Discrete Mathematics": ["DISOPT", "ERG", "MDS"],
       "Geometry and Topology": ["ARG", "CAG", "EGG", "CMGR", "GR-TR", "UPHESS"],
       "Mathematics in Computational Sciences": ["ANCHP", "CSQI", "Deparis-Group", "GR-PI", "LCVMM", "MCSS", "MNS", "OPTIM"],
       "Probability and Statistics": ["CSFT", "PROB", "PRST", "RGM", "SMAT", "STOAN", "PROPDE"],
       "Statistics": ["BIOSTAT", "DOLA", "MDS", "OPTIM", "SDS", "SMAT", "STAT"]}
#Remark: We only consider the chairs at SMA so far. 
#TODO: maybe implement a relation matrix between research areas?? (incidence matrix)

research_areas = list(sma.keys())

chairs = list(set(value for values_list in sma.values() for value in values_list))

number_of_chairs = len(chairs) #equals to 34

#print(number_of_chairs) 