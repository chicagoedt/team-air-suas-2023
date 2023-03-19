'''
    functions that deal with variety of size of image.
'''

import numpy as np
import cv2

import y_imgPreprocessing as prepr

# stdSize = 125, stdScaledWidth = 100, stdCropSize = 50
# input target img, get the right size to crop and size to scale up
def getScaleAndCrop(img, stdSize, stdScaledWidth, stdCropSize):
    print('>> Begin getScaleAndCrop:')
    height = img.shape[0]
    width = img.shape[1]

    # get cropSize and scaledWidth
    averageSize = int((height + width) / 2)
    cropSize = int(stdCropSize * averageSize / stdSize)
    scaledWidth = int(stdScaledWidth * averageSize / stdSize)

    # special case
    if cropSize < stdCropSize:
        cropSize = stdCropSize
    if scaledWidth < stdScaledWidth:
        scaledWidth = stdScaledWidth
    print(f'image has height: {height}, width: {width} -> We need cropSize: {cropSize}, scaledWidth: {scaledWidth}')
    print('>> End getScaleAndCrop')
    return scaledWidth, cropSize
