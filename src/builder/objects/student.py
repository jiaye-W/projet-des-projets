class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def display_info(self):
        print(f"Name: {self.name}\nStudent ID: {self.student_id}")


class BachelorStudent(Student):
    def __init__(self, name, student_id, major):
        super().__init__(name, student_id)
        self.major = major

    def display_info(self):
        super().display_info()
        print(f"Major: {self.major}\nStudent Type: Bachelor")


class MasterStudent(Student):
    def __init__(self, name, student_id, thesis_topic):
        super().__init__(name, student_id)
        self.thesis_topic = thesis_topic

    def display_info(self):
        super().display_info()
        print(f"Thesis Topic: {self.thesis_topic}\nStudent Type: Master")

