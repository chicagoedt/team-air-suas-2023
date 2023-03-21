'''
    first, run y_targetLocate.py in playWithColor/ to get possible targets
    Then, we determine which target is valid (which target has letter) and read the letter
'''

import os
import cv2
import easyocr
import time

import y_TextDetectionHelper as textDetect
import y_checkTargetHaveLetterHelper as checkTarget


# init hyper variables
stdSize = 125
stdScaledWidth = 120
stdCropSize = 50

# init model and start timer
reader = easyocr.Reader(['en'])
start = time.time()

# init images
folder_path = '../playWithColor/cropImages'
imgName_list = [i for i in os.listdir(folder_path) if i[-4:] == '.jpg']

# check if target is valid: check if target has letter
targetList = []
step = 20
print('##################### Check target has letter #####################\n')
for imgName in imgName_list:
    print(imgName)
    img_path = os.path.join(folder_path, imgName)
    img = cv2.imread(img_path)
    TargetHaveLetter = checkTarget.deepReadImgCheckTargetHaveLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step)
    if TargetHaveLetter:
        targetList.append(imgName)
    print('--------------------------------------')

# deep read the target that has letter
step = 10
print('\n\n################# Deep read ######################\n')
for target in targetList:
    print(target)
    img_path = os.path.join(folder_path, target)
    img = cv2.imread(img_path)
    textDetect.deepReadImgDetectLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step)
    print('--------------------------------------')

print('Overall time:', time.time() - start)