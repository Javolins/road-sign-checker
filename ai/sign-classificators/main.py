import cv2
import numpy as np

from scipy.stats import circmean

import sys
import os

BLACK_THRESHOLD_VALUE = 76
WHITE_THRESHOLD_VALUE_MIN = 140
WHITE_THRESHOLD_SATURATION_MAX = 30

COLORFUL_PIXELS_REQUIRED = 1000

HUE_MARGIN = 10
SATURATION_MARGIN_MIN = 50
VALUE_MARGIN_MIN = 50

def readImageAsHSV(filename):
    BGR_image = cv2.imread(filename)
    HSV_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2HSV)
    return HSV_image

    
def getParametersFromImage(HSV_image):
    image_size = np.shape(HSV_image)[0]
    FILL_RATIO = 0.5
    return image_size, FILL_RATIO
    

def findMainColor(HSV_image):
    image_size, fill_ratio = getParametersFromImage(HSV_image)
    middle_px = image_size // 2
    #what about image height?
    counter = 0
    distance = 0
    hsv_list = []
    #collect colorful(non-black and non-white) pixels starting from center
    #procedure iterates through wider and wider squares until a certain amount is collected
    while(counter < COLORFUL_PIXELS_REQUIRED):
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
    print (hue_mean, saturation_mean, value_mean)
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

    SOME_MAGIC_HUE_THRESHOLD = 179

    lower_hue = HSV_mean[0] - HUE_MARGIN
    if lower_hue < 0:
        lower_hue += SOME_MAGIC_HUE_THRESHOLD
    if lower_hue > SOME_MAGIC_HUE_THRESHOLD:
        lower_hue -= SOME_MAGIC_HUE_THRESHOLD
    
    upper_hue = HSV_mean[0] + HUE_MARGIN
    if upper_hue < 0:
        upper_hue += SOME_MAGIC_HUE_THRESHOLD
    if upper_hue > SOME_MAGIC_HUE_THRESHOLD:
        upper_hue -= SOME_MAGIC_HUE_THRESHOLD
    
    lowerBound = (lower_hue, HSV_mean[1] - SATURATION_MARGIN_MIN, HSV_mean[2] - VALUE_MARGIN_MIN)
    upperBound = (upper_hue, 255, 255)
    
    if lowerBound[0] > upperBound[0]:
        mask1 = cv2.inRange(HSV_image, lowerb=(0, lowerBound[1], lowerBound[2]), upperb = upperBound) 
        mask2 = cv2.inRange(HSV_image, lowerb=lowerBound, upperb = (SOME_MAGIC_HUE_THRESHOLD, upperBound[1], upperBound[2]))
        mask = mask1 | mask2
    else:
        mask = cv2.inRange(HSV_image, lowerb = lowerBound, upperb = upperBound)
    return mask
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide image path")
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print("file does not exist")
        exit(2)

    znakPath = sys.argv[1]

    #does OpenCV return image as BGR by default?
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