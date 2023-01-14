import os
import cv2

import sys

from image_analisys_functions import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide learning set directory")
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print("path does not exist")
        exit(2)

    if not os.path.isdir(sys.argv[1]):
        print("path is not a directory")
        exit(3)

    learningSetDirectory = sys.argv[1]
    learnignSetFilenames = os.listdir(learningSetDirectory)

    znakiDataset = []
    for fileName in learnignSetFilenames:
        filePath = learningSetDirectory + "/" + fileName

        znakImage = cv2.imread(filePath)
        if znakImage is None:
            print(filePath + " is not a valid image file")
            exit(4)

        mainContour = getZnakContour(znakImage)
        circularity = getCircularity(mainContour)

        CIRCLE_THRESHOLD = 0.95
        isNotCircle = circularity < CIRCLE_THRESHOLD
        
        if isNotCircle:
            contoursSharpened = cv2.approxPolyDP(mainContour, 10, True)
            numberOfVertices = len(contoursSharpened)
            if numberOfVertices == 3:
                shape = "triangle"
            elif numberOfVertices == 4:
                shape = "rectangle"
            elif numberOfVertices == 8:
                shape = "octagon"
            else:
                shape = "polygon of " + numberOfVertices + "vertices"
        else:
            shape = "circle"

        znakiElement = {
            "fileName": fileName,
            "circularity": circularity,
            "shape": shape
        }
        znakiDataset.append(znakiElement)

    for znakiElement in znakiDataset:
        print(znakiElement)

