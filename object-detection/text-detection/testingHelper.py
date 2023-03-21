import cv2
import os                             # listdir, path.join
import itertools                      # permutation
import random                         # shuffleList
import statistics                     # mean, median, stdDev

import y_TextDetectionHelper as textDetect  # textDetection

# ignore this guy for now


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

# read random target imgs that have letter = input letter, text detect it and compared the actual result with expected result
def getAccuracyOfTextDetection(folder_path, fileName_list, letter_list, reader, letter, stdSize, stdScaledWidth, stdCropSize, numIter):

    # set up list of target filenames and list of answers list
    imageNames_list = [fileName_list[i] for i in range(len(letter_list)) if letter_list[i] == letter] # setting all targets to be A
    
    # pick randomimages
    randomImageNames = chooseRandomImages(imageNames_list, numIter)

    # loop
    correct = 0
    cannotDetect = 0
    wrong = 0
    wrong_list = []
    for i in range(numIter):

        # init image
        imgName = randomImageNames[i] + '.jpg'
        print(i, '> Processing: ', imgName)
        img_path = os.path.join(folder_path, imgName)
        img = cv2.imread(img_path)

        # text detect it, get results and narrow results
        scaledWidth, cropSize = adapt.getScaleAndCrop(img_path, stdSize, stdScaledWidth, stdCropSize)
        result_list = textDetect.readImgDetectLetterWithPreprocessed(img, reader, scaledWidth, 20, cropSize, cropSize)
        narrow_list = textDetect.narrowResultList(result_list)
        result_list = [j[1] for j in result_list]
        print('result_list:', result_list)
        print('narrow_list:', narrow_list)

        # check accuracy
        if len(narrow_list) == 0:
            print('Cannot detect anything')
            cannotDetect += 1
        else:
            if letter in narrow_list:
                print('correct!')
                correct += 1
            else:
                print('Wrong :(')
                wrong_list.append((imgName, result_list, narrow_list))
                wrong += 1
        print('-----------------------------------')

    # write to text file
    with open('wrong.txt', '+a') as f:
        for item in wrong_list:
            f.write('Letter: {}\n'.format(letter))
            f.write(str(item))
            f.write('\n----------------------------------------------\n')

    # print resutls 
    print('##########  Result ########################')
    print('Correct: {}/{}'.format(correct, numIter))
    print('Wrong: {}/{}'.format(wrong, numIter))
    print('Cannot Detect: {}/{}'.format(cannotDetect, numIter))
    return correct, wrong, cannotDetect

    

# ignore this guy for now
# get accuracy of function mapping letters and images
# def getAccuracyOfLettersImagesMapping(folder_path, newWidth, step, numIter):

#     imageNames_list = [i for i in os.listdir(folder_path) if len(i) == 21]
#     score_list = []   
#     for i in range(numIter):
#         print('#############################################')
#         print('loop number', i)
#         score = 0

#         # choose 5 random images from list of images
#         randomImageNames = chooseRandomImages(imageNames_list, 5)
#         # get answers from "judge" 
#         letters = [i[-5] for i in randomImageNames]
#         letters = shuffleList(letters)

#         print('Judge gives:', letters)
#         print('Image taken from cams:', randomImageNames)

#         # read every imageNames to possibilities and store image and its corresponding possibilites/None into a dictionary
#         mapping_result = mapLettersToImages(letters, randomImageNames, folder_path, newWidth, step)

#         for imageName, letter in mapping_result.items():
#             if imageName[-5] == letter:
#                 score += 1
#         print('Score:', score)
#         score_list.append(score)
#         print('#############################################')
    
#     # get average, median of score_list:
#     mean = statistics.mean(score_list)
#     median = statistics.median(score_list)
#     stdDeviation = statistics.stdev(score_list)
#     print('Mean:', mean)
#     print('Median:', median)
#     print('Standard Deviation:', stdDeviation)
    