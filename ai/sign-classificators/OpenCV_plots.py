import cv2
from matplotlib import pyplot as plt
def plotOpenCV(BGRImage):
    rgbImg = cv2.cvtColor(BGRImage, cv2.COLOR_BGR2RGB)  # Converts from one colour space to the other
    plt.imshow(rgbImg)
    plt.show()