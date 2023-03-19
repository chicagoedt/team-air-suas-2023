'''
    read input images and detect letters
'''

import os
import cv2
import easyocr
import y_TextDetection as textDetect    # text detection
import y_adaptToRealLife as adapt       # get cropSize and scaledWidth
import y_imgPreprocessing as prepr      # img preprocessing
import testingHelper as help
import mainHelper
import time

# init hyper variables
stdSize = 125
stdScaledWidth = 120
stdCropSize = 45

# init images
reader = easyocr.Reader(['en'])
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023/object-detection/playWithColor/cropImages'
imgName_list = [i for i in os.listdir(folder_path) if i[-4:] == '.jpg']


targetList = []

start = time.time()

# check if target is valid: check if target has letter
step = 20
print('##################### Check target has letter #####################\n')
for imgName in imgName_list:
    print(imgName)
    img_path = os.path.join(folder_path, imgName)
    img = cv2.imread(img_path)
    TargetHaveLetter = mainHelper.checkImgHavingLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step)
    if TargetHaveLetter:
        targetList.append(imgName)
    print('--------------------------------------')

# deep read
step = 10
print('\n\n################# Deep read ######################\n')
for target in targetList:
    print(target)
    img_path = os.path.join(folder_path, target)
    img = cv2.imread(img_path)
    mainHelper.deepReadImgReadLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step)
    print('--------------------------------------')

print('Overall time:', time.time() - start)