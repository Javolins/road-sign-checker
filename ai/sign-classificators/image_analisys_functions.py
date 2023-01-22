import cv2
import numpy as np
import math

from enum import Enum

class ZnakShape(Enum):
    CIRCLE = 1,
    TRIANGLE = 2,
    RECTANGLE = 3,
    OCTAGON = 4,
    UNKNOWN = 10


def binarizeToExtractShapeMask(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    t, binarizedOtsu = cv2.threshold(imageGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    maskOtsu = cv2.bitwise_not(binarizedOtsu)

    # add border to close without expansion
    border = 50
    maskOtsuExpanded = cv2.copyMakeBorder(maskOtsu, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=0)
    # cv2.imshow("znak border", znakBinary3)
    # cv2.waitKey(0)

    kernel = np.ones((5, 5), np.uint8)
    maskClosed = cv2.morphologyEx(maskOtsuExpanded, cv2.MORPH_CLOSE, kernel, iterations=20)

    shapeMask = maskClosed[border:-border, border:-border]
    return shapeMask

def getCircularity(contour):
    area = cv2.contourArea(contour)
    center, radius = cv2.minEnclosingCircle(contour)
    perimeter = 2 * np.pi * radius
    circularity = (4 * np.pi * area) / (perimeter ** 2)
    return circularity

def getEllipsisity(contour):
    area = cv2.contourArea(contour)
    (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
    ellipseArea = math.pi * MA * ma
    ellipsisity = area/ellipseArea
    return ellipsisity

def getMaskContour(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mainContour = contours[0]
    return mainContour
def getZnakContour(znakImage):
    #assert znakImage is valid object returned by cv2.imread
    znakShape = binarizeToExtractShapeMask(znakImage)
    mainContour = getMaskContour(znakShape)
    return mainContour

def getZnakCircularity(znakImage):
    #assert znakImage is valid object returned by cv2.imread
    mainContour = getZnakContour(znakImage)
    circularity = getCircularity(mainContour)

    return circularity

def getNumberOfVertices(mainContour, imageSize):
    imageDiagonalLength = np.sqrt(imageSize.width ** 2 + imageSize.height ** 2)
    EPSILON_PERCENTAGE = 0.07
    polygonApproximationEpsilon = EPSILON_PERCENTAGE * imageDiagonalLength
    contoursSharpened = cv2.approxPolyDP(mainContour, polygonApproximationEpsilon, True)
    numberOfVertices = len(contoursSharpened)
    return numberOfVertices

class ImageSize:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def createFromOpenCVImage(openCVImage):
        # shape stores number of rows(height) first
        size = ImageSize(openCVImage.shape[1], openCVImage.shape[0])
        return size

def getShape(contour, imageSize):
    #contour - first element exctracted from cv2.findContours
    ellipsisity = getEllipsisity(contour)

    ELLIPSE_THRESHOLD = 0.95
    isNotCircle = ellipsisity < ELLIPSE_THRESHOLD

    if isNotCircle:
        numberOfVertices = getNumberOfVertices(contour, imageSize)
        if numberOfVertices == 3:
            return ZnakShape.TRIANGLE
        elif numberOfVertices == 4:
            return ZnakShape.RECTANGLE
        elif numberOfVertices == 8:
            return ZnakShape.OCTAGON
        else:
            return ZnakShape.UNKNOWN
    else:
        return ZnakShape.CIRCLE

def getMaskShape(mask):
    #@param mask binary image where white represents shape and black background
    maskContour = getMaskContour(mask)
    imageSize = ImageSize.createFromOpenCVImage(mask)
    shape = getShape(maskContour, imageSize)
    return shape
