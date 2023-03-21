'''
    given target image, detect shape color and letter color
'''

import cv2
import os
import y_colorDetectionHelper as colorDetect

# init hyper variables
stdCropColorRatio = 40 / 125

# init images
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName_list = ['img_014_tar_214_S.jpg']

for imgName in imgName_list:
    print(imgName)
    imgPath = os.path.join(folder_path, imgName)
    img = cv2.imread(imgPath)

    # get shape and letter color
    shapeColor, letterColor = colorDetect.readImgGetShapeAndLetterColor(img, stdCropColorRatio)

