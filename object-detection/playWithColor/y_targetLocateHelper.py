'''
    Helper functions for objLocal.py
'''

import cv2
import numpy as np
import os
import y_colorFunc as colorFunc                    # color
import y_adaptToRealLife as adapt            # real image: light level
import y_imgPreprocessing as prepr           # preprocessing img
import nameFormatHelper as nameHelper        # deal with file name

# preprocessing img before locating targets
def imgPreprocessing(img):
    lightLevel = adapt.measureBackgroundLightLevel(img)
    brightnessChange, contrastChange = adapt.getBrightnessContrastChange(lightLevel)
    print('brightnessChange: {}, contrastChange: {}'.format(brightnessChange, contrastChange))
    img = prepr.apply_brightness_contrast(img, brightnessChange, contrastChange)
    return img

# return a list of color-filtered masks
def collectingMasks(img):
    print('>> Begin collecting masks')
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # collecting mask
    maskList = []
    for color in colorFunc.colorDict.keys():
        lowerArray, upperArray = colorFunc.colorDict[color]
        mask = colorFunc.extractMask(imgHSV, lowerArray, upperArray)
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
def targetLocalization(img, maskFolder, stdTargetMinSize, stdTargetMaxSize):

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
            if M['m00'] < 500:     # very messy, need to clean this guy
                continue
            
            print('Area:', M['m00'])
            cx = int(M['m10']/M['m00'])    # comment to see behavior
            cy = int(M['m01']/M['m00'])
            print('Centroid:', (cx, cy))

            # bounding box
            rect = cv2.minAreaRect(contour)
            width, height = rect[1]
            width = int(width)
            height = int(height)

            _, _, width1, height1 = cv2.boundingRect(contour)
            averageSize = int((width1 + height1) / 2)
            print('Width: {}, Height: {}, Width1: {}, Height1, averageSize: {}'.format(width, height, width1, height1, averageSize))

            if M['m00'] < ((width * height) * 1/3):
                continue

            if stdTargetMinSize <= width and width <= stdTargetMaxSize and stdTargetMinSize <= height and height <= stdTargetMaxSize:
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                img = cv2.drawContours(img,[box],0,(0,255,255),2)
                TargetFound_list.append(((cx, cy), M['m00'], imgName[0:-4], (width, height), averageSize)) # center, area, color, dimension
            print('-----------------------------------------')

        print('#################################################')
        # cv2.imshow(imgName, img)   # for TESTING
        # cv2.waitKey(0)

    cv2.destroyAllWindows()
    print('>> Finish locating targets!')
    return TargetFound_list

# after locating the possibile targets, crop them and save them to dest folder
def cropFoundTargets(img, imgName, TargetFound_list, destFolder, enableClearOldFiles, ImgTargetRatio):
    print('>> Begin cropFoundTargets. Clear old files =', enableClearOldFiles)
    if enableClearOldFiles:
        # clear destFolder first
        oldFiles = os.listdir(destFolder)
        if len(oldFiles) != 0:
            for file in oldFiles:
                os.remove(os.path.join(destFolder, file))

    # for each found target, crop it
    for targetFound in TargetFound_list:
        # get cropSize 
        cropSize = int(targetFound[4] * ImgTargetRatio)
        print('targetSize: {}, ImgTargetRatio: {} -> cropSize: {}'.format(targetFound[4], ImgTargetRatio, cropSize))

        # crop target
        centerCoords = (int(targetFound[0][0]), int(targetFound[0][1]))
        crop = prepr.cropImage(img, centerCoords, cropSize, cropSize)
        
        # get name for crop file, get path for crop file
        imgNameWithoutExtension = nameHelper.cutExtension(imgName)
        cropName = imgNameWithoutExtension + '_' + str(centerCoords[0]) + '-' + str(centerCoords[1]) + '_' + targetFound[2] + '.jpg'
                   # <imgName>_<centerCoords>_<targetShapeColor>.jpg
        print('creating file {}\n-----------------------------------'.format(cropName))
        
        # write crop to destFolder
        cropPath = os.path.join(destFolder, cropName)
        cv2.imwrite(cropPath, crop)
    print('>> Finish cropFoundTargets!')
