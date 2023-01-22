import cv2
import numpy
from PIL import Image
from fastai.vision.core import PILImage
def PILToOpenCV(imgPIL):
    #return OpenCV BGR image
    pilArray = numpy.array(imgPIL)
    opencvImage = cv2.cvtColor(pilArray, cv2.COLOR_RGB2BGR)
    return opencvImage
def OpenCVToPIL(openCVImage):
    #opencv image in BGR format
    img = cv2.cvtColor(openCVImage, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    fastaiPIL = PILImage(im_pil)
    return fastaiPIL