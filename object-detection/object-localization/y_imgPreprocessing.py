import cv2
import os


def scaleImg(img, newWidth): 
    size = img.shape # a tuple (side1, side2, rgb)
    width = min(size[0], size[1]) # find which side is width (the smaller side)
    new_size = (int(size[1] * newWidth / width), int(size[0] * newWidth / width)) 
    scaled_img = cv2.resize(img, new_size) # scale to new_size
    return scaled_img 

def cropImage(img, width, height):
    centerCoords = (int(img.shape[1] / 2), int(img.shape[0] / 2))
    
    startRow = centerCoords[1] - int(height / 2)
    endRow = centerCoords[1] + int(height / 2)
    startCol = centerCoords[0] - int(width / 2)
    endCol = centerCoords[0] + int(width / 2)
    cropped = img[startRow:endRow, startCol:endCol]
    return cropped

def imgPreprocessing(img, scaledWidth, cropWidth, cropHeight): # set newWidth to 100
    # crop to only letter
    cropped = cropImage(img, cropWidth, cropHeight)
    croppedScale = scaleImg(cropped, scaledWidth)
    croppedBlur = cv2.GaussianBlur(croppedScale, (3,3), 0.5)
    croppedGray = cv2.cvtColor(croppedBlur, cv2.COLOR_BGR2GRAY)
    return croppedGray

