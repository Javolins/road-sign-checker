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


def expandImageToThreeLayers(oneLayerImage):
    expanded = oneLayerImage[:, :, np.newaxis].repeat(3, 2)
    return expanded

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

def getEllipsisityDeviation(contour):
    area = cv2.contourArea(contour)
    (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
    ellipseArea = math.pi * MA * ma
    ellipsisity = 4*area/ellipseArea
    deviation = abs(1.0 - ellipsisity)
    return deviation

def getRectangularity(contour):
    area = cv2.contourArea(contour)
    boundingRectSize = ImageSize.createFromMask(contour)
    rectArea = boundingRectSize.width * boundingRectSize.height
    rectangularity = area/rectArea
    return rectangularity

def getMaskContour(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mainContour = max(contours, key = cv2.contourArea)
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

def getPolygonEpsilonBasedOnImageSize(imageSize, EPSILON_PERCENTAGE):
    imageDiagonalLength = np.sqrt(imageSize.width ** 2 + imageSize.height ** 2)
    polygonApproximationEpsilon = EPSILON_PERCENTAGE * imageDiagonalLength
    return polygonApproximationEpsilon
def getSimplifiedShape(mainContour, polygonApproximationEpsilon):
    simplifiedShape = cv2.approxPolyDP(mainContour, polygonApproximationEpsilon, True)
    return simplifiedShape

def getNumberOfVertices(mainContour, imageSize, EPSILON_PERCENTAGE = 0.0095):
    polygonApproximationEpsilon = getPolygonEpsilonBasedOnImageSize(imageSize, EPSILON_PERCENTAGE)
    simplifiedShape = getSimplifiedShape(mainContour, polygonApproximationEpsilon)
    numberOfVertices = len(simplifiedShape)
    return numberOfVertices

class ImageSize:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def createFromOpenCVImage(openCVImage):
        # shape stores number of rows(height) first
        size = ImageSize(openCVImage.shape[1], openCVImage.shape[0])
        return size

    def createFromMask(maskContour):
        rect = cv2.minAreaRect(maskContour)
        boundingRectSize = ImageSize(rect[1][0], rect[1][1])
        return boundingRectSize

def isContourElliptic(contour):
    ELLIPSE_DEVIATION_THRESHOLD = 0.0125
    ellipsisityDeviation = getEllipsisityDeviation(contour)
    isElliptic = ellipsisityDeviation <= ELLIPSE_DEVIATION_THRESHOLD
    return isElliptic

def getShape(contour, maskSize):
    #contour - first element exctracted from cv2.findContours
    TRIANGLE_RECTANGULARITY_THRESHOLD = 0.6
    rectangularity = getRectangularity(contour)
    if rectangularity > TRIANGLE_RECTANGULARITY_THRESHOLD:
        numberOfVertices = getNumberOfVertices(contour, maskSize)
        if isContourElliptic(contour):
            # octagon under angle may undergo as circle
            if numberOfVertices != 8:
                return ZnakShape.CIRCLE
            else:
                return ZnakShape.OCTAGON
        elif rectangularity > 0.9:
            return ZnakShape.RECTANGLE
        else:
            if numberOfVertices == 4:
                return ZnakShape.RECTANGLE
            elif numberOfVertices == 8:
                return ZnakShape.OCTAGON
            else:
                return ZnakShape.UNKNOWN
    else:
        return ZnakShape.TRIANGLE



def getMaskShape(mask):
    #@param mask binary image where white represents shape and black background
    maskContour = getMaskContour(mask)
    contourArea = cv2.contourArea(maskContour)
    if contourArea != 0:
        maskSize = ImageSize.createFromMask(maskContour)
        shape = getShape(maskContour, maskSize)
        return shape
    else:
        return ZnakShape.UNKNOWN
