from y_imgPreprocessing import *
from y_TextDetection import *
import random

def list2FreqDict(result_list):
    return_dict = {}
    for i in result_list:
        if i not in return_dict:
            return_dict[i] = 1
        else:
            return_dict[i] += 1
    return return_dict

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

reader = easyocr.Reader(['en'])
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'

numIter = 20
dictLetter = {}
letters = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'
# idxL = random.randint(0, len(letters) - 1)
# letters = letters[idxL]
for letter in letters:
    print('Letter:', letter)
    finalList = []
    imgName_list = [i for i in os.listdir(folder_path) if len(i) == 21 and i[-5] == letter]
    randomImage_list = chooseRandomImages(imgName_list, numIter)
    for i in range(numIter):
        img_name = randomImage_list[i]
        print('Reading image:', img_name)
        img_path = os.path.join(folder_path, img_name)
        result_list = readImgPathDetectLetter(img_path, 150, 20, reader)
        results = [j[1] for j in result_list]
        print('results', results)
        finalList.extend(results)
        print('------------------------------------------')
    # cv2.imshow('img', img)
    # cv2.imshow('processed', result[-1])
    # cv2.waitKey(0)

    freqDict = list2FreqDict(finalList)
    dictLetter[letter] = freqDict
    print('############################################################################')

for letter, freqDict in dictLetter.items():
    print('{}: \n\t {}'.format(letter, freqDict))


    


