'''
    extract color from image
'''
# Task: find the range for red
import os
import cv2
import numpy as np
import y_colorFunc as color
import y_adaptToRealLife as adapt
import y_imgPreprocessing as prepr

def extractMask(imgHSV, lower_array, upper_array):
    lenArray = len(lower_array)
    mask_array = []
    for i in range(lenArray):
        mask = cv2.inRange(imgHSV, lower_array[i], upper_array[i])
        mask_array.append(mask)
    maskTotal = np.zeros((imgHSV.shape[0], imgHSV.shape[1]), dtype = np.uint8)
    for mask in mask_array:
        maskTotal = cv2.bitwise_or(maskTotal, mask)
    return maskTotal

folder_path = '/Users/mightymanh/Desktop/t1'
filename = 'Frame-15-03-2023-07-31-42.jpeg'

# path to image
# file_path = '/Users/mightymanh/Desktop/HSVrange.png'
file_path = os.path.join(folder_path, filename)
img = cv2.imread(file_path)


# scale target so it's big enough
imgScaled = img #cv2.resize(img, (300, 300))
imgScaledHSV = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2HSV)

# hsv bounds for color
lower_array = color.lowerBlack_array
upper_array = color.upperBlack_array


# extract color from imgScaled
maskTotal = extractMask(imgScaledHSV, lower_array, upper_array)
result = cv2.bitwise_and(imgScaled, imgScaled, mask = maskTotal)
cv2.imwrite('/Users/mightymanh/Desktop/mask.jpg', maskTotal)

# show images
cv2.imshow('Scaled', imgScaled)
cv2.imshow('mask', maskTotal)
cv2.imshow('result', result)
cv2.waitKey(0)

