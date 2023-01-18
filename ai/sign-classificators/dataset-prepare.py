import cv2
from crop_image import findMainColor
from crop_image import getInsideMask
import numpy as np

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

if __name__ == '__main__':
    learningSetDirectory = 'znaki_idealne'
    filename = 'A-1.png'
    path = learningSetDirectory + '/' + filename
    BGR_image = cv2.imread(path)

    border = 100
    BGR_image = cv2.copyMakeBorder(BGR_image, border, border, border, border, cv2.BORDER_CONSTANT, value=0)

    cv2.imshow("załadowany", BGR_image)

    HSV_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2HSV)
    HSV_mean = findMainColor(HSV_image)
    mask = getInsideMask(HSV_image, HSV_mean)

    cv2.imshow("maska", mask)

    signWithMagendaBakcground = applyMagentaBackground(BGR_image, mask)
    cv2.imshow("sign with background", signWithMagendaBakcground)

    cv2.waitKey(0)