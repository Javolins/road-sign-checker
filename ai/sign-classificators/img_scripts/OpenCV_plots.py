import cv2
from matplotlib import pyplot as plt
import os
import math

def plotOpenCV(BGRImage):
    rgbImg = cv2.cvtColor(BGRImage, cv2.COLOR_BGR2RGB)  # Converts from one colour space to the other
    plt.imshow(rgbImg)
    plt.show()

def plotGrid(dirPath):
    preprocessedSampleNames = os.listdir(dirPath)
    numberOfOutputSamples = len(preprocessedSampleNames)
    columns = 4
    rows = math.ceil(numberOfOutputSamples / 4)
    fig = plt.figure()
    plt.subplots_adjust(top = 0.99, bottom=0.01, hspace=1.5)
    for i in range(numberOfOutputSamples):
        subplotIndex = i + 1
        plt.subplot(rows, columns, subplotIndex)
        imageFilename = preprocessedSampleNames[i]
        imagePath = os.path.join(dirPath, imageFilename)
        BGRImage = cv2.imread(imagePath)
        rgbImg = cv2.cvtColor(BGRImage, cv2.COLOR_BGR2RGB)  # Converts from one colour space to the other
        plt.imshow(rgbImg)
        plt.title(imageFilename)