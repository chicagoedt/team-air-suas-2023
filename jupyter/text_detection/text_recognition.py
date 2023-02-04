'''
    assume the inputed image has only one printed letter.
    detect the letter
'''

import cv2 # for reading image and processing image
import easyocr # a pytorch model that detects text and letters
import imutils # for rotating image
import time # for TESTING

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

def detectLetter(rotations_list):
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
    reader = easyocr.Reader(['en']) # 'en' stands for reading in english. easyocr can read many languages like chinese, spanish,... but we care only english
    
    # pass all rotated versions to model and get results
    for rotation in rotations_list: 
        result = reader.readtext(rotation[0])
        print(rotation[1]) # for TESTING # angle
        print(result) # for TESTING # detected text
        if len(result) != 0: # if it detects something from a rotated image
            if len(result[0][1]) == 1 and ((result[0][1].isalpha() and result[0][1].isupper()) or (result[0][1].isnumeric())) and result[0][2] >= 0.9:
                return result[0][0], result[0][1], result[0][2], rotation[1]
                 #    box coordinates,  letter,  confidence level,  angle of rotation
    
    return () # when all results are bad

def readImgDetectLetter(img, step):
    rotations_list = listRotations(img, step)
    results = detectLetter(rotations_list)
    print(results)
    return results

if __name__ == '__main__':
    start_time = time.time()
    img_path = 'non scaled a.png'

    # read img to matrix and scale it
    img = cv2.imread(img_path) 
    
    scaled_img = scaleImg(img) 

    # create list of rotations
    rotations_list = listRotations(scaled_img)
    # for i in rotations_list:
    #     cv2.imshow(str(i[1]), i[0])
    #     cv2.waitKey(0)

    # detect Letter in image
    result = detectLetter(rotations_list)
    if len(result) != 0:
        print('detected letter:', result[1])
        print('confidence level:', result[2])
        print('angle of rotation:', result[3])
    else:
        print('there is NOTHING!?! **throws the laptop to the floor, paper scatters**  You f tricked me! WE ARE ON A BREAK!! **door slammed. a chilling breeze wipes someone\'s tear**')
    print('TIME:', round(time.time() - start_time, 2))


'''
So through some experiments, i realize that the speed and accuracy of text_recognition depends on :
    - newWidth (in scaleImage()): higher width means matrix is bigger, 
                                  which may increase accurracy but reduce time to process matrix.
                                  smaller width means matrix is smaller,
                                  which may reduce accurracy but gain speed to process matrix
    - step (in listRotation()): bigger step means lower accuracy but higher speed
                                lower step means higher accuracy but lower speed
'''

