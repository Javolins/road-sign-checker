from fastai.data.transforms import get_image_files

from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.augment import aug_transforms

import re

import os

from matplotlib import pyplot

from fastai.vision.all import *

from nnpaths import SignsNeuralNetworkPathBuilers

class LearningResult:
    def __init__(self, dls, learner, modelPath):
        self.dls = dls
        self.model = learner
        self.modelPath = modelPath

class SpecificSignTypeLearner:
    def __init__(self, datasetDirPath, modelName, sampleRepeats):
        self.datasetDirPath = datasetDirPath
        rootPath = os.path.join(__file__, '..')
        pathBuilder = SignsNeuralNetworkPathBuilers(rootPath)
        self.modelPath = pathBuilder.getModelPath(modelName)

        learnerOutputDirPath = pathBuilder.getLearnerDirPath(modelName)

        if not os.path.exists(learnerOutputDirPath):
            os.makedirs(learnerOutputDirPath)

        znakiFiles = get_image_files(datasetDirPath)
        filesLen = len(znakiFiles)
        znakiPaths = []
        for i in range(sampleRepeats):
            for j in range(filesLen):
                znakiPaths.append(znakiFiles[j])

        labels_pattern = r'([A-Z]-\d+[a-z]?)_(\d+).\w+'
        rgxp = re.compile(labels_pattern)
        rgxp.match(znakiFiles[0].name)

        self.dls = ImageDataLoaders.from_name_re(learnerOutputDirPath, znakiPaths, labels_pattern, shuffle=True, bs=4,
                                            item_tfms=Resize(90),
                                            batch_tfms=aug_transforms(do_flip=False))

        self.model = vision_learner(self.dls, resnet18, metrics=error_rate)
        self.model.lr_find()

    def tuneModel(self, additionalEpochs):
        self.model.fine_tune(additionalEpochs)
        self.model.export(self.modelPath)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide sign subset name")
        exit(1)

    signSubsetName = sys.argv[1]

    if len(sys.argv) < 3:
        print("provide number of epochs")
        exit(2)

    try:
        epochs = int(sys.argv[2])
    except ValueError:
        print("epochs is not a valid integer")
        exit(3)

    rootPath = os.path.abspath(os.path.join(__file__, '..', '..'))
    pathBuilder = SignsNeuralNetworkPathBuilers(rootPath)
    preprocessedDatasetDirPath = pathBuilder.getPreprocessedDatasetDirPath(signSubsetName)

    learner = SpecificSignTypeLearner(preprocessedDatasetDirPath, signSubsetName)
    learner.tuneModel(epochs)