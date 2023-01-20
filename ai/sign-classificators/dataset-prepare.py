import cv2
from crop_image import findMainColor
from crop_image import getInsideMask
import numpy as np

import sys
import os

import re

def createSameSizeBackground(imageTensor, color):
    backgroundImage = createSingleColoredImage(imageTensor.shape[1], imageTensor.shape[0], color)
    return backgroundImage

def createSingleColoredImage(width, height, color):
    colorMapKernel = np.array([[color]], np.uint8)
    colorImage = colorMapKernel.repeat(height, 0).repeat(width, 1)
    return colorImage

def combineImages(backgroundImage, foregroundImage, foregroundMask):
    maskedForeground = cv2.bitwise_and(foregroundImage, foregroundImage, mask=foregroundMask)

    backgroundMask = cv2.bitwise_not(foregroundMask)

    maskedBackground = cv2.bitwise_and(backgroundImage, backgroundImage, mask=backgroundMask)

    combinedImages = np.add(maskedBackground, maskedForeground)
    return combinedImages

def applyColorBackground(image, mask, color):
    colorBackground = createSameSizeBackground(image, color)
    imageWithBackground = combineImages(colorBackground, image, mask)
    return imageWithBackground
def applyMagentaBackground(image, mask):
    magentaColor = [255, 0, 255]
    imageWithMagentaBackground = applyColorBackground(image, mask, magentaColor)
    return imageWithMagentaBackground

def preprocessSigns(datasetDirPath, rawDataDirName, processedDataDirName, subsetDirName):
    rawDatasetDir = datasetDirPath + '/' + rawDataDirName
    rawSignsDir = rawDatasetDir + '/' + subsetDirName

    if not os.path.isdir(rawSignsDir):
        print("no such raw dataset directory")
        exit(2)

    processedSignsDirPath = datasetDirPath + '/' + processedDataDirName + '/' + subsetDirName

    if not os.path.exists(processedSignsDirPath):
        os.makedirs(processedSignsDirPath)

    rawSignsFilenames = os.listdir(rawSignsDir)

    roadSignFilenamePattern = r'([A-Z]-\d+[a-z]?)([\w-]+)?.(\w+)'
    roadSignFilenameRegex = re.compile(roadSignFilenamePattern)

    for rawSignFilename in rawSignsFilenames:
        regexMatch = roadSignFilenameRegex.match(rawSignFilename)
        signCode = regexMatch[1]
        signFileExtension = regexMatch[3]

        rawSignPath = rawSignsDir + '/' + rawSignFilename
        BGR_image = cv2.imread(rawSignPath)

        BGR_image = cv2.copyMakeBorder(BGR_image, 5, 5, 0, 0, cv2.BORDER_REPLICATE)

        HSV_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2HSV)
        HSV_mean = findMainColor(HSV_image)
        mask = getInsideMask(HSV_image, HSV_mean)
        signWithMagendaBakcground = applyMagentaBackground(BGR_image, mask)


        noCopies = 4
        for i in range(noCopies):
            newFilename = signCode + '_' + str(i) + '.' + signFileExtension
            processedSignPath = processedSignsDirPath + '/' + newFilename
            cv2.imwrite(processedSignPath, signWithMagendaBakcground)
            # if i == 0:
            #     cv2.imwrite(processedSignPath, signWithMagendaBakcground)
            # elif i == 1:
            #     cv2.imwrite(processedSignPath, cv2.rotate(signWithMagendaBakcground, cv2.ROTATE_90_CLOCKWISE))
            # elif i == 2:
            #     cv2.imwrite(processedSignPath, cv2.rotate(signWithMagendaBakcground, cv2.ROTATE_180))
            # elif i == 3:
            #     cv2.imwrite(processedSignPath, cv2.rotate(signWithMagendaBakcground, cv2.ROTATE_90_COUNTERCLOCKWISE))


def preprocessSignsForNN(subsetDirName):
    datasetsDirPath = 'nn/datasets'
    rawDataDirName = 'raw'
    processedDataDirName = 'preprocessed'
    preprocessSigns(datasetsDirPath, rawDataDirName, processedDataDirName, subsetDirName)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide sign subset name")
        exit(1)

    signSubsetName = sys.argv[1]

    preprocessSignsForNN(signSubsetName)