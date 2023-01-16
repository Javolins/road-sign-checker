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
        
        img = self.IMAGE

        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        # cv2.imshow('Result', hsv)
        # cv2.waitKey(0)

        #deleting whit fragments
        lower = np.array([0, 0, 30])  # -- Lower range --
        upper = np.array([255, 255, 255])  # -- Upper range --
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(hsv, hsv, mask=mask)  # -- Contains pixels having the gray color--
        # res = cv2.cvtColor(res, cv2.COLOR_HSV2RGB)
        # cv2.imshow('Result', res)
        # cv2.waitKey(0)

        # reshaping to a list of pixels
        res = res.reshape((res.shape[1] * res.shape[0], 3))

        

        # save image after operations
        self.IMAGE = img

        # using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS, n_init='auto')
        kmeans.fit(res)

        # the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        # returning after converting to integer from float
        # res = cv2.cvtColor(res, cv2.COLOR_HSV2RGB)
        kmeans.fit(res)
        
        return kmeans.cluster_centers_


    def printCol(self, image_col):

        thickness = -1

        image: ndarray = np.zeros((200,self.CLUSTERS*self.WIDTH,3))


        for i in range(self.CLUSTERS):
            start_point = (i*self.WIDTH, 0)
            end_point = ((i+1)*self.WIDTH, 200)
            color = np.uint8([[[ self.COLORS[i][0], self.COLORS[i][1],self.COLORS[i][2] ]]])
            color = cv2.cvtColor(color, cv2.COLOR_HSV2RGB)
            color = color[0][0]
            col= ( (color[0])/255,(color[1])/255,(color[2])/255)
            # print(col)
            image = cv2.rectangle(image, start_point, end_point, col, thickness)
        # print redHSV
        # image = cv2.rectangle(image, (0,0), (20,40),(0, 0, .7), thickness)
        # window_name = 'Colors'
        image_col.append(image)
        # print(self.COLORS.astype(int));
        # cv2.waitKey(0)
        
if __name__ == '__main__': 
    from matplotlib import pyplot as plt

    "A-1.png"
    glob_list = []
    image_list = []
    image_list_col = []
    
    filename= "../../znaki-sandbox/znaki/A-1.png"
   
    im = cv2.imread(filename)
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    image_list.append(im)
        
    img = image_list[0]
    dc = DominantColors(img)
    dmc = dc.dominantColors();# RGB
    dc.printCol(image_list_col)

    # image_list_col[0] = cv2.cvtColor(image_list_col[0], cv2.COLOR_RGB2BGR)
    cv2.imshow('Result', image_list_col[0])
    cv2.waitKey(0)
