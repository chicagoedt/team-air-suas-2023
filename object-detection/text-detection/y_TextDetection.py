'''
    assume the inputed image has only one printed letter.
    detect the letter
'''

import cv2 # for reading image and processing image
import easyocr # a pytorch model that detects text and letters
import imutils # for rotating image
import time # for TESTING
from y_specialcase import *

def scaleImg(img, newWidth): 
    '''
    matrix, int -> matrix

    Scale an image from size (W * L) to size (newWidth * (newWidth * L / W)).

    Returns: a scaled img
    '''
    size = img.shape # a tuple (side1, side2, rgb)
    width = min(size[0], size[1]) # find which side is width (the smaller side)
    new_size = (int(size[1] * newWidth / width), int(size[0] * newWidth / width)) 
    scaled_img = cv2.resize(img, new_size) # scale to new_size
    return scaled_img 
    
def listRotations(img, step):
    '''
    matrix, int -> list

    Rotate an img from 0 to 360 (not including 360) with a step = inputed step.
    if step = 45 then we have 0, 45, 90, 135, 180, ..., 300, 345.

    Returns: a list of rotations of img. Each element (rotation) is a 2-elements tuple:
        - rotated img (matrix)
        - angle of rotation (int)
    '''
    rotations_list = []
    for i in range(0, 360, step):
        rotatedImg = imutils.rotate(img, i)
        rotations_list.append((rotatedImg, i))
    return rotations_list 

def detectLetter(rotations_list, reader):
    '''
    list -> tuple

    Pass all rotations to the model and pick the one that has best result: the model detects
    a letter with a confidence level of at least 90%
    
    Returns: a 4-elements tuple containing:
        - coordinates of a box surrounding letter (list)
        - letter (str) 
        - confidence level (int)
        - angle of rotation (int)
    Returns empty tuple if there is no good result
    '''
 
    # pass all rotated versions to model and get results
    for rotation in rotations_list: 
        result = reader.readtext(rotation[0])
        # print(rotation[1]) # for TESTING # angle
        # print(result) # for TESTING # detected text
        if len(result) != 0: # if it detects something from a rotated image
            if len(result[0][1]) == 1 and (result[0][1].isalpha() or result[0][1].isnumeric()) and result[0][2] >= 0.9:
                return result[0][0], result[0][1], result[0][2], rotation[1], rotation[0]   #TESTING: JUST REPLACE TUPLE WITH LIST
                 #  box coordinates, letter, confidence level, angle of rotation, the preprocessed image
    
    return rotation[1], rotation[0] # when all results are bad
            # angle of rotation, preprocessed image


# detect letter in img
def readImgDetectLetter(img, step, reader):
    '''
    Matrix, int, easyocr.Reader -> list
    '''
    rotations_list = listRotations(img, step)
    results = detectLetter(rotations_list, reader)
    # print(results)
    return results

# get all possibilities from result. e.g: if easyocr detects its an N, the letter could be N or Z
def resultsToPossibility(results):
    '''
    list -> list
    '''
    return specialCase(results[1])

# detect letter in img
def readImgPathDetectLetter(img_path, newWidth, step, reader):
    '''
    str, int, int, easyocr.Reader -> list
    '''
    startTime = time.time()
    # read img
    img = cv2.imread(img_path)

    # img preprocessing it, scale it to newWidth
    imgScaled = scaleImg(img, newWidth)
    # blur and gray scale the frame
    imgBlur = cv2.GaussianBlur(imgScaled, (7,7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    # create rotations_list
    results = readImgDetectLetter(imgGray, step, reader)
    print('Time:', time.time() - startTime)
    return results



