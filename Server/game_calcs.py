__author__ = 'harry'
import math

class Point():
    """Used to represent a single point on the screen"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vector():
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.angle = math.degrees(math.atan2(y2-y1, x2-x1))

    def update(self,x1,y1,x2,y2):
	"""Reset the vector to a new point"""
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def useAngle(self, x1, y1, mag, angle):
	"""Init a vector with a magnitude and angle"""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + math.cos(math.radians(angle))
        self.y2 = y1 + math.sin(math.radians(angle))
        self.angle = angle

    def add(self, vector):
	"""Returns the resultant vector of the addition of this and another vector"""
        newx = self.getDx() + vector.getDx()
        newy = self.getDy() + vector.getDy()
        return Vector(self.x2, self.y2, self.x1 + newx, self.y1 + newy)


    def getMagnitude(self):
	"""Returns the length of this vector"""

        return math.sqrt((self.y2-self.y1)**2 + (self.x2-self.x1)**2)

    def getDx(self):
	"""Returns the x-length of the vector"""
        return math.fabs(self.x2 - self.x1)

    def getDy(self):
	"""Returns the y-length of the vector"""
        return math.fabs(self.y2 - self.y1)

    def dotProduct(self, vector):
	"""Returns the scalar product of this vector and another"""

        return self.getDx()*vector.getDx() + self.getDy()*vector.getDy()

class Rectangle():
    """A simple rectangle of vectors."""
    def __init__(self, TopLeft, BottomLeft, BottomRight, TopRight):
        TopSide = Vector(TopLeft[0], TopLeft[1], TopRight[0], TopRight[1])
        LeftSide = Vector(TopLeft[0], TopLeft[1], BottomLeft[0], BottomLeft[1])
        BottomSide = Vector(BottomLeft[0], BottomLeft[1], BottomRight[0], BottomRight[1])
        RightSide = Vector(TopRight[0], TopRight[1], BottomRight[0], BottomRight[1])
        self.myVectors = [TopSide, LeftSide, RightSide, BottomSide]

    def collides(self, vector):
        """Checks whether a vector intersects with the rectangle"""
	for v in self.myVectors:
            if intersect(v, vector):
                return True
        return False

def getAngleOfIntersection(vecA, vecB):
    """a dot b / mag(a) mag(b)"""
    num = vecA.dotProduct(vecB)
    denom = vecA.getMagnitude() * vecB.getMagnitude()
    ang =  math.degrees(math.acos(num/denom))
    print ang
    if ang > 90:
        diff = ang - 90
        ang = 90 - diff
    return ang

def getDeltaT(time1, time2):
    """Returns the difference between 2 time.time instances"""

    return time2 - time1

def getPoints(x1, y1, x2, y2):
    """Returns a list of pixels on the line joining (x1,y1) to (x2, y2)"""

    angle = math.atan2(y2-y1, x2-x1)
    values = []
    for x in range(1,int(math.sqrt((y2-y1)**2 + (x2-x1)**2))+2):
        values.append([math.floor(x1 + x*math.cos(angle)), math.floor(y1 + x*math.sin(angle))])
    return values

def intersect(vectorA, vectorB):
    """Checks whether two vectors intersect"""

    a = getPoints(vectorA.x1, vectorA.y1, vectorA.x2, vectorA.y2)
    b = getPoints(vectorB.x1, vectorB.y1, vectorB.x2, vectorB.y2)
    for c in a:
        if c in b:
            return True
    return False
