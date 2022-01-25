import time
from math import sqrt
from collections import OrderedDict


class Solver(object):
    """executes the alogirithms in order to find the intersections"""

    def __init__(self, algo, circles):
        self.algo = algo
        self.circles = circles

    def find_intersect(self):
        # if (self.getAlgo() == 1):
        return self.algo1()

    def getAlgo(self):
        return self.algo

    def algo1(self):
        # do shizlle in O(N^2)
        result = list()
        intersections = set()
        infinity = bool(0)
        now = time.time()
        for circle in self.circles:
            # copy of the original array thus has size n - 1
            hulp = list(self.circles)
            hulp.remove(circle)
            for otherCircle in hulp:
                dis = circle.center_distance(otherCircle)
                if (otherCircle.getCenter().getX() >= circle.getCenter().getX()):
                    if not (dis > (circle.getRadius() + otherCircle.getRadius())) and not (dis < abs(circle.getRadius() - otherCircle.getRadius())) and not (dis == 0 and circle.getRadius() == otherCircle.getRadius()):
                        intersect = circle.intersect(otherCircle)
                        for inter in intersect:
                            if not (inter in intersections):
                                intersections.add(inter)
                else:
                    # no solutions circles are too far apart
                    # no solutions circles are enclosing each other
                    # infinitely many solutions coinciding circles
                    if (dis == 0 and circle.getRadius() == otherCircle.getRadius()):
                        infinity = bool(1)
        now = time.time() - now
        if (infinity):
            result.append('infinity')
            result.append(now)
            return result
        else:
            result.append(intersections)
            result.append(now)
            return result

    def can_intersect(self, circle, otherCircle):
        dis = circle.center_distance(otherCircle)
        return not (dis > (circle.getRadius() + otherCircle.getRadius())) and not (dis < abs(circle.getRadius() - otherCircle.getRadius())) and not (dis == 0 and circle.getRadius() == otherCircle.getRadius())
