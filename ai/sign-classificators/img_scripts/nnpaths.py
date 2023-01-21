from enum import Enum
import os
class SignType(Enum):
    WARNING = 'warning'
    PROHIBITION = 'proh'
    WARRANT = 'warrant'
    INFORMATIONAL = 'info'

class SignsNeuralNetworkPathBuilers:
    def __init__(self):
        self.nnDirPath = os.path.abspath('nn')
        self.datasetsDirName = 'datasets'
        self.rawDatasetDirName = 'raw'
        self.preprocessedDatasetDirName = 'preproc'
        self.learnerFilesDirName = 'learner'
        self.modelsDirName = 'models'

    def getModelPath(self, signType):
        modelFilename = signType + '.pkl'
        modelsDirPath = os.path.join(self.nnDirPath, self.modelsDirName)
        if not os.path.exists(modelsDirPath):
            os.makedirs(modelsDirPath)

        modelPath = os.path.join(modelsDirPath, modelFilename)
        return modelPath

    def getRawDatasetDirPath(self, signType):
        rawDatasetPath = os.path.join(self.nnDirPath, self.datasetsDirName, signType, self.rawDatasetDirName)
        return rawDatasetPath

    def getPreprocessedDatasetDirPath(self, signType):
        preprossedDatasetPath = os.path.join(self.nnDirPath, self.datasetsDirName, signType, self.preprocessedDatasetDirName)
        return preprossedDatasetPath

    def getLearnerDirPath(self, signType):
        learnerDirPath = os.path.join(self.nnDirPath, self.learnerFilesDirName, signType)
        return learnerDirPath