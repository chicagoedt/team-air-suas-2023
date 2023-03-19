

import cv2
import os
import easyocr
import y_imgPreprocessing as prepr
import testingHelper as help
import y_TextDetection as textDetect
import y_adaptToRealLife as adapt
import mainHelper

# init hyper variables
stdSize = 125
stdScaledWidth = 120
stdCropSize = 45
step = 20

# init images
reader = easyocr.Reader(['en'])
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023/object-detection/playWithColor/cropImages'
imgName_list = [i for i in os.listdir(folder_path) if i[-4:] == '.jpg']

for imgName in imgName_list:
    print(imgName)
    imgPath = os.path.join(folder_path, imgName)
    img = cv2.imread(imgPath)

    # check letter
    TargetHaveLetter = mainHelper.checkImgHavingLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step)