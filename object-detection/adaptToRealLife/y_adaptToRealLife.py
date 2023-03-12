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

def measureBackgroundLightLevel(img):
    print('>> in measureBackgroundLightLevel: measuring light level of image and estimate its average color')
    imgScaled = prepr.scaleImg(img, 30)
    height = imgScaled.shape[0]
    width = imgScaled.shape[1]
    numPixel = height * width

    # sum all pixels and get average
    sumB = 0
    sumG = 0
    sumR = 0
    for y in range(height):
        for x in range(width):
            sumB += imgScaled[y][x][0]
            sumG += imgScaled[y][x][1]
            sumR += imgScaled[y][x][2]
    
    averageColor = np.array([[[int(sumB / numPixel), int(sumG / numPixel), int(sumR / numPixel)]]], dtype = np.uint8)
    averageColorHSV = cv2.cvtColor(averageColor, cv2.COLOR_BGR2HSV)
    
    # light level of the average is the V value
    lightLevel = averageColorHSV[0][0][2]
    
    # show output
    print('average BGR color: {}, light level: {}'.format(averageColor, lightLevel))
    print('>> end measureBackgroundLightLevel')
    return lightLevel

# get light level of target img
def measureTargetLightLevel(img):
    print('>> in measureTargetLightLevel:')
    height = img.shape[0]
    width = img.shape[1]
    numPixel = height + width - 1

    # sum pixels in first row and first column, get average
    sumB = 0
    sumG = 0
    sumR = 0
    for y in range(height):
        sumB += img[y][0][0] 
        sumG += img[y][0][1] 
        sumR += img[y][0][2] 

    for x in range(1, width):
        sumB += img[0][x][0]
        sumG += img[0][x][1]
        sumR += img[0][x][2]
    
    averageColor = np.array([[[int(sumB / numPixel), int(sumG / numPixel), int(sumR / numPixel)]]], dtype = np.uint8)
    averageColorHSV = cv2.cvtColor(averageColor, cv2.COLOR_BGR2HSV)
    
    # light level is the V value of average HSV pixel
    lightLevel = averageColorHSV[0][0][2]

    # show output
    print('average BGR color: {}, light level: {}'.format(averageColor, lightLevel))
    print('>> end measureTargetLightLevel')

    return lightLevel

# get corresponding brightness change and contrast change depending on lightLevel
# to pass to function apply_brightness_contrast() in y_imgPreprocessing.py
def getBrightnessContrastChange(lightLevel, stdLightLevel):
    print('>> in getBrightnessContrastChange()')
    difference = stdLightLevel - lightLevel
    print('Light Level: {}, standard light level: {} => difference = {}'.format(lightLevel, stdLightLevel, difference))
    
    brightnessChange = 0
    contrastChange = 0
    if abs(difference) <= 10:
        pass
    else:
        brightnessChange = -105
        contrastChange = 95
    print('Brightness change: {}, Contrast change: {}'.format(brightnessChange, contrastChange))
    print('>> Finish getBrightnessContrastChange()')
    return brightnessChange, contrastChange


def measureBackgroundLightLevel2(img):
    print('>> in measureBackgroundLightLevel: measuring light level of image and estimate its average color')
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
    print('>> end measureBackgroundLightLevel')
    return lightLevel


'''
    need a light level table
'''