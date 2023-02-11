# Import some dependecies
from text_recognition import *
import os
import numpy as np
from PIL import Image

# some helper functions

# stack orignal and result image (these imgs are from cv2)
def stackHorizontal(img_name, imgScaled, results):
    # build gutter
    height = imgScaled.shape[0]
    gutter = np.full((height, 3, 3), 255, dtype = np.uint8)

    # build imgResult
    imgResult = cv2.cvtColor(results[-1], cv2.COLOR_GRAY2BGR)
    if len(results) == 5:
        box = results[0] 
        cv2.rectangle(imgResult, [int(box[0][0]), int(box[0][1])], [int(box[2][0]), int(box[2][1])], (0, 0, 255), 5)
        text = results[1] + ", " + str(round(results[2], 3)) + ", " + str(results[3]) + "degree"
        print('Pass!')
        cv2.putText(imgResult, text, [int(box[0][0]), int(box[0][1]) - 5], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)   # draw text

    # stack img, gutter, and resultImg
    imgStack = cv2.hconcat([imgScaled, gutter, imgResult])

    # put title 
    cv2.putText(imgStack, img_name, (6, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return imgStack


# test accuracy of the model by iterating all files in the folder
# get the pdf file containing comparison
def getAccuracyOfTextDetection(folder_path, newWidth, step):

    # set up list of target filenames and list of answers list
    targets_list = [i for i in os.listdir(folder_path) if (len(i) == 21 and (not os.path.isdir(i)))]
    targets_list.sort()
    answers_list = [i[-5] for i in targets_list]

    imgPil_list = [] # lists that contains images that will be loaded to pdf
    num_targets = len(targets_list)
    incorrectTargets = []
    correct = 0
    
    # for each target in targets_list
    for i in range(num_targets):
        print(i, '> Processing: ', targets_list[i])
        target_path = os.path.join(folder_path, targets_list[i])

        # pass target to text detection model, follow step by step: read, img preprocessing, pass it to model to get output, and compare two results
        results = readImgPathDetectLetter(target_path, newWidth, step)
        if len(results) == 2:
            print('Cannot detect anything')
            incorrectTargets.append(targets_list[i])
        else:
            if answers_list[i] == results[1]:
                print('Correct!')
                correct += 1
            # special case
            else:
                print('Wrong :(')
                incorrectTargets.append(targets_list[i])
    
        
        # build scaled img
        img = cv2.imread(target_path)
        imgScaled = scaleImg(img, 500)

        # get imgStack and convert it to PIL image
        imgStack = stackHorizontal(targets_list[i], imgScaled, results)
        imgStackPil = Image.fromarray(imgStack)
        imgPil_list.append(imgStackPil)

        print('-----------------------------------')


    # load pil images to pdf
    print('Loading pdf file: ....')
    imgPil_list[0].save('experiment.pdf', save_all = True, append_images = imgPil_list[1:])

    # print resutls 
    accuracy = round(correct / num_targets, 3)
    print('Accuracy:', accuracy)
    print('Num files incorrect:', len(incorrectTargets))

    return accuracy



# # folder path that contains file 
# folder_path = ''
# newWidth = 500
# step = 20
