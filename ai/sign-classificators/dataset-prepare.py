import os
import cv2
from crop_image import findMainColor
from crop_image import getInsideMask
import numpy as np

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

    maskedSign = cv2.bitwise_and(BGR_image, BGR_image, mask=mask)
    cv2.imshow("znak z maska", maskedSign)

    normalizedMask = mask / 255

    invertedMask = cv2.bitwise_not(mask)

    invertedMaskTensor = np.repeat(invertedMask[:, :, np.newaxis], 3, axis=2)

    invertedMaskTensorNorm = invertedMaskTensor/255

    magentaMap = np.array([[[255, 0, 255]]], np.uint8)
    magentaTensor = magentaMap.repeat(invertedMask.shape[0], 0).repeat(invertedMaskTensor.shape[1], 1)
    magentaTensor.astype(np.uint8)

    print(magentaTensor[:10, :10])

    cv2.imshow("magenta", magentaTensor)

    magentaBackground = cv2.bitwise_and(magentaTensor, magentaTensor, mask=invertedMask)
    cv2.imshow("magenta background", magentaBackground)

    signWithMagendaBakcground = np.add(magentaBackground, maskedSign)
    cv2.imshow("sign with background", signWithMagendaBakcground)

    cv2.waitKey(0)