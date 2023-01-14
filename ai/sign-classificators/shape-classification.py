import os
import cv2
import numpy as np

import sys

def binarizeToExtractShapeMask(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    t, binarizedOtsu = cv2.threshold(imageGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    maskOtsu = cv2.bitwise_not(binarizedOtsu)

    # add border to close without expansion
    border = 50
    maskOtsuExpanded = cv2.copyMakeBorder(maskOtsu, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=0)
    # cv2.imshow("znak border", znakBinary3)
    # cv2.waitKey(0)

    kernel = np.ones((40, 40), np.uint8)
    maskClosed = cv2.morphologyEx(maskOtsuExpanded, cv2.MORPH_CLOSE, kernel)

    shapeMask = maskClosed[border:-border, border:-border]
    return shapeMask

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide image path")
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print("file does not exist")
        exit(2)

    znakPath = sys.argv[1]

    znakImage = cv2.imread(znakPath)
    if znakImage is None:
        print("file is not an image")
        exit(3)

    cv2.imshow("znak", znakImage)

    znakShape = binarizeToExtractShapeMask(znakImage)
    cv2.imshow("znak shaoe", znakShape)

    border = 10
    znakShape2 = cv2.copyMakeBorder(znakShape, border, border, border, border, cv2.BORDER_CONSTANT, value=0)

    contours, hierarchy = cv2.findContours(znakShape2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    print(hierarchy)

    shapeRGB = cv2.cvtColor(znakShape2, cv2.COLOR_GRAY2RGB)

    #draw all points of contour as red with thickness of 3
    znakWithContour = cv2.drawContours(shapeRGB, contours, -1, (0, 0, 255), 3)
    cv2.imshow("znak contour", znakWithContour)
    cv2.waitKey(0)