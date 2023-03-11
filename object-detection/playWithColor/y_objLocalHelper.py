'''
    Helper functions for objLocal.py
'''

import cv2
import numpy as np
import os
from y_colorFunc import *                    # color
import y_adaptToRealLife as adapt            # real image: light level
import y_imgPreprocessing as prepr           # preprocessing img

def extractMask(imgHSV, lower_array, upper_array):
    lenArray = len(lower_array)
    mask_array = []
    for i in range(lenArray):
        mask = cv2.inRange(imgHSV, lower_array[i], upper_array[i])
        mask_array.append(mask)
    maskTotal = np.zeros((imgHSV.shape[0], imgHSV.shape[1]), dtype = np.uint8)
    for mask in mask_array:
        maskTotal = cv2.bitwise_or(maskTotal, mask)
    return maskTotal

# preprocessing img before locating targets
def imgPreprocessing(img, stdLightLevelRange): # set stdLightLevel = 72
    lightLevel = adapt.measureBackgroundLightLevel(img)
    brightnessChange, contrastChange = adapt.getBrightnessContrastChange(lightLevel, stdLightLevelRange)
    img = prepr.apply_brightness_contrast(img, brightnessChange, contrastChange)
    return img

# return a list of color-filtered masks
def collectingMasks(img):
    print('>> Begin collecting masks')
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # collecting mask
    maskList = []
    for color in colorDict.keys():
        lowerArray, upperArray = colorDict[color]
        mask = extractMask(imgHSV, lowerArray, upperArray)
        maskList.append((color, mask))
    print('>> Finish collecting masks')
    return maskList

# write masks to a folder
def writeMaskToMaskFolder(maskList, destFolder):
    print('>> Begin writing mask')
    imgName_list = []
    for mask in maskList:
        maskName = mask[0] + '.jpg'
        imgName_list.append(maskName)
        print('Writing mask image {}'.format(maskName))
        destPath = os.path.join(destFolder, maskName)
        cv2.imwrite(destPath, mask[1])
    
    print('>> Finish writing mask:', imgName_list)
    return imgName_list

# main function that locates targets and also determine its shape color
def targetLocalization(img, maskFolder, stdTargetMinSize = 40, stdTargetMaxSize = 120):

    # collect mask
    mask_list = collectingMasks(img)

    # write masks to a folder
    imgName_list = writeMaskToMaskFolder(mask_list, maskFolder)

    # target localization
    TargetFound_list = []
    print('>> Begin locating targets')
    for imgName in imgName_list:
        print(imgName)
        imgPath = os.path.join(maskFolder, imgName)
        img = cv2.imread(imgPath)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # same as ShapeDetector in Chris Code
        contours, _ = cv2.findContours(imgGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # datas
            M = cv2.moments(contour)
            if M['m00'] < 500:
                continue
            
            print('Area:', M['m00'])
            cx = int(M['m10']/M['m00'])    # comment to see behavior
            cy = int(M['m01']/M['m00'])
            print('Centroid:', (cx, cy))

            # bounding box
            rect = cv2.minAreaRect(contour)
            width, height = rect[1]
            print('Width: {}, Height: {}'.format(width, height))

            if M['m00'] < ((width * height) * 1/3):
                continue

            if stdTargetMinSize <= width and width <= stdTargetMaxSize and stdTargetMinSize <= height and height <= stdTargetMaxSize:
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                img = cv2.drawContours(img,[box],0,(0,255,255),2)
                TargetFound_list.append(((cx, cy), M['m00'], imgName[0:-4], (width, height))) # center, area, color, dimension
            print('-----------------------------------------')

        print('#################################################')
        cv2.imshow(imgName, img)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    print('>> Finish locating targets')
    print('found coordinates:', TargetFound_list)
    return TargetFound_list
