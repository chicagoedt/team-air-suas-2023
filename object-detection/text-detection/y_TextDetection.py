'''
    Given a target image, read letter on it
'''

import os
import cv2
import easyocr
import y_TextDetectionHelper as textDetect

# init hyper variables
stdSize = 125
stdScaledWidth = 125
stdCropSize = 50
step = 10

# init images
reader = easyocr.Reader(['en'])
folderPath = '../playWithColor/cropImages'
imgName_list = ['img_014_tar_253_2258-2000_Yellow.jpg']

for imgName in imgName_list:
    print(imgName)

    # read img
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # read letter
    textDetect.deepReadImgDetectLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step)
