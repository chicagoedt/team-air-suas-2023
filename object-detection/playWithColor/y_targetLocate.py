'''
    Goal: locate targets using color (except gray objects), assuming input image is 4K (3K is still fine)
'''
import os
import cv2
import y_targetLocateHelper as targetLoc
import testingHelper
import y_imgPreprocessing as prepr

# init hypervariables
stdTargetMinSize = 40
stdTargetMaxSize = 120
stdMinAreaRatio = 1/3
stdImgTargetRatio = 10 / 6 # the ratio the size of crop target image and the size of target

# input images and folder
folderPath = '/Users/mightymanh/Desktop/15march'
imgName_list = ['Frame-15-03-2023-07-31-04.jpeg']
destFolderForCrop = 'cropImages'

# for each image get centerCoords, Area of target, Shape color, width * height of target
for imgName in imgName_list:
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # preprocessing image
    imgPreprocessed = targetLoc.imgPreprocessing(img)
    # cv2.imshow('imgPreprocessed', imgPreprocessed)   # TESTING
    # cv2.waitKey(0)

    # target locating
    maskFolder = 'maskFolder' # check maskFolder to understand
    TargetFound_list = targetLoc.targetLocalization(imgPreprocessed, maskFolder, stdTargetMinSize, stdTargetMaxSize, stdMinAreaRatio)
    for targetFound in TargetFound_list:
        print(targetFound)
        # color, centerCoords, targetSize

    # cropping targets from input img / imgPreprocessed
    cropList = targetLoc.cropFoundTargets(imgPreprocessed, imgName, TargetFound_list, destFolderForCrop, True, stdImgTargetRatio)



