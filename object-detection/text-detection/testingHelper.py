from y_letterImageMapping import *    # textDetection, letterImageMapping
import os                             # listdir, path.join
import numpy as np                    # pdf generator
from PIL import Image                 # pdf generator
import itertools                      # permutation
import random                         # shuffleList
import statistics                     # mean, median, stdDev
from y_specialcase import *

''' ----- helper function for getAccuracyOfTextDetection() ----- '''
# stack orignal and result image (these imgs are read by cv2)
def stackHorizontal(imgName, imgScaled, results, possibility):
    # build gutter
    height = imgScaled.shape[0]
    gutter = np.full((height, 3, 3), 255, dtype = np.uint8)

    # build imgResult
    imgResult = cv2.cvtColor(results[-1], cv2.COLOR_GRAY2BGR)
    if len(results) == 5:
        box = results[0] 
        cv2.rectangle(imgResult, [int(box[0][0]), int(box[0][1])], [int(box[2][0]), int(box[2][1])], (0, 0, 255), 5)
        text = str(results[1]) + ', ' + str(possibility) + ', ' + str(round(results[2], 3)) + ', ' + str(results[3]) + 'degree'
        print('Pass!')
        cv2.putText(imgResult, text, [int(box[0][0]) - 5, int(box[0][1]) - 5], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)   # draw text

    # stack img, gutter, and resultImg
    imgStack = cv2.hconcat([imgScaled, gutter, imgResult])

    # put title to imgStack
    cv2.putText(imgStack, imgName, (6, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return imgStack

''' ------ end of helper function for getAccuracyOfTextDetection() ------ '''


''' ----- helper function for getAccuracyOfLettersImagesMapping() ----- '''
# choose num random images from images_list, return a list of the chosen images
def chooseRandomImages(images_list, num):
    randomImages_list = []
    idx_used = []
    for i in range(num):
        idx = random.randint(0, len(images_list) - 1)
        if idx in idx_used:
            idx = random.randint(0, len(images_list) - 1)
        image = images_list[idx]
        randomImages_list.append(image)
    return randomImages_list

# given a list, shuffle it in the list and return the shuffled list
def shuffleList(sth_list):
    permutations_list = list(itertools.permutations(sth_list))
    idx = random.randint(0, len(permutations_list) - 1)
    return permutations_list[idx]

''' ----- end of helper function for getAccuracyOfLettersImagesMapping() ----- '''


def getAccuracyOfTextDetection(folder_path, newWidth, step, letter, numIter):
    reader = easyocr.Reader(['en'])

    # set up list of target filenames and list of answers list
    imageNames_list = [i for i in os.listdir(folder_path) if (len(i) == 21 and i[-5] == letter)] # setting all targets to be A
    
    # pick randomimages
    randomImageNames = chooseRandomImages(imageNames_list, numIter)
    randomImageNames.sort()
    answers_list = [i[-5] for i in imageNames_list]

    # loop
    correct = 0
    cannotDetect = 0
    wrong = 0
    for i in range(numIter):
        print(i, '> Processing: ', randomImageNames[i])
        img_path = os.path.join(folder_path, randomImageNames[i])
        result_list = readImgPathDetectLetter(img_path, newWidth, step, reader)
        narrow_list = narrowResultList(result_list)
        result_list = [j[1] for j in result_list]
        print('result_list:', result_list)
        print('narrow_list:', narrow_list)
        if len(narrow_list) == 0:
            print('Cannot detect anything')
            cannotDetect += 1
        else:
            if answers_list[i] in narrow_list:
                print('correct!')
                correct += 1
            else:
                print('Wrong :(')
                wrong += 1
        print('-----------------------------------')

    # print resutls 
    print('##########  Result ########################')
    print('Correct: {}/{}'.format(correct, numIter))
    print('Wrong: {}/{}'.format(wrong, numIter))
    print('Cannot Detect: {}/{}'.format(cannotDetect, numIter))
    return correct, wrong, cannotDetect

    

# get accuracy of function mapping letters and images
def getAccuracyOfLettersImagesMapping(folder_path, newWidth, step, numIter):

    imageNames_list = [i for i in os.listdir(folder_path) if len(i) == 21]
    score_list = []   
    for i in range(numIter):
        print('#############################################')
        print('loop number', i)
        score = 0

        # choose 5 random images from list of images
        randomImageNames = chooseRandomImages(imageNames_list, 5)
        # get answers from "judge" 
        letters = [i[-5] for i in randomImageNames]
        letters = shuffleList(letters)

        print('Judge gives:', letters)
        print('Image taken from cams:', randomImageNames)

        # read every imageNames to possibilities and store image and its corresponding possibilites/None into a dictionary
        mapping_result = mapLettersToImages(letters, randomImageNames, folder_path, newWidth, step)

        for imageName, letter in mapping_result.items():
            if imageName[-5] == letter:
                score += 1
        print('Score:', score)
        score_list.append(score)
        print('#############################################')
    
    # get average, median of score_list:
    mean = statistics.mean(score_list)
    median = statistics.median(score_list)
    stdDeviation = statistics.stdev(score_list)
    print('Mean:', mean)
    print('Median:', median)
    print('Standard Deviation:', stdDeviation)


        
        
            
        

    