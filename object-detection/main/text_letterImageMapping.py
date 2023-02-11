from text_detection import *
import os
import itertools # for permutation

def calScore(letters, possibilities_list):
    score = 0
    numImages = len(possibilities_list)
    for i in range(numImages):
        if possibilities_list[i] != None:
            if letters[i] in possibilities_list[i]:
                score += 1
    return score

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


def mapLettersToImages(letters, images_folder):

    reader = easyocr.Reader(['en'])
    images = os.listdir(images_folder)

    # read every images to possibilities and store image and its corresponding possibilites/None into a dictionary
    possibilities_list = []
    print('Reading images...\n----------------------------')

    for image in images:
        print(image)
        image_path = os.path.join(images_folder, image)
        results = readImgPathDetectLetter(image_path, 400, 20, reader)
        if len(results) == 2:
            possibility = None
        else:
            possibility = resultsToPossibility(results)
        print('Possibility: ', possibility)
        possibilities_list.append(possibility)
        print('----------------------------')
    
    # map letters to images  
    print('Possibilites_list: ', possibilities_list)
    print('Mapping........')
    permutation_letters = list(itertools.permutations(letters))
    bestPermutation = maxScore(permutation_letters, possibilities_list)
    
    print('############## Result ###############')
    mapImage_letter = {}
    score = 0
    for i in range(len(images)):
        print(images[i], ': ', bestPermutation[i]) 
        mapImage_letter[images[i]] = bestPermutation[i]
    
    return mapImage_letter