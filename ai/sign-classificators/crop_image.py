import cv2
import sys
import os
import numpy as np
from scipy.stats import circmean
from matplotlib import pyplot as plt


BLACK_THRESHOLD_VALUE = 76
WHITE_THRESHOLD_VALUE_MIN = 140
WHITE_THRESHOLD_SATURATION_MAX = 30

COLORFUL_PIXELS_REQUIRED = 1000

HUE_MARGIN = 10
SATURATION_MARGIN_MIN = 50
VALUE_MARGIN_MIN = 50


def readImageAsRGB(filename):
    BGR_image = cv2.imread(filename)
    RGB_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2RGB)
    return RGB_image


def readImageAsHSV(filename):
    BGR_image = cv2.imread(filename)
    HSV_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2HSV)
    return HSV_image


def getParametersFromImage(HSV_image):
    image_size = np.shape(HSV_image)[0]
    FILL_RATIO = 0.5
    return image_size


def findMainColor(HSV_image):
    image_size = getParametersFromImage(HSV_image)
    middle_px = image_size // 2
    # what about image height?
    counter = 0
    distance = 0
    hsv_list = []
    # collect colorful(non-black and non-white) pixels starting from center
    # procedure iterates through wider and wider squares until a certain amount is collected
    while (counter < COLORFUL_PIXELS_REQUIRED):
        for i in range(middle_px - distance, middle_px + distance + 1):
            for j in range(middle_px - distance, middle_px + distance + 1):
                if isEdge(i, j, middle_px, distance) and isColorful(HSV_image[i][j]):
                    counter += 1
                    hsv_list.append(HSV_image[i][j])
        distance += 1
    hue_list = []
    saturation_sum = 0
    value_sum = 0
    for hsv in hsv_list:
        hue_list.append(hsv[0])
        saturation_sum += hsv[1]
        value_sum += hsv[2]
    hue_mean = circmean(hue_list, high=180)
    saturation_mean = saturation_sum / len(hsv_list)
    value_mean = value_sum / len(hsv_list)
    print(hue_mean, saturation_mean, value_mean)
    return hue_mean, saturation_mean, value_mean


def isEdge(x, y, middle, distance):
    return x == middle - distance or y == middle - distance or x == middle + distance or y == middle + distance


def isColorful(HSV_value):
    return not isBlack(HSV_value) and not isWhite(HSV_value)


def isBlack(HSV_value):
    return HSV_value[2] < BLACK_THRESHOLD_VALUE


def isWhite(HSV_value):
    return HSV_value[2] > WHITE_THRESHOLD_VALUE_MIN and HSV_value[1] < WHITE_THRESHOLD_SATURATION_MAX


def makeMask(HSV_image, HSV_mean):

    HUE_MAX_THRESHOLD = 179

    lower_hue = HSV_mean[0] - HUE_MARGIN
    if lower_hue < 0:
        lower_hue += HUE_MAX_THRESHOLD
    if lower_hue > HUE_MAX_THRESHOLD:
        lower_hue -= HUE_MAX_THRESHOLD

    upper_hue = HSV_mean[0] + HUE_MARGIN
    if upper_hue < 0:
        upper_hue += HUE_MAX_THRESHOLD
    if upper_hue > HUE_MAX_THRESHOLD:
        upper_hue -= HUE_MAX_THRESHOLD

    lowerBound = (
        lower_hue, HSV_mean[1] - SATURATION_MARGIN_MIN, HSV_mean[2] - VALUE_MARGIN_MIN)
    upperBound = (upper_hue, 255, 255)

    if lowerBound[0] > upperBound[0]:
        mask1 = cv2.inRange(HSV_image, lowerb=(
            0, lowerBound[1], lowerBound[2]), upperb=upperBound)
        mask2 = cv2.inRange(HSV_image, lowerb=lowerBound, upperb=(
            HUE_MAX_THRESHOLD, upperBound[1], upperBound[2]))
        mask = mask1 | mask2
    else:
        mask = cv2.inRange(HSV_image, lowerb=lowerBound, upperb=upperBound)

    temp = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = temp[-2]
    cv2.drawContours(mask, contours, contourIdx=-1,
                     color=(255, 255, 255), thickness=-1)

    return mask


def applyMask(img, mask):
    return cv2.bitwise_and(img, img, mask=mask)


def getCroppedSign(filename):
    hue_mean, saturation_mean, value_mean = findMainColor(
        readImageAsHSV(filename))
    HSV_mean = (hue_mean, saturation_mean, value_mean)
    mask = makeMask(readImageAsHSV(filename), HSV_mean)
    croppedSign = applyMask(readImageAsRGB(filename), mask)
    return croppedSign


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide image path")
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print("file does not exist")
        exit(2)

    znakPath = sys.argv[1]

    # does OpenCV return image as BGR by default?
    znakImage = cv2.imread(znakPath)
    if znakImage is None:
        print("file is not an image")
        exit(3)

    cv2.imshow("znak", znakImage)

    znakImageHSV = cv2.cvtColor(znakImage, cv2.COLOR_BGR2HSV)
    cv2.imshow("znak HSV", znakImageHSV)

    hue_mean, saturation_mean, value_mean = findMainColor(znakImageHSV)
    HSV_mean = (hue_mean, saturation_mean, value_mean)
    mask = makeMask(znakImageHSV, HSV_mean)

    cv2.imshow("mask", mask)

    cv2.waitKey(0)

# # for testing purposes
# test = getCroppedSign("./znaki/A-7.png")
# plt.imshow(test)
# plt.savefig("test.jpg")
