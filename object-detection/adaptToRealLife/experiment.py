'''
    Goal: determine standard light level of background image
'''

import cv2
import os
import y_adaptToRealLife as adapt
import testingHelper as help

# init images
folderPath = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName_list = [i for i in os.listdir(folderPath) if len(i) == 19]
imgName_list = help.chooseRandomImages(imgName_list, 1000)

freqDict = {}
counter = 1
for imgName in imgName_list:
    print('{}> {}'.format(counter, imgName))
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)
    lightLevel = adapt.measureBackgroundLightLevel2(img)
    if lightLevel in freqDict:
        freqDict[lightLevel] += 1
    else:
        freqDict[lightLevel] = 1
    print('-----------------------------------------------')
    counter += 1

for lightLevel, freq in freqDict.items():
    print('{}: {}'.format(lightLevel, freq))

