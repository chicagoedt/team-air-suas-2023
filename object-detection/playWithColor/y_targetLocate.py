'''
    Goal: locate targets using color (except gray objects)
'''
import os
import cv2
import y_targetLocateHelper as targetLoc
import tool_testingHelper
import tool_imgPreprocessing as prepr

# init hypervariables
stdTargetMinSize = 40
stdTargetMaxSize = 120
stdMinAreaRatio = 1/3
stdImgTargetRatio = 10 / 6 # the ratio the size of crop target image and the size of target

# input images and folder
folderPath = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName_list = ['img_014_tar_253.jpg']
destFolderForCrop = 'cropImages'

# for each image get centerCoords, Area of target, Shape color, width * height of target
for imgName in imgName_list:
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # preprocessing image
    imgPreprocessed = targetLoc.imgPreprocessing(img)
    # cv2.imshow('imgPreprocessed', imgPreprocessed)   # TESTING
    # cv2.waitKey(0)                                   # TESTING

    # target locating
    maskFolder = 'maskFolder' # check maskFolder to understand
    TargetFound_list = targetLoc.targetLocation(imgPreprocessed, maskFolder, stdTargetMinSize, stdTargetMaxSize, stdMinAreaRatio)
    for targetFound in TargetFound_list:
        print(targetFound)
        # color, centerCoords, targetSize

    # cropping targets from input img / imgPreprocessed
    cropList = targetLoc.cropFoundTargets(imgPreprocessed, imgName, TargetFound_list, destFolderForCrop, True, stdImgTargetRatio)



