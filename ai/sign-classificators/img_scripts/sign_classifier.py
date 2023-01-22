import sys
import os

from nnpaths import SignsNeuralNetworkPathBuilers
from dataset_prepare import applyMagentaBackground
from dataset_prepare import thresholdWithMagentaBackground

from fastai.vision.all import *

class ClassificationResult:
    def __init__(self, predictionsDescending):
        self.predictionsDescending = predictionsDescending

    def getClassifiedType(self):
        firstKey = list( self.predictionsDescending.keys())[0]
        return firstKey

    def getClassificationValue(self):
        firstValue = list(self.predictionsDescending)[0]
        return firstValue
    def getPredictions(self):
        return self.predictionsDescending
class SignClassifier:

    def createPredictionDict(self, predictionResult):
        predictionDict = {}
        vocabLength = len(self.model.dls.vocab)
        for dictElementIndex in range(vocabLength):
            dictElement = self.model.dls.vocab[dictElementIndex]
            elementPredictionValue = predictionResult[2][dictElementIndex]
            predictionDict[dictElement] = float(elementPredictionValue)

        return predictionDict

    def sortPredictionDict(self, predictionDict):
        sortedPredictions = dict(sorted(predictionDict.items(), key=lambda item: item[1], reverse=True))
        return sortedPredictions

    def createSortedPredictionDict(self, predictionResult):
        predictionDict = self.createPredictionDict(predictionResult)
        sortedPredictions = self.sortPredictionDict(predictionDict)
        return sortedPredictions

    def __init__(self, modelPath):
        self.model = load_learner(modelPath)
    def classifySign(self, preprocessedSign):
        #@preprocessedSign path to image or PILImage object
        predictionResult = self.model.predict(preprocessedSign)
        sortedPredictions = self.createSortedPredictionDict(predictionResult)
        classificationResult = ClassificationResult(sortedPredictions)
        return classificationResult

    def preprocessAndClassify(self, BGR_image, mask):
        preprocessedSign = applyMagentaBackground(BGR_image, mask)
        classificationResult = self.classifySign(preprocessedSign)
        return classificationResult

    def binarizeAndClassify(self, BGR_image):
        preprocessedSign = thresholdWithMagentaBackground(BGR_image)
        classificationResult = self.classifySign(preprocessedSign)
        return classificationResult

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide sign type")
        exit(1)

    signType = sys.argv[1]

    pathBuilder = SignsNeuralNetworkPathBuilers()
    modelPath = pathBuilder.getModelPath(signType)

    if not os.path.exists(modelPath):
        print("model does not exist")
        exit(2)

    if len(sys.argv) < 3:
        print("provide input image path")
        exit(3)

    inputImagePath = sys.argv[2]
    if not os.path.exists(inputImagePath):
        print("input image does not exist")
        exit(4)

    classifier = SignClassifier(modelPath)
    classifyResult = classifier.binarizeAndClassify(inputImagePath)
    print("result")
    print(classifyResult.getClassifiedType())
    print("vector")
    print(classifyResult.getPredictions())
