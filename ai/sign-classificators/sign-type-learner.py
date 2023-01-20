from fastai.data.transforms import get_image_files

from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.augment import aug_transforms

import re

from matplotlib import pyplot

from fastai.vision.all import *

def learnNNForSpecificSignType(typeName):
    neuralNetworkDirPath = 'nn'
    prepreocessedDatasetsDirPath = neuralNetworkDirPath + '/datasets/preprocessed'
    signsDataSetDir = prepreocessedDatasetsDirPath + '/' + typeName

    if not os.path.exists(neuralNetworkDirPath):
        os.makedirs(neuralNetworkDirPath)

    learnerOutputDirPath = neuralNetworkDirPath + '/learner/' + typeName

    if not os.path.exists(learnerOutputDirPath):
        os.makedirs(learnerOutputDirPath)

    znakiFiles = get_image_files(signsDataSetDir)

    labels_pattern = r'([A-Z]-\d+[a-z]?)_(\d+).\w+'
    rgxp = re.compile(labels_pattern)
    rgxp.match(znakiFiles[0].name)

    dls = ImageDataLoaders.from_name_re(learnerOutputDirPath, znakiFiles, labels_pattern, bs=4, batch_tfms=aug_transforms(do_flip=False))

    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.lr_find()

    epochs = 20
    learn.fine_tune(epochs)

    modelFilename = typeName + '.pkl'
    modelPath = os.path.abspath(neuralNetworkDirPath + '/' + modelFilename)
    learn.export(modelPath)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("provide sign subset name")
        exit(1)

    signSubsetName = sys.argv[1]

    learnNNForSpecificSignType(signSubsetName)