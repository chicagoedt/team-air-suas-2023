'''
    functions that deal with real life image: light level
'''

import numpy as np
import cv2

import y_imgPreprocessing as prepr
from y_colorFunc import *

# stdSize = 130, stdScaledWidth = 130, stdCropSize = 60
def getScaleAndCrop(img_path, stdSize, stdScaledWidth, stdCropSize):
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
    return scaledWidth, cropSize

# give a background image measure light level
def measureBackgroundLightLevel(img):
    print('>> in measureBackgroundLightLevel: measuring light level of image and estimate its average color')
    imgScaled = prepr.scaleImg(img, 30)
    height = imgScaled.shape[0]
    width = imgScaled.shape[1]
    numPixel = 0

    # sum all pixels and get average
    sumB = 0
    sumG = 0
    sumR = 0
    for y in range(height):
        for x in range(width):
            if not (hsvInRangeArray(imgScaled[y][x], lowerWhite_array, upperWhite_array) or hsvInRangeArray(imgScaled[y][x], lowerBlack_array, upperBlack_array)):
                numPixel += 1
                sumB += imgScaled[y][x][0]
                sumG += imgScaled[y][x][1]
                sumR += imgScaled[y][x][2]
    
    averageColor = np.array([[[int(sumB / numPixel), int(sumG / numPixel), int(sumR / numPixel)]]], dtype = np.uint8)
    averageColorHSV = cv2.cvtColor(averageColor, cv2.COLOR_BGR2HSV)

    # light level of the average is the V value
    lightLevel = averageColorHSV[0][0][2]
    
    # show output
    print('average color: {}, light level: {}'.format(averageColor, lightLevel))
    print('>> end measureBackgroundLightLevel')
    return lightLevel

# get corresponding brightness change and contrast change depending on lightLevel
# to pass to function apply_brightness_contrast() in y_imgPreprocessing.py
def getBrightnessContrastChange(lightLevel):
    print('>> in getBrightnessContrastChange()')
    print('Light Level: {}'.format(lightLevel))
    
    brightnessChange = 0
    contrastChange = 0
    if 70 <= lightLevel and lightLevel <= 100: # this is light level of the simulated image
        pass
    elif 35 <= lightLevel and lightLevel <= 45:
        brightnessChange = 82
        contrastChange = 95
    else:  # if image is two bright
        brightnessChange = -105
        contrastChange = 95
    print('Brightness change: {}, Contrast change: {}'.format(brightnessChange, contrastChange))
    print('>> Finish getBrightnessContrastChange()')
    return brightnessChange, contrastChange


