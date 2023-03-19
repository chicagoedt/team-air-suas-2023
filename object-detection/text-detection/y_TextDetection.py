'''
    tools for text detection.
    assume the inputed image has only one printed letter. detect the letter
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
            #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image

# detect letter in img
def readImgDetectLetter(img, reader, step):
    print('>> Begin readImgDetectLetter:')
    startTime = time.time()

    # get a list of rotations
    rotations_list = listRotations(img, step)

    # text Result
    result_list = detectLetter(rotations_list, reader)
    print('Time:', time.time() - startTime)
    print('>> End readImgdetectLetter.')
    return result_list
        #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image

# preprocess img, read preprocessed img, detect letter
def readImgDetectLetterWithPreprocessed(img, reader, scaledWidth, step, cropWidth, cropHeight):
    print('>> Begin readImgDetectLetterWithPreprocessed:')
    startTime = time.time()

    # preprocessed img
    processed = prepr.imgPreprocessing(img, scaledWidth, cropWidth, cropHeight)

    # get a list of rotations
    rotations = listRotations(processed, step)

    # text Result
    result_list = detectLetter(rotations, reader)
    print('Time:', time.time() - startTime)
    print('>> End readImgdetectLetterWithPreprocessed.')
    return result_list
        #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image


#--------------------------------------------------------

# check if target contains letter
def checkTargetHaveLetter(rotations_list, reader):
    targetHaveLetter = False
    # pass all rotated versions to model and get results
    for rotation in rotations_list: 
        output = reader.readtext(rotation[0])
        if len(output) != 0:
            targetHaveLetter = True
            break           
    
    return targetHaveLetter

def readImgCheckTargetHaveLetter(img, reader, step):
    print('>> Begin readImgCheckTargetHaveLetter:')
    startTime = time.time()

    # get a list of rotations
    rotations_list = listRotations(img, step)

    # text Result
    targetHaveLetter = checkTargetHaveLetter(rotations_list, reader)
    print('Time:', time.time() - startTime)
    print('>> End readImgCheckTargetHaveLetter.')
    return targetHaveLetter

# preprocess img, read img and check if having letter
def readImgCheckTargetHaveLetterWithPreprocessed(img, reader, scaledWidth, step, cropWidth, cropHeight):
    print('>> Begin readImgCheckTargetHaveLetterWithPreprocessed:')
    startTime = time.time()

    # preprocessed img
    processed = prepr.imgPreprocessing(img, scaledWidth, cropWidth, cropHeight)

    # get a list of rotations
    rotations = listRotations(processed, step)

    # text Result
    targetHaveLetter = checkTargetHaveLetter(rotations, reader)
    print('status:', targetHaveLetter)
    print('Time:', time.time() - startTime)
    print('>> End readImgCheckTargetHaveLetterWithPreprocessed.')
    return targetHaveLetter