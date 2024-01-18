class Student:
    def __init__(self, name, degree, research_interest):
        self.name = name # or any equivalent identity of student (sciper, email, etc)
        self.degree = degree
        self.research_interests = research_interest # a list 

class BachelorStudent(Student):
    def __init__(self, name, research_interest):
        super().__init__(name, 'bachelor', research_interest)


class MasterStudent(Student):
    def __init__(self, name, research_interest):
        super().__init__(name, 'master', research_interest)

