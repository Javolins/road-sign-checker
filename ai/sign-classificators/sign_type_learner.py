from fastai.data.transforms import get_image_files

from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.augment import aug_transforms

import re

from matplotlib import pyplot

from fastai.vision.all import *

from nnpaths import SignsNeuralNetworkPathBuilers

def learnNNForSpecificSignType(datasetDirPath, modelName, epochs):
    #@return path to trained model
    pathBuilder = SignsNeuralNetworkPathBuilers()
    learnerOutputDirPath = pathBuilder.getLearnerDirPath(modelName)

    if not os.path.exists(learnerOutputDirPath):
        os.makedirs(learnerOutputDirPath)

    znakiFiles = get_image_files(datasetDirPath)

    labels_pattern = r'([A-Z]-\d+[a-z]?)_(\d+).\w+'
    rgxp = re.compile(labels_pattern)
    rgxp.match(znakiFiles[0].name)

    dls = ImageDataLoaders.from_name_re(learnerOutputDirPath, znakiFiles, labels_pattern, bs=4, item_tfms=Resize(90),
                                        batch_tfms=aug_transforms(do_flip=False))

    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.lr_find()

    epochs = 20
    learn.fine_tune(epochs)

    modelPath = pathBuilder.getModelPath(modelName)
    learn.export(modelPath)

    return modelPath


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

    pathBuilder = SignsNeuralNetworkPathBuilers()
    preprocessedDatasetDirPath = pathBuilder.getPreprocessedDatasetDirPath(signSubsetName)

    learnNNForSpecificSignType(preprocessedDatasetDirPath, signSubsetName, epochs)