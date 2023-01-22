from sklearn.cluster import KMeans
import DominantColors
import numpy as np

#color , color2 - colory porównywane między sobą in HSV
def dopasowanieKoloru(a, color2):
    dh = (1-min(abs(a[0]-color2[0]), 179-abs(a[0]-color2[0]))/179)**3
    ds = (1-abs(a[1]-color2[1]) /255)
    dv = (1-abs(a[2]-color2[2]) / 255.0 )   
    return (dh*ds*dv)

def checkWhite(color):
    return abs(color[2]) / 255.0   *(abs(255-color[1]) / 255.0)**3   

#1 if color is black
def checkBlack(color):    
    return (abs(255-color[2]) / 255.0   )

def howDif(mesure , expected ):
    return 1 - abs(mesure -expected)

class estymarotZnaku:
    def __init__(self):
        # self.i = 0 ;
        pass
    #arr [nx3] coveraget [n]
    def est(self, arr, coverage):            

        return [self.checkA(arr, coverage, sum(coverage)),          
        self.checkB(arr, coverage,sum(coverage)) ,          
        self.checkC(arr, coverage,sum(coverage))]
    
    def checkA(self,col,coverage, allField):
        yelow = [ 30,   240,   240]
        red =   [0,   240,   240]
        yd = 0
        yc = 0
        bd = 0
        bc = 0
        rd = 0
        rc = 0
        for i, f in zip(col,coverage):
            tmp = dopasowanieKoloru(yelow, i)
            if(tmp > yd):
                yd = tmp
                yc = f
            tmp = dopasowanieKoloru(red, i)
            if(tmp > rd):
                rd = tmp
                rc = f
            tmp = checkBlack( i)
            if(tmp > bd):
                bd = tmp
                bc = f
        sum = bc+yc
        if sum > allField:
            sum = max(bc,yc)   
        return (yd*.5 +bd*.1)*howDif((sum)/allField, 0.8) +rd*.4*howDif(rc/allField, 0.2)
    
    def checkB(self,col,coverage, allField):
        red = [ 0,   250,   250]
        yd = 0
        bd = 0
        wd = 0
        yc = 0
        bc = 0
        wc = 0
        for i, f in zip(col,coverage):
    
            tmp = dopasowanieKoloru(red, i)
            if(tmp > yd):
                yd = tmp
                yc = f
            tmp = checkWhite( i)                
            if(tmp > yd):
                wd = tmp
                wc = f
            tmp = checkBlack( i)                
            if(tmp > yd):
                bd = tmp
                bc = f
        sum = yc +wc 
        if sum > allField:
            sum = max(yc,wc) 
        return (yd*.45 + wd *.45)*howDif(sum/allField,0.8) +bd*.1 * howDif(bc/allField,0.2)
    
    def checkC(self,col,coverage, allField):
        blue = [ 109,   230,   210]#101 243 199 on ideal
        yd = 0
        bd = 0
        wd = 0
        yc = 0
        bc = 0
        wc = 0
        for i, f in zip(col,coverage): 
            tmp = dopasowanieKoloru(blue, i)               
            if(tmp > yd):
                yd = tmp
                yc = f
            tmp = checkWhite(i)
            if(tmp > yd):
                wd = tmp
                wc = f
            tmp = checkBlack( i)                
            if(tmp > yd):
                bd = tmp
                bc = f
        sum = bc +wc 
        if sum > allField:
            sum = max(bc,wc) 
        return yd*.8 *howDif(yc/allField, 0.45) +( wd*.1+bd*.1)* howDif(sum/allField, 0.55)
est = estymarotZnaku()

def finalColorClasifaier(imgRGB, mask):
    DominantColors.dmc.imgPreper_save(imgRGB, mask)
    # color is returned as img 
    color = DominantColors.dmc.n_dominant_colors_conv_to_hsv()
    return est.est(color[0],DominantColors.dmc.get_size_of_color_covered_area())
