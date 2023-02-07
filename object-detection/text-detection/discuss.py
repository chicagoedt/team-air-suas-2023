# Import some dependecies
from text_recognition import *
import os

# some helper functions

# test accuracy of the model by iterating all files in the folder
def getAccuracyOfTextDetection(folder_path, newWidth, step):

    # set up list of target filenames and list of answers list
    targets_list = [i for i in os.listdir(folder_path) if (len(i) == 21 and not os.path.isdir(i))]
    targets_list.sort()
    answers_list = [i[-5] for i in targets_list]

    num_targets = len(targets_list)
    incorrectTargets = []
    correct = 0
    newWidth = 500
    step = 20
    
    # for each target in targets_list
    for i in range(num_targets):
        target_path = os.path.join(folder_path, targets_list[i])

        # pass target to text detection model, follow step by step: read, img preprocessing, pass it to model to get output, and compare two results
        results = readImgPathDetectLetter(target_path, newWidth, step)
        if len(results) == 0:
            incorrectTargets.append(targets_list[i])
            continue
        else:
            if answers_list[i] == results[1]:
                correct += 1
            # special case
            else:
                incorrectTargets.append(targets_list[i])
                continue



    pass



# folder path that contains file 
folder_path = ''
newWidth = 500
step = 20
