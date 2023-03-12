'''
    assume the inputed image has only one printed letter.
    detect the letter
'''

import cv2                          # for reading image and processing image
import easyocr                      # a pytorch model that detects text and letters
import imutils                      # for rotating image
import time                         # for TESTING
import y_imgPreprocessing as prepr  # for image processing
from y_specialcase import *

# generate a list of rotations
def listRotations(img, step):
    rotations_list = []
    for i in range(0, 360, step):
        rotatedImg = imutils.rotate(img, i)
        rotations_list.append((rotatedImg, i))
    return rotations_list 

# get results from list of rotations
def detectLetter(rotations_list, reader):
    result_list = []
    # pass all rotated versions to model and get results
    for rotation in rotations_list: 
        output = reader.readtext(rotation[0])
        # print(rotation[1]) # for TESTING # angle
        # print(output) # for TESTING # detected text
        if len(output) != 0: # if it detects something from a rotated image
            if len(output[0][1]) == 1 and (output[0][1].isalpha() or output[0][1].isnumeric()) and output[0][2] >= 0.9:
                result = (output[0][0], output[0][1], round(output[0][2], 2), rotation[1], rotation[0])
                     #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image
                result_list.append(result)               
    
    return result_list

# detect letter in img
def readImgDetectLetter(img, step, reader):
    rotations_list = listRotations(img, step)
    result_list = detectLetter(rotations_list, reader)
    # print(results)
    return result_list

# read img but with preprocess image
def readImgDetectLetter2(img, reader, scaledWidth, step, cropWidth, cropHeight):
    print('>> Begin readImgDetectLetter2:')
    startTime = time.time()
    processed = prepr.imgPreprocessing(img, scaledWidth, cropWidth, cropHeight)
    rotations = listRotations(processed, step)
    result_list = detectLetter(rotations, reader)
    print('Time:', time.time() - startTime)
    print('>> End readImgdetectLetter2.')
    return result_list

# read image path detect letter
def readImgPathDetectLetter(img_path, reader, scaledWidth, step, cropWidth, cropHeight):
    startTime = time.time()
    img = cv2.imread(img_path)
    processed = prepr.imgPreprocessing(img, scaledWidth, cropWidth, cropHeight)
    rotations = listRotations(processed, step)
    result_list = detectLetter(rotations, reader)
    print('Time:', time.time() - startTime)
    return result_list

