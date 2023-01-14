import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import circmean
from PIL import Image
import glob

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
    counter = 0
    distance = 0
    hsv_list = []
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
    
    lower_hue = HSV_mean[0] - HUE_MARGIN
    if lower_hue < 0:
        lower_hue += 179
    if lower_hue > 179:
        lower_hue -= 179
    
    upper_hue = HSV_mean[0] + HUE_MARGIN
    if upper_hue < 0:
        upper_hue += 179
    if upper_hue > 179:
        upper_hue -= 179
    
    lowerBound = (lower_hue, HSV_mean[1] - SATURATION_MARGIN_MIN, HSV_mean[2] - VALUE_MARGIN_MIN)
    upperBound = (upper_hue, 255, 255)
    
    if lowerBound[0] > upperBound[0]:
        mask1 = cv2.inRange(HSV_image, lowerb=(0, lowerBound[1], lowerBound[2]), upperb = upperBound) 
        mask2 = cv2.inRange(HSV_image, lowerb=lowerBound, upperb = (179, upperBound[1], upperBound[2]))
        mask = mask1 | mask2
    else:
        mask = cv2.inRange(HSV_image, lowerb = lowerBound, upperb = upperBound)
    return mask
    

# main
hue_mean, saturation_mean, value_mean = findMainColor(readImageAsHSV("znaki/A-7_2.jpg"))
HSV_mean = (hue_mean, saturation_mean, value_mean)
mask = makeMask(readImageAsHSV("znaki/A-7_2.jpg"), HSV_mean)
plt.imshow(mask, cmap='gray')
plt.savefig("aaaaaaa.jpg")