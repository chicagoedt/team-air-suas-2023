import numpy as np
import cv2
import os
import y_adaptToRealLife as adapt
import ShapeDetector as SD


folderPath = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023/object-detection/playWithColor/cropImages'
imgName_list = [i for i in os.listdir(folderPath) if len(i) >= 7 and i[-4:] == '.jpg']

for imgName in imgName_list:
    print(imgName)
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)
    contourImg, _, _ = SD.findShape(img)
    cv2.imshow('contour', contourImg)
    cv2.waitKey(0)
