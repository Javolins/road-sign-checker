import os
import cv2

import sys

from image_analisys_functions import *

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
    #cv2.imshow("znak shaoe", znakShape)

    border = 10
    znakShape2 = cv2.copyMakeBorder(znakShape, border, border, border, border, cv2.BORDER_CONSTANT, value=0)

    contours, hierarchy = cv2.findContours(znakShape2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #contoursSharpened = cv2.approxPolyDP(contours[0], 10, True)
    #contours = [contoursSharpened]

    #jesli wspolczynnik kolowosci jest bliski 1 to znak jest kołem
    #w innym przypadku
    #   jesli da sie go uśrednić do n punktów - n-kąt

    #[vx, vy, x, y] = cv2.fitLine(contours, cv2.DIST_L2, 0, 0.01, 0.01)

    shapeRGB = cv2.cvtColor(znakShape2, cv2.COLOR_GRAY2RGB)

    #draw all points of contour as red with thickness of 3
    znakWithContour = cv2.drawContours(shapeRGB, contours, -1, (255, 0, 0), 1)

    #draw axis
    contoursSharpened = cv2.approxPolyDP(contours[0], 10, True)
    axis = cv2.fitLine(contoursSharpened, cv2.DIST_L2, 0, 0.01, 0.01)
    [vx, vy, x, y] = axis
    rows, cols = znakShape2.shape[:2]
    #draw anchor point of axis
    start = (int(x), int(y))
    magnitude = np.sqrt(rows**2 + cols**2)/4
    vector = (magnitude*vx, magnitude*vy)
    end = (int(start[0] + vector[0]), int(start[1] + vector[1]))
    znakWithContour = cv2.line(znakWithContour, start, end, (0, 0, 255))
    znakWithContour = cv2.circle(znakWithContour, start, 3, (0, 0, 255))
    #image = cv2.circle(znakWithContour, (x, y), radius=0, color=(0, 0, 255), thickness=-1)

    cv2.imshow("znak contour", znakWithContour)

    #circularity
    mainContour = contours[0]

    circularity = getCircularity(mainContour)
    print(circularity)

    cv2.waitKey(0)