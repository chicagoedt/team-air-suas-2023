'''
    Goal: locate objects using color (except gray objects)
'''
import os
import cv2
import y_objLocalHelper as objloc
import testingHelper as help

# init hypervariables
stdLightLevelRange = (70, 100)
stdTargetMinSize = 40
stdTargetMaxSize = 120

# init images
folderPath = '../ImagesByCamera'
imgName_list = ['img_000_tar_005.jpg']

# for each image get centerCoords, Area of target, Shape color, width * height of target
for imgName in imgName_list:
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # preprocessing image
    img = objloc.imgPreprocessing(img, stdLightLevelRange)
    cv2.imshow('img', img)
    cv2.waitKey(0)

    # target locating
    maskFolder = 'maskFolder' # check maskFolder to understand
    TargetFound_list = objloc.targetLocalization(img, maskFolder, stdTargetMinSize, stdTargetMaxSize)
    print(len(TargetFound_list))
    # centerCoords, area, shape color, width * height
