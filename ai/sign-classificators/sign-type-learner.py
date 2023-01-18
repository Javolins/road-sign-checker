from fastai.data.transforms import get_image_files

from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Resize
from fastai.vision.augment import aug_transforms

import re

from matplotlib import pyplot

from fastai.vision.all import *

if __name__ == '__main__':
    signsDataSetDir = 'nn-dataset/preprocessed/warn'
    learner_output_dir = '.'
    znakiFiles = get_image_files(signsDataSetDir)

    labels_pattern = r'([A-Z]-\d+[a-z]?).\w+'
    rgxp = re.compile(labels_pattern)
    rgxp.match(znakiFiles[0].name)

    dls = ImageDataLoaders.from_name_re(learner_output_dir, znakiFiles, labels_pattern, bs=4)
    #dls.show_batch()

    #pyplot.show()

    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.lr_find()

    pyplot.show()