"""
The class of projects

Created on: 13.01.2024

@author: Jiaye Wei <jiaye.wei@epfl.ch>
"""

class Project:
    def __init__(self, supervisor, title, description, stud_type):
        self.supervisor = supervisor
        self.title = title
        self.description = description
        self.stud_type = stud_type # bachelor/master/both


class PseudoProject(Project):
    def __init__(self, supervisor, stud_type, title=None, description=None):
        super().__init__(supervisor, stud_type, title, description)