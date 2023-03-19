'''
    tools for image preprocessing
'''

import cv2
import os

# scale img from W * L -> newWidth * (L * newWidth / W)
def scaleImg(img, newWidth): 
    size = img.shape 
    width = min(size[0], size[1]) # find which side is width (the smaller side)
    new_size = (int(size[1] * newWidth / width), int(size[0] * newWidth / width)) 
    scaled_img = cv2.resize(img, new_size) # scale to new_size
    return scaled_img 

# crop Image 
def cropImage(img, centerCoords, width, height):
    startRow = centerCoords[1] - int(height / 2)
    endRow = centerCoords[1] + int(height / 2)
    startCol = centerCoords[0] - int(width / 2)
    endCol = centerCoords[0] + int(width / 2)
    cropped = img[startRow:endRow, startCol:endCol]
    return cropped

# image preprocessing before passing to text detection code
def imgPreprocessing(img, newWidth, cropWidth, cropHeight): 
    # crop to only letter
    centerCoords = (int(img.shape[1] / 2), int(img.shape[0] / 2))
    cropped = cropImage(img, centerCoords, cropWidth, cropHeight)

    # scale the cropped so its bigger
    croppedScale = scaleImg(cropped, newWidth)

    # some blur and gray scale which help increase accuracy
    croppedBlur = cv2.GaussianBlur(croppedScale, (3,3), 0.5)
    croppedGray = cv2.cvtColor(croppedBlur, cv2.COLOR_BGR2GRAY)
    return croppedGray

