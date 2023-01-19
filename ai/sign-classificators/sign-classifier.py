import sys
import os

from fastai.vision.all import *

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