'''
    Helper functions for y_targetLocate.py
'''

import cv2
import numpy as np
import os
import y_colorFunc as colorFunc              # color
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

# detect shapes that is valid (valid size and valid area)
def findShape(img, imgName, targetMinSize, targetMaxSize, minAreaRatio):

    # gray scale img
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # get list of contours
    contours, _ = cv2.findContours(imgGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # process each contour and grab contour whose size in range targetMinSize and targetMaxSize
    possibleTarget_list = []
    for contour in contours:

        # min bounding box of Target
        rect = cv2.minAreaRect(contour)
        width, height = rect[1]
        width = int(width)
        height = int(height)

        # filter contours with valid size
        if targetMinSize <= width and width <= targetMaxSize and targetMinSize <= height and height <= targetMaxSize:
            M = cv2.moments(contour)

            # skip if the area is not valid
            area = M['m00']
            if area < ((width * height) * minAreaRatio):
                continue

            # gen centroid of contour
            cx = int(M['m10']/M['m00']) 
            cy = int(M['m01']/M['m00'])
            centroid = (cx, cy)

            # get average size of target
            _, _, width1, height1 = cv2.boundingRect(contour) # width1, height1 is different to width, height
            averageSize = int((width1 + height1) / 2)
            
            # add to the list
            print('Info about contour: width: {}, height: {}, area: {}, centroid: {}, average size: {}'.format(width, height, area, centroid, averageSize))
            possibleTarget_list.append([imgName, centroid, averageSize])

    #         # draw the yellow box around the target
    #         box = cv2.boxPoints(rect)
    #         box = np.intp(box)              # not sure if this line is necessary  # uncomment for TESTING
    #         img = cv2.drawContours(img, [box], 0, (0,255,255), 2)
    # cv2.imshow(imgName, img)   # for TESTING
    # cv2.waitKey(0)

    return possibleTarget_list

# main function that locates targets and also determine its shape color
def targetLocation(img, maskFolder, stdTargetMinSize, stdTargetMaxSize, stdAreaRatio):

    # collect mask
    mask_list = collectingMasks(img)

    # write masks to a folder
    imgName_list = writeMaskToMaskFolder(mask_list, maskFolder)

    # target localization
    TargetFound_list = []
    print('>> Begin targetLocation:')
    for imgName in imgName_list:
        print(imgName)
        color = nameHelper.cutExtension(imgName)
        imgPath = os.path.join(maskFolder, imgName)
        img = cv2.imread(imgPath)
        # detect possible targets
        TargetFound_list.extend(findShape(img, color, stdTargetMinSize, stdTargetMaxSize, stdAreaRatio))
        print('------------------------------------------------')
    
    print('>> Finish targetLocation!')
    return TargetFound_list
            # color, centroid, averageSize

# cropping targets from input img
# after locating the possibile targets, crop them and save them to dest folder
def cropFoundTargets(img, imgName, TargetFound_list, destFolder, enableClearOldFiles, ImgTargetRatio):
    print('>> Begin cropFoundTargets. Clear old files =', enableClearOldFiles)
    if enableClearOldFiles:
        # clear destFolder first
        oldFiles = os.listdir(destFolder)
        if len(oldFiles) != 0:
            for file in oldFiles:
                os.remove(os.path.join(destFolder, file))

    crop_list = []
    # for each found target, crop it
    for targetFound in TargetFound_list:
        
        # get info of target
        centerCoords = (int(targetFound[1][0]), int(targetFound[1][1]))
        originalImgName = nameHelper.cutExtension(imgName)
        shapeColor = targetFound[0]
        targetSize = targetFound[2]
    
        # crop target and add crop to crop_list
        cropSize = int(targetSize * ImgTargetRatio)
        print('targetSize: {}, ImgTargetRatio: {} -> cropSize: {}'.format(targetFound[2], ImgTargetRatio, cropSize))
        crop = prepr.cropImage(img, centerCoords, cropSize, cropSize)
        crop_list.append((originalImgName, centerCoords, shapeColor, crop))

        # FOR EXPORTING CROP TO IMAGES
        # get name for crop file, get path for crop file
        cropName = originalImgName + '_' + str(centerCoords[0]) + '-' + str(centerCoords[1]) + '_' + shapeColor + '.jpg'
                   # <originalImgName>_<centerCoords>_<targetShapeColor>.jpg
        print('creating file {}\n-----------------------------------'.format(cropName))
        
        # write crop to destFolder
        cropPath = os.path.join(destFolder, cropName)
        cv2.imwrite(cropPath, crop)
    print('>> Finish cropFoundTargets!')

    return crop_list
