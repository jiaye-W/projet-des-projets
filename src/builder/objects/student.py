class Student:
    def __init__(self, name, sciper, degree):
        self.name = name
        self.sciper = sciper
        self.degree = degree

    def display_info(self):
        print(f"Name: {self.name}\nStudent ID: {self.student_id}")


class BachelorStudent(Student):
    def __init__(self, name, sciper):
        super().__init__(name, sciper, 'bachelor')


class MasterStudent(Student):
    def __init__(self, name, sciper):
        super().__init__(name, sciper, 'master')

