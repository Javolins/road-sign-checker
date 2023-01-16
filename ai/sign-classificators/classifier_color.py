from sklearn.cluster import KMeans
import numpy as np
import cv2

def n_dominant_colors(imRGB ,n=3):
    
    #deleting whit fragments
    # if mask == None:
    #     lower = np.array([0, 0, 30])  # -- Lower range --
    #     upper = np.array([255, 255, 255])  # -- Upper range --
    #     mask = cv2.inRange(imRGB, lower, upper)
    # res = cv2.bitwise_and(imRGB, imRGB, mask=mask)  # -- Contains pixels having the gray color--

    imRGB = imRGB.reshape((imRGB.shape[1] * imRGB.shape[0], 3))   

    # save image after operations

    # using k-means to cluster pixels
    kmeans = KMeans(n_clusters=n, n_init='auto')
    kmeans.fit(imRGB)

    # the cluster centers are our dominant colors.
    kmeans.cluster_centers_
    
    return kmeans.cluster_centers_.astype(np.uint8)

def n_dominant_colors_conv_to_hsv(imRGB,n=3): 
    return cv2.cvtColor(np.uint8([n_dominant_colors(imRGB ,n)]), cv2.COLOR_RGB2HSV) # type: ignore


#color , color2 - colory porównywane między sobą in HSV
def dopasowanieKoloru(a, color2):
    dh = (1-min(abs(a[0]-color2[0]), 179-abs(a[0]-color2[0]))/179)**3
    ds = (1-abs(a[1]-color2[1]) /255)
    dv = (1-abs(a[2]-color2[2]) / 255.0 )   
    return (dh*ds*dv)

def checkWhite(color):
    return abs(color[2]) / 255.0   *(abs(255-color[1]) / 255.0)**3   

def checkBlack(color):    
    return 1-(abs(255-color[2]) / 255.0   )

class estymarotZnaku:
    def __init__(self):
        pass
        
    def est(self, arr):            

        return [self.checkA(arr),          
        self.checkB(arr) ,          
        self.checkC(arr)]
    
    def checkA(self,col):
        yelow = [ 30,   240,   240]
        red =   [0,   240,   240]
        yd = 0
        bd = 0
        rd = 0
        for i in col:
            yd= max(yd,dopasowanieKoloru(yelow, i))
            rd= max(rd,dopasowanieKoloru(red, i))
            bd= max(bd,1-checkWhite( i))
        return yd*.5+rd*.4 +bd*.1
    
    def checkB(self,col):
        red = [ 0,   250,   250]
        yd = 0
        bd = 0
        rd = 0
        for i in  col:
            yd= max(yd,dopasowanieKoloru(red, i))
            # rd= max(rd,checkWhite( i))
            bd= max(bd,1-checkWhite( i))
        return yd*.9 +bd*.1#+rd*.4
    
    def checkC(self,col):
        blue = [ 109,   230,   210]#101 243 199 on ideal
        yd = 0
        rd = 0
        for i in  col:
            yd= max(yd,dopasowanieKoloru(blue, i))
            rd= max(rd,checkWhite( i))
        return yd*.8+rd*.2
        
def compareFn(a, b):
    if a[0]==b[0]:
        if a[1]==b[1]:
            if a[2]==b[2]:
                return 0
            else:
                return a[2]-b[2]
        else:
            return a[1]-b[1]
    else:
        return a[0]-b[0]
    
def sortCol(arr):
    if compareFn(arr[0], arr[1])>0:
        tmp = arr[0].copy()
        arr[0] = arr[1]
        arr[1] = tmp
    if compareFn(arr[1], arr[2])>0:
        tmp= arr[1].copy()
        arr[1]= arr[2]
        arr[2]= tmp
    if compareFn(arr[0], arr[1])>0:
        tmp = arr[0].copy()
        arr[0]= arr[1]
        arr[1]= tmp