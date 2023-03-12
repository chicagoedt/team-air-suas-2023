'''
    Goal: locate objects using color (except gray objects)
'''
import os
import cv2
import y_objLocalHelper as objloc
import testingHelper as help
import y_imgPreprocessing as prepr

# init hypervariables
stdLightLevelRange = (70, 100)
stdTargetMinSize = 40
stdTargetMaxSize = 120

# input images
folderPath = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName_list = ['img_008_tar_009.jpg']

# for each image get centerCoords, Area of target, Shape color, width * height of target
for imgName in imgName_list:
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # preprocessing image
    imgPreprocessed = objloc.imgPreprocessing(img, stdLightLevelRange)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)

    # target locating
    maskFolder = 'maskFolder' # check maskFolder to understand
    TargetFound_list = objloc.targetLocalization(imgPreprocessed, maskFolder, stdTargetMinSize, stdTargetMaxSize)
    for targetFound in TargetFound_list:
        print(targetFound)
    # centerCoords, area, shape color, width * height

    # cropping targets
    destFolder = 'cropImages'
    # clear dest_folder first
    oldFiles = os.listdir(destFolder)
    if len(oldFiles) != 0:
        for file in oldFiles:
            os.remove(os.path.join(destFolder, file))

    for targetFound in TargetFound_list:
        try:
            centerCoords = (int(targetFound[0][0]), int(targetFound[0][1]))
            crop = prepr.cropImage(imgPreprocessed, centerCoords, 130, 130)
            print(crop.shape)
            cropName = str(centerCoords[0]) + '_' + str(centerCoords[1]) + '_' + targetFound[2] + '.jpg'
            cropPath = os.path.join(destFolder, cropName)
            cv2.imwrite(cropPath, crop)
        except:
            pass
        
