import cv2
import numpy as np
from numpy import ndarray
from sklearn.cluster import KMeans

class DominantColors:
    CLUSTERS = None
    IMAGE = None
    COLORS = None
    WIDTH = 40

    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image

#make the white frame around photo first
    def dominantColors(self):
        # read image
        img = cv2.imread(self.IMAGE)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #deleting whit fragments
        lower = np.array([0, 0, 30])  # -- Lower range --
        upper = np.array([255, 255, 255])  # -- Upper range --
        mask = cv2.inRange(img, lower, upper)
        res = cv2.bitwise_and(hsv, hsv, mask=mask)  # -- Contains pixels having the gray color--
        cv2.imshow('Result', res)
        cv2.waitKey(0)

        # reshaping to a list of pixels
        img = res.reshape((res.shape[1] * res.shape[0], 3))



        # save image after operations
        self.IMAGE = img

        # using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS)
        kmeans.fit(img)

        # the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        # returning after converting to integer from float
        return self.COLORS.astype(int)

    def printCol(self):

        thickness = -1

        image: ndarray = np.zeros((200,self.CLUSTERS*self.WIDTH,3))


        for i in range(self.CLUSTERS):
            start_point = (i*self.WIDTH, 0)
            end_point = ((i+1)*self.WIDTH, 200)
            color = int(self.COLORS[i][0])/255,int(self.COLORS[i][1])/255,int(self.COLORS[i][2])/255
            # print(color)
            # color = (255, 0, 0)
            image = cv2.rectangle(image, start_point, end_point, color, thickness)

        # image = cv2.rectangle(image, (0,0), (20,40),(0, 0, .7), thickness)
        window_name = 'Colors'
        cv2.imshow(window_name, image)
        print(self.COLORS.astype(int));
        cv2.waitKey(0)