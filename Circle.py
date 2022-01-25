import matplotlib.pyplot as plt
from Position import Position
from numpy import poly1d


class Circle(object):
    """A class used to represent circles"""
    color = 1

    def __init__(self, center, radius):
        self.center = center
        self.radius = float(radius)
        self.TOP = Position(center.getX(), center.getY() + radius)
        self.BOTTOM = Position(center.getX(), center.getY() - radius)
        self.LEFT = Position(center.getX() - radius, center.getY())
        self.RIGHT = Position(center.getX() + radius, center.getY())
        if (Circle.color % 4 == 0):
            self.plot = plt.Circle((self.getCenter().getX(
            ), self.getCenter().getY()), radius, color='b', fill=False)
            Circle.color = Circle.color + 1
        elif (Circle.color % 4 == 1):
            self.plot = plt.Circle((self.getCenter().getX(
            ), self.getCenter().getY()), radius, color='g', fill=False)
            Circle.color = Circle.color + 1
        elif (Circle.color % 4 == 3):
            self.plot = plt.Circle((self.getCenter().getX(
            ), self.getCenter().getY()), radius, color='r', fill=False)
            Circle.color = Circle.color + 1
        else:
            self.plot = plt.Circle((self.getCenter().getX(
            ), self.getCenter().getY()), radius, color='black', fill=False)
            Circle.color = Circle.color + 1

    def display(self):
        print("Center: ", self.center)
        print("Radius: ", self.radius)

    def getCenter(self):
        return self.center

    def getRadius(self):
        return self.radius

    def getPlot(self):
        return self.plot

    def center_distance(self, other):
        return self.getCenter().distance(other.getCenter())

    def intersect(self, otherCircle):
        result = set()
        a = 2*self.getCenter().getX() - 2*otherCircle.getCenter().getX()
        b = 2*self.getCenter().getY() - 2*otherCircle.getCenter().getY()
        d = (-1)*(self.getRadius()**2) + otherCircle.getRadius()**2 + self.getCenter().getX()**2 + \
            self.getCenter().getY()**2 - otherCircle.getCenter().getX()**2 - \
            otherCircle.getCenter().getY()**2
        if not (a == 0):
            A = (b/a)**2 + 1
            B = (2*((d/a)-self.getCenter().getX()) * ((-1)*b/a)) - \
                2 * self.getCenter().getY()
            C = (d/a - self.getCenter().getX())**2 + \
                self.getCenter().getY()**2 - self.getRadius()**2
            D = round((B**2) - (4*A*C), 15)
            ypoints = list()
            ypoints.append(round((-B + D**0.5)/(2*A), 15))
            ypoints.append(round((-B - D**0.5)/(2*A), 15))
            xpoints = list()
            for y in ypoints:
                xpoints.append(d/a - b/a*y)
            result.add(Position(xpoints.pop(), ypoints.pop()))
            result.add(Position(xpoints.pop(), ypoints.pop()))
            return result
        else:
            y = d/b
            C = d**2/b**2 - ((2*self.getCenter().getY())*(d/b)) - self.getRadius()**2 + \
                self.getCenter().getX()**2 + self.getCenter().getY()**2
            A = 1
            B = -2*self.getCenter().getX()
            D = round((B**2) - (4*A*C), 15)
            xpoints = list()
            xpoints.append(round((-B + D**0.5)/(2*A), 15))
            xpoints.append(round((-B - D**0.5)/(2*A), 15))
            result.add(Position(xpoints.pop(), y))
            result.add(Position(xpoints.pop(), y))
            return result

    def to_string(self):
        return "|" + self.getCenter().to_string() + "|" + str(self.getRadius()) + "|"
