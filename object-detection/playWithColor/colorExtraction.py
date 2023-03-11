import os
import cv2
import numpy as np
from y_colorFunc import *
from y_colorDetectionHelper import *
from y_imgPreprocessing import *

# extract input hsv color from an imgHSV
def extractInputMask(imgHSV, lower_array, upper_array):
    lenArray = len(lower_array)
    mask_array = []
    for i in range(lenArray):
        mask = cv2.inRange(imgHSV, lower_array[i], upper_array[i])
        mask_array.append(mask)
    maskTotal = np.zeros((imgHSV.shape[0], imgHSV.shape[1]), dtype = np.uint8)
    for mask in mask_array:
        maskTotal = cv2.bitwise_or(maskTotal, mask)
    return maskTotal

# should be original imgHSV
def readImgPathExtractShapeAndLetterMask(imgPath):
    img = cv2.imread(imgPath)

    # get the shape and letter color
    cropped = cropImage(img, 30, 30)
    croppedHSV = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    shapeColor, letterColor = readImgHSVGetShapeAndLetterColor(croppedHSV)

    # extract shape and letter color
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # show
    original = scaleImg(img, 500)
    print('shape:', shapeColor)
    print('letter:', letterColor)
    cv2.imshow('original:', original)
    cv2.imshow('cropped:', cropped)
    if shapeColor != 'Gray':
        shapeMask = extractInputMask(imgHSV, colorDict[shapeColor][0], colorDict[shapeColor][1])
    if letterColor != 'Gray':
        letterMask = extractInputMask(imgHSV, colorDict[letterColor][0], colorDict[letterColor][1])
    if shapeColor != 'Gray' and letterColor != 'Gray':
        cv2.imshow('Shape mask', shapeMask)
        cv2.imshow('letter Color', letterMask)
    elif shapeColor != 'Gray':
        cv2.imshow('Shape mask', shapeMask)
    elif letterColor != 'Gray':
        cv2.imshow('letter Color', letterMask)
    cv2.waitKey(0)
    
    

