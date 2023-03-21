'''
    Goal: determine light level of image
'''

import cv2
import os
import tool_adaptToRealLife as adapt
import tool_testingHelper as help

# init images
folderPath = '/Users/mightymanh/Desktop/15march'
imgName_list = [i for i in os.listdir(folderPath) if i[-4:] == '.jpg' or i[-5:] == '.jpeg']
print('Number of img in the list:', len(imgName_list))

# stats variable
freqDict = {}
counter = 0
sum = 0

# measure light level of runaway
for imgName in imgName_list:
    print('{}> {}'.format(counter, imgName))
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)

    # measure light level of img
    lightLevel = adapt.deepMeasureBackgroundLightLevel(img)

    # add to list for later stats analysis
    if lightLevel in freqDict:
        freqDict[lightLevel] += 1
    else:
        freqDict[lightLevel] = 1
    print('-----------------------------------------------')
    counter += 1
    sum += lightLevel

# print stats
for lightLevel, freq in freqDict.items():
    print('{}: {}'.format(lightLevel, freq))
average = sum / counter
print('average: {}'.format(average))
