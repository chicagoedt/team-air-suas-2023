'''
    functions that deal with real life image: light level
'''

import numpy as np
import cv2

import y_imgPreprocessing as prepr
from y_colorFunc import *

# stdSize = 130, stdScaledWidth = 130, stdCropSize = 60
def getScaleAndCrop(img_path, stdSize, stdScaledWidth, stdCropSize):
    print('>> Begin getScaleAndCrop:')
    img = cv2.imread(img_path)
    height = img.shape[0]
    width = img.shape[1]
    print(f'height: {height}, width: {width}')
    averageSize = int((height + width) / 2)
    cropSize = int(stdCropSize * averageSize / stdSize)
    scaledWidth = int(stdScaledWidth * averageSize / stdSize)

    # special case
    if cropSize < stdCropSize:
        cropSize = stdCropSize
    if scaledWidth < stdScaledWidth:
        scaledWidth = stdScaledWidth
    print(f'cropSize: {cropSize}, scaledWidth: {scaledWidth}')
    print('>> End getScaleAndCrop')
    return scaledWidth, cropSize

# give a background image measure light level
def measureBackgroundLightLevel(img):
    print('>> in measureBackgroundLightLevel2: measuring light level of image and estimate its average color')
    imgScaled = prepr.scaleImg(img, 30)
    imgScaledHSV = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2HSV)
    height = imgScaled.shape[0]
    width = imgScaled.shape[1]
    numPixel = 0

    # sum all pixels and get average
    sumH = 0
    sumS = 0
    sumV = 0
    for y in range(height):
        for x in range(width):
            if not (hsvInRangeArray(imgScaledHSV[y][x], lowerWhite_array, upperWhite_array) or hsvInRangeArray(imgScaledHSV[y][x], lowerBlack_array, upperBlack_array)):
                numPixel += 1
                sumH += imgScaled[y][x][0]
                sumS += imgScaled[y][x][1]
                sumV += imgScaled[y][x][2]
    
    averageColorHSV = np.array([[[int(sumH / numPixel), int(sumS / numPixel), int(sumV / numPixel)]]], dtype = np.uint8)
    
    # light level of the average is the V value
    lightLevel = averageColorHSV[0][0][2]
    
    # show output
    print('average HSV color: {}, light level: {}'.format(averageColorHSV, lightLevel))
    print('>> end measureBackgroundLightLevel2')
    return lightLevel

# get corresponding brightness change and contrast change depending on lightLevel
# to pass to function apply_brightness_contrast() in y_imgPreprocessing.py
def getBrightnessContrastChange(lightLevel, stdLightLevelRange):
    print('>> in getBrightnessContrastChange()')
    print('Light Level: {}, standard light level: {}'.format(lightLevel, stdLightLevelRange))
    
    brightnessChange = 0
    contrastChange = 0
    if stdLightLevelRange[0] <= lightLevel and lightLevel <= stdLightLevelRange[1]:
        pass
    else:
        brightnessChange = -105
        contrastChange = 95
    print('Brightness change: {}, Contrast change: {}'.format(brightnessChange, contrastChange))
    print('>> Finish getBrightnessContrastChange()')
    return brightnessChange, contrastChange




'''
    need a light level table
'''