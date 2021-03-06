__author__ = 'harry'
import math


class Point():
    """A class to define a point in 2D space"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector():
    """A class to define a vector using 2 points"""
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

    def update(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def useAngle(self, x1, y1, mag, angle):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + math.cos(math.radians(angle))
        self.y2 = y1 + math.sin(math.radians(angle))
        self.angle = angle

    def add(self, vector):
        newx = self.getDx() + vector.getDx()
        newy = self.getDy() + vector.getDy()
        return Vector(self.x2, self.y2, self.x1 + newx, self.y1 + newy)


    def getMagnitude(self):
        return math.sqrt((self.y2 - self.y1) ** 2 + (self.x2 - self.x1) ** 2)

    def getDx(self):
        return (self.x2 - self.x1)

    def getDy(self):
        return (self.y2 - self.y1)

    def dotProduct(self, vector):
        return (self.getDx() * vector.getDx()) + (self.getDy() * vector.getDy())


class Rectangle():
    def __init__(self, TopLeft, BottomLeft, BottomRight, TopRight):
        TopSide = Vector(TopLeft[0], TopLeft[1], TopRight[0], TopRight[1])
        LeftSide = Vector(TopLeft[0], TopLeft[1], BottomLeft[0], BottomLeft[1])
        BottomSide = Vector(BottomLeft[0], BottomLeft[1], BottomRight[0], BottomRight[1])
        RightSide = Vector(TopRight[0], TopRight[1], BottomRight[0], BottomRight[1])
        self.myVectors = [TopSide, LeftSide, RightSide, BottomSide]

    def collides(self, vector):
        for v in self.myVectors:
            if intersect(v, vector):
                return True
        return False


def getAngleOfIntersection(vecA, vecB):
    """a dot b / mag(a) mag(b)"""
    try:
        #Set numerator and denom
        num = vecA.dotProduct(vecB)
        denom = vecA.getMagnitude() * vecB.getMagnitude()
        #Angle is cos-1(A,B / |A||B|)
        ang = math.degrees(math.acos(num / denom))
        return ang
    except Exception as ex:
        print "Exception in getangleofintersection: " + str(ex)


def getPoints(x1, y1, x2, y2):
    try:
        angle = math.atan2(y2 - y1, x2 - x1)
        values = []
        for x in range(1, int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)) + 5):
            values.append([int(x1 + x * math.cos(angle)), int(y1 + x * math.sin(angle))])
        return values
    except Exception as ex:
        print "Exception in getpoints: " + str(ex)


def intersect(vectorA, vectorB):
    try:
        a = getPoints(vectorA.x1, vectorA.y1, vectorA.x2, vectorA.y2)
        b = getPoints(vectorB.x1, vectorB.y1, vectorB.x2, vectorB.y2)
        for c in a:
            if c in b:
                return True
        return False
    except Exception as ex:
        print "Exception in intersect: " + str(ex)

