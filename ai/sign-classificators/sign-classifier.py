import sys
import os

from fastai.vision.all import *

from enum import Enum;

class SignType(Enum):
    WARNING = 'warn'
    PROHIBITION = 'proh'
    WARRANT = 'warnt'
    INFORMATIONAL = 'info'

class SignsNeuralNetworkPathBuilers:
    def __init__(self):
        self.nnDirPath = os.path.abspath('nn')
        self.datasetsDirName = 'datasets'
        self.rawDatasetDirName = 'datasets'
        self.preprocessedDatasetDirName = 'datasets'
        self.learnerFilesDirName = 'learner'
        self.modelsDirName = 'models'

    def getModelPath(self, signType):
        modelFilename = signType + '.pkl'
        modePath = os.path.join(self.nnDirPath, self.modelsDirName, modelFilename)
        return modelPath

    def getRawDatasetDirPath(self, signType):
        rawDatasetPath = os.path.join(self.nnDirPath, self.datasetsDirName, signType, self.rawDatasetDirName)
        return rawDatasetPath

    def getPreprocessedDatasetDirPath(self, signType):
        preprossedDatasetPath = os.path.join(self.nnDirPath, self.datasetsDirName, signType, self.preprocessedDatasetDirName)
        return preprossedDatasetPath

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide sign type")
        exit(1)

    neuralNetworkDirPath = 'nn'
    signClassifierModel = neuralNetworkDirPath + '/' + sys.argv[1] + '.pkl'

    if not os.path.exists(signClassifierModel):
        print("model does not exist")
        exit(2)

    if len(sys.argv) < 3:
        print("provide input image path")
        exit(3)

    inputImagePath = sys.argv[2]
    if not os.path.exists(inputImagePath):
        print("input image does not exist")
        exit(4)

    learner = load_learner(signClassifierModel)
    print(learner.dls.vocab)
    predictionResult = learner.predict(inputImagePath)
    print(predictionResult)

    predictionDict = {}
    vocabLength = len(learner.dls.vocab)
    for dictElementIndex in range(vocabLength):
        dictElement = learner.dls.vocab[dictElementIndex]
        elementPredictionValue = predictionResult[2][dictElementIndex]
        predictionDict[dictElement] = float(elementPredictionValue)

    print(predictionDict)
    sortedPredictions = dict(sorted(predictionDict.items(), key=lambda item: item[1], reverse=True))
    print(sortedPredictions)

    #posotruj predictions od największej do najmniejszej i zwróć posortowany słownik klasyfikacji
