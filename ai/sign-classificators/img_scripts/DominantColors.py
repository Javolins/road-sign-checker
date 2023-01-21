from sklearn.cluster import KMeans
import cv2
import numpy as np
import crop_image

class DominantColors:
    COLORS = None
    LABLES = None
    img = None
    n = None
    dellBackground = None
    delIndex = None
    
    # to remove background from color list add 1 color as background

    def __init__(self, n=3, dellBackground=True):
        self.n = n
        self.dellBackground = dellBackground
        self.kmeans = KMeans(n_clusters=n+dellBackground, n_init='auto')

    def imgPreper_save(self, imRGB, mask):
        self.img = self.imgPreper(imRGB, mask)
        return self.img

    def imgPreper(self, imRGB, mask):
        imRGB = crop_image.applyMask(imRGB, mask)
        if (self.dellBackground == True):
            backGC = np.zeros((imRGB.shape[0], imRGB.shape[1], 3), np.uint8)
            for i in backGC:
                for j in i:
                    j[1] = 222
            # add grean
            mask = cv2.bitwise_not(mask)
            
            imRGB = cv2.bitwise_or(imRGB, cv2.bitwise_and(backGC,backGC, mask=mask))
        return imRGB

    # pass prepered img
    # return array of colors in
    # contain last image added in imgPreper_save if no argument pass
    def n_dominant_colors(self, imRGB=None):
        # deleting whit fragments
        # if mask == None:
        #     lower = np.array([0, 0, 30])  # -- Lower range --
        #     upper = np.array([255, 255, 255])  # -- Upper range --
        #     mask = cv2.inRange(imRGB, lower, upper)
        # res = cv2.bitwise_and(imRGB, imRGB, mask=mask)  # -- Contains pixels having the gray color--
        if (imRGB is None):
            imRGB = self.img

        imRGB = imRGB.reshape((imRGB.shape[1] * imRGB.shape[0], 3))

        # save image after operations

        # using k-means to cluster pixels
        self.kmeans.fit(imRGB)

        # the cluster centers are our dominant colors.
        self.COLORS = np.uint8(self.kmeans.cluster_centers_).tolist()
        self.delIndex = 0
        for i in self.COLORS :
            if(i[0] <2 and  i[1] < 224 and  i[1] > 220 and i[2] < 2): # +-2
                del self.COLORS[self.delIndex]                
                break
            self.delIndex +=1
        # print(self.COLORS)
        
        return self.COLORS
    # return array of colors in hsv

    def n_dominant_colors_conv_to_hsv(self, imRGB=None):
        # type: ignore
        return cv2.cvtColor(np.uint8([self.n_dominant_colors(imRGB)]), cv2.COLOR_RGB2HSV)

    # return array of color covered arrea
    # be carefull if you change color order
    def get_size_of_color_covered_area(self):
        tab = np.zeros(self.n+1,np.uint).tolist()
        for i in self.kmeans.labels_:
            tab[i]+=1
        if(self.delIndex <=self.n ):
            del tab[self.delIndex]
        return tab

dmc = DominantColors()
