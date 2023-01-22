# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import numpy as np


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reposDir = os.path.abspath('./../../..')
    znakiDir = os.path.abspath(reposDir + '/znaki-sandbox/znaki')
    znakPath = os.path.abspath(znakiDir + "/B-2.png")


    znakImage = cv2.imread(znakPath)
    cv2.imshow("znak", znakImage)
    cv2.waitKey(0)

    imageGray = cv2.cvtColor(znakImage, cv2.COLOR_RGB2GRAY)
    # cv2.imshow("znak szary", imageGray)
    # cv2.waitKey(0)

    t, znakBinary = cv2.threshold(imageGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow("znak bin", znakBinary)
    # cv2.waitKey(0)

    znakBinary2 = cv2.bitwise_not(znakBinary)
    cv2.imshow("znak bin inverse", znakBinary2)
    cv2.waitKey(0)

    #add border to close without expansion
    border = 50
    znakBinary3 = cv2.copyMakeBorder(znakBinary2, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=0)
    # cv2.imshow("znak border", znakBinary3)
    # cv2.waitKey(0)

    kernel = np.ones((40, 40), np.uint8)
    znakClosed = cv2.morphologyEx(znakBinary3, cv2.MORPH_CLOSE, kernel)
    # znakClosed = cv2.erode(cv2.dilate(znakBinary2, kernel), kernel)
    # cv2.imshow("znak closed", znakClosed)
    # cv2.waitKey(0)

    znakClosed2 = znakClosed[border:-border, border:-border]
    cv2.imshow("znak closed", znakClosed2)
    cv2.waitKey(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
