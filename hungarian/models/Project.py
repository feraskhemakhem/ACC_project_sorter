
class Project(object):

    def __init__(self, name, id, num_members):
        self.name = name
        self.id = id
        self.num_members = num_members

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)