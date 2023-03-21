from y_TextDetectionHelper import *  # text detection
from y_specialcase import *    # text detection
import os                      # listdir, pathjoin 
import itertools               # permutation

# ignore this for now, just messing around

''' ------------- helper functions for mapLettersToImages() -------------- '''
def calScore(letters, possibilities_list):
    score = 0
    numImages = len(possibilities_list)
    for i in range(numImages):
        if len(possibilities_list[i]) != 0:
            if letters[i] in possibilities_list[i]:
                score += 1
    return score

# find the permutation of letters that has the highest score
# return that permutation
def maxScore(permutation_letters, possibilities_list):
    bestPermutation = ()
    maxScore = 0
    for letters in permutation_letters:
        score = calScore(letters, possibilities_list)
        if score > maxScore:
            maxScore = score
            bestPermutation = letters
    print('Max score:', maxScore)
    return bestPermutation

''' ------------- end helpper functions for mapLettersToImages() -------------- '''

# map letters to imageNames
# return a dictionary with key imageName and its value is its mapped letter
def mapLettersToImages(letters, imageNames_list, root, newWidth, step):

    DEBUG = True
    reader = easyocr.Reader(['en'])

    # read every images to possibilities and store image and its corresponding possibilites/None into a dictionary
    possibilities_list = []
    
    if DEBUG: print('Reading images...\n----------------------------')

    for imageName in imageNames_list:
        print(imageName)
        image_path = os.path.join(root, imageName)
        result_list = readImgPathDetectLetter(image_path, newWidth, step, reader)
        narrow_list = narrowResultList(result_list)
        result_list = [i[1] for i in result_list]
        print('result_list:', result_list)
        print('narrow_list:', narrow_list)
        possibilities_list.append(narrow_list)
        if DEBUG: print('----------------------------')
    
    # map letters to images  
    if DEBUG: print('Possibilites_list: ', possibilities_list)
    print('Mapping........')
    permutation_letters = list(itertools.permutations(letters))
    bestPermutation = maxScore(permutation_letters, possibilities_list)
    
    print('### Result ###')
    mapImage_letter = {}
    score = 0
    for i in range(len(imageNames_list)):
        print(imageNames_list[i], ': ', bestPermutation[i]) 
        mapImage_letter[imageNames_list[i]] = bestPermutation[i]
    
    return mapImage_letter