class Person:
    def __init__(self, id, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
    def __str__(self):
        return "<{} {} {}>".format(self.id, self.first_name, self.last_name)


class Queue(object):
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    def __str__(self):
        return "< Queue " + str(self.id) + ": " + self.name + " >"