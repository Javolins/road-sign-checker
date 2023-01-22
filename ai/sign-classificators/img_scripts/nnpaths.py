from enum import Enum
import os
class SignType(Enum):
    WARNING = 'warning'
    PROHIBITION = 'proh'
    WARRANT = 'warrant'
    INFORMATIONAL = 'info'
    WARRANT_INFORMATIONAL = 'warnt-info'

class SignsNeuralNetworkPathBuilers:
    def __init__(self, path):
        self.nnDirPath = os.path.join(path, 'nn')
        print(type(self.nnDirPath))
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
