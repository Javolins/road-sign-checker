import cv2
import numpy as np

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

def getZnakContour(znakImage):
    #assert znakImage is valid object returned by cv2.imread
    znakShape = binarizeToExtractShapeMask(znakImage)
    contours, hierarchy = cv2.findContours(znakShape, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mainContour = contours[0]
    return mainContour

def getZnakCircularity(znakImage):
    #assert znakImage is valid object returned by cv2.imread
    mainContour = getZnakContour(znakImage)
    circularity = getCircularity(mainContour)

    return circularity

def getNumberOfVertices(mainContour, imageSize):
    imageDiagonalLength = np.sqrt(imageSize[0] ** 2 + imageSize[1] ** 2)
    EPSILON_PERCENTAGE = 0.07
    polygonApproximationEpsilon = EPSILON_PERCENTAGE * imageDiagonalLength
    contoursSharpened = cv2.approxPolyDP(mainContour, polygonApproximationEpsilon, True)
    numberOfVertices = len(contoursSharpened)
    return numberOfVertices
def getShape(contour, imageSize):
    #znakMask - binarized image of znak where white pixels represent it
    circularity = getCircularity(contour)

    CIRCLE_THRESHOLD = 0.95
    isNotCircle = circularity < CIRCLE_THRESHOLD

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
