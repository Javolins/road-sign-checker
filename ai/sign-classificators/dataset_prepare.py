import cv2
from crop_image import findMainColor
from crop_image import getInsideMask
from crop_image import getFinalMask
import numpy as np

import sys
import os

import re

from nnpaths import SignsNeuralNetworkPathBuilers

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

def thresholdWithMagentaBackground(BGR_image):
    HSV_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2HSV)
    HSV_mean = findMainColor(HSV_image)
    inside_mask = getInsideMask(HSV_image, HSV_mean)
    mask = getFinalMask(HSV_image, inside_mask)
    signWithMagendaBakcground = applyMagentaBackground(BGR_image, mask)
    return signWithMagendaBakcground

def preprocessSignImage(preprocessedDatasetDirPath, rawSignPath, signCode, signFileExtension, sampleTypeIndex):
    BGR_image = cv2.imread(rawSignPath)

    #add top and bottom border to adjust to 90x90 pixels(BIASED FOR WARNING SIGNS)
    BGR_image = cv2.copyMakeBorder(BGR_image, 5, 5, 0, 0, cv2.BORDER_REPLICATE)

    signWithMagendaBakcground = thresholdWithMagentaBackground(BGR_image)

    newFilename = signCode + '_' + str(sampleTypeIndex) + '.' + signFileExtension
    processedSignPath = preprocessedDatasetDirPath + '/' + newFilename
    cv2.imwrite(processedSignPath, signWithMagendaBakcground)
class RawDatasetDirDoesNotExistError(Exception):
    pass

def preprocessSigns(rawDatasetDirPath, preprocessedDatasetDirPath):
    #may raise RawDatasetDirDoesNotExistError exception
    if not os.path.exists(preprocessedDatasetDirPath):
        os.makedirs(preprocessedDatasetDirPath)

    try:
        rawSignsFilenames = os.listdir(rawDatasetDirPath)
    except NotADirectoryError:
        raise RawDatasetDirDoesNotExistError()

    roadSignFilenamePattern = r'([A-Z]-\d+[a-z]?)([\w-]+)?.(\w+)'
    roadSignFilenameRegex = re.compile(roadSignFilenamePattern)

    preprocessedSignFilenames = []
    for rawSignFilename in rawSignsFilenames:
        regexMatch = roadSignFilenameRegex.match(rawSignFilename)

        if regexMatch:
            signCode = regexMatch[1]
            signFileExtension = regexMatch[3]

            rawSignPath = rawDatasetDirPath + '/' + rawSignFilename
            preprocessSignImage(preprocessedDatasetDirPath, rawSignPath, signCode, signFileExtension, 0)

            preprocessedSignFilenames.append(rawSignFilename)

    return preprocessedSignFilenames

class PreprocessSignsResult:
    def __init__(self, outputDirPath, preprocessedSignFilenames):
        self.outputDirPath = outputDirPath
        self.preprocessedSignFilenames = preprocessedSignFilenames
def preprocessSignsForNN(subsetDirName):
    pathBuildr = SignsNeuralNetworkPathBuilers()
    rawDatasetDirPath = pathBuildr.getRawDatasetDirPath(subsetDirName)
    preprocessedDatasetDirPath = pathBuildr.getPreprocessedDatasetDirPath(subsetDirName)
    preprocessedSignFilenames = preprocessSigns(rawDatasetDirPath, preprocessedDatasetDirPath)
    result = PreprocessSignsResult(preprocessedDatasetDirPath, preprocessedSignFilenames)
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide sign subset name")
        exit(1)

    signSubsetName = sys.argv[1]

    try:
        preprocessedSignsResult = preprocessSignsForNN(signSubsetName, 4)
    except RawDatasetDirDoesNotExistError:
        print("raw dataset directory does not exist")
        exit(2)

    print("preprocessed signs filenames:")
    for filename in preprocessedSignsResult.preprocessedSignFilenames:
        print(filename)
