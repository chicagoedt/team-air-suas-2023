'''
    Goal: locate objects using color (except gray objects)
'''
import os
import cv2
import y_targetLocateHelper as targetLoc
import testingHelper
import y_imgPreprocessing as prepr

# init hypervariables
stdLightLevelRange = (70, 100)
stdTargetMinSize = 40
stdTargetMaxSize = 120
stdImgTargetRatio = 10 / 6 # the ratio the size of crop target image and the size of target

# input images and folder
folderPath = '/Users/mightymanh/Desktop/t1'
imgName_list = ['Frame-15-03-2023-07-34-06.jpeg']
destFolderForCrop = 'cropImages'

# for each image get centerCoords, Area of target, Shape color, width * height of target
for imgName in imgName_list:
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # preprocessing image
    imgPreprocessed = targetLoc.imgPreprocessing(img)

    # target locating
    maskFolder = 'maskFolder' # check maskFolder to understand
    TargetFound_list = targetLoc.targetLocalization(imgPreprocessed, maskFolder, stdTargetMinSize, stdTargetMaxSize)
    for targetFound in TargetFound_list:
        print(targetFound)
        # centerCoords, area, shape color, width * height

    # cropping targets
    targetLoc.cropFoundTargets(imgPreprocessed, imgName, TargetFound_list, destFolderForCrop, True, stdImgTargetRatio)



