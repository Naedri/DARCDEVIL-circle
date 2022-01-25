from math import sqrt


class Position(object):
    """A class used to represent Position"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distance(self, other):
        return ((self.getX() - other.getX())**2 + (self.getY() - other.getY())**2)**0.5

    def to_string(self):
        return "(" + str(self.getX()) + ", " + str(self.getY()) + ")"
