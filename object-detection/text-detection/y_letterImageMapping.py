from y_TextDetection import *  # text detection
import os                      # listdir, pathjoin 
import itertools               # permutation

''' ------------- helper functions for mapLettersToImages() -------------- '''
def calScore(letters, possibilities_list):
    score = 0
    numImages = len(possibilities_list)
    for i in range(numImages):
        if possibilities_list[i] != None:
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
        results = readImgPathDetectLetter(image_path, newWidth, step, reader)
        if len(results) == 2: # if it does not detect anything
            possibility = None
            if DEBUG:
                print('Possibility:', possibility)
        else:
            possibility = resultsToPossibility(results)
            if DEBUG: 
                print('result:', results[1])
                print('Possibility:', possibility)
        possibilities_list.append(possibility)
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