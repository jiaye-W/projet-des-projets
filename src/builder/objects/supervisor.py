class Supervisor:
    def __init__(self, name, ad_type):
        self.name = name
        self.ad_type = ad_type # string: group-based or project-based
        self.projects = None
        self.research = None

        self.is_valid()

    @classmethod
    def is_valid(self):
        return True