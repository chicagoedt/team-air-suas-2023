import cv2 
import ShapeDetector 
import os 
import math
from matplotlib import pyplot as plt

import shutil

# get the expected coordinates 
def calculateExpectedCoord (img_path, yolo_path):
    # get x and y percentage values from yolo file
    file = open(yolo_path, 'r')
    line = file.read() 
    line_list = line.split()
    x_percentage = float(line_list[1])
    y_percentage = float(line_list[2])
    file.close()

    # calculate the x and y based on image dimension
    img = cv2.imread(img_path)
    x = int(img.shape[1] * x_percentage)
    y = int(img.shape[0] * y_percentage)
    return x, y

# check if the foundCoord is good enough (meaning foundCoord is in range maxDistance of expectedCoord)
# maxDistance is the distance that defines the valid range between foundCoord and expectedCoord
def isCoordCorrect( expectedCoord, foundCoord, maxDistance):
    distance = math.sqrt((foundCoord[0] - expectedCoord[0]) ** 2 + (foundCoord[1] - expectedCoord[1]) ** 2)
    print('Distance:', distance)
    if distance <= maxDistance:
        return True
    return False

# check the consistency of jpgs and yolos, assuming they are sorted
def isConsistentJpgsAndYolos(jpgs_list, yolos_list):
    if len(jpgs_list) != len(yolos_list): # if two lists do not have same size then they are not consistent
        print('Inconsistent size: jpgs_list', len(jpgs_list), 'vs yolos_list', len(yolos_list))
        return False
    
    for i in range(len(jpgs_list)):
        if jpgs_list[i][:15] != yolos_list[i][:15]: # if two files do not correspond to each other 
            # show where it gets inconsistent
            print('Inconsistent at index', i, '; jpgs:', jpgs_list[i], 'vs', 'yolos:', yolos_list[i])
            return False
    return True


# check accuracy of the localization
# maxDistance is the distance that defines the valid range between foundCoord and expectedCoord
def checkAccuracyOfLocalization(folder_path, maxDistance):
    # get lists of file
    jpgs_list = [i for i in os.listdir(folder_path) if (not os.path.isdir(i)) and len(i) == 19]
    yolos_list = [i for i in os.listdir(folder_path) if (not os.path.isdir(i)) and len(i) == 20]
    jpgs_list.sort()
    yolos_list.sort()

    # check if jpgs and yolos in folder_path are consistent
    if not isConsistentJpgsAndYolos(jpgs_list, yolos_list):
        print('Jpgs files and yolo files are not consistent. Maybe something is wrong with folder format')
        return None
        
    correct = 0
    totalImages = len(jpgs_list)
    errorFiles = [] # image files that ShapeDetector.py fails to process. Useful for optimizing code
    incorrect = [] # image files which ShapeDetector.py fails (isCoordCorrect() == False). Maybe useful for optimizing code

    # for every 2 files (image and yolo) check accuracy
    for i in range(0, totalImages):
        img_path = os.path.join(folder_path, jpgs_list[i])
        yolo_path = os.path.join(folder_path, yolos_list[i])
        print('image:', jpgs_list[i], ', yolo:', yolos_list[i])

        # get expected Coord
        expectedCoord = calculateExpectedCoord(img_path, yolo_path)

        # get foundCoord
        try:
            img = cv2.imread(img_path)
            post_img, foundCoord, _ = ShapeDetector.findShape(img)
            print('Expected Coord:', expectedCoord)

            # compare two coords
            if isCoordCorrect(expectedCoord, foundCoord, maxDistance):
                correct += 1
            else:
                incorrect.append(jpgs_list[i])   # append both incorrect jpgs with its corresponding yolos
                incorrect.append(yolos_list[i])

        except:
            errorFiles.append(jpgs_list[i])   # append both incorrect jpgs with its corresponding yolos
            errorFiles.append(yolos_list[i])
            print('some ERROR with ShapeDetector.py') 
            print('-----------------------------------')
            continue
        print('-----------------------------------')
        plt.imshow(post_img)
        plt.show()
        cv2.waitKey(0)


    # cv2.imsave(img_path + ".png", post_img)
    # print(errorFiles)  # uncomment to show all files that ShapeDetector finds trouble to process
    # print(incorrect) # uncomment to show all files that ShapeDetector fails 
    print('Number of files failed:', int(len(incorrect) / 2))
    print('Number of errorFiles:', len(errorFiles))
    accuracy = round(correct / (totalImages), 3)
    return accuracy, errorFiles, incorrect

# ignore this, just messing around
# # got copy all files into a folder_path
# def copyFilesToNewFolder(files_list, srcfolder_path, dstfolder_path):
#     for i in range(len(files_list)):
#         img_path = os.path.join(srcfolder_path, files_list[i])
#         yolo_path = os.path.join(folder_path, files_list[i + 1])

#         # copy files to folder
        
    



#------------------------------------------
# MAIN
folder = '../../simulate-images/snapshots/target' # this will be folder that contains jpg files and yolo files
maxDistance = 40 # need to figure out what the best maxDistance is
accuracy, errorFiles, incorrect = checkAccuracyOfLocalization(folder, maxDistance) 
print('maxDistance:', maxDistance)
print('Accuracy: ', accuracy)

'''
    I comment some "if DEBUG" statements in ShapeDetector.py so terminal prints main infos.
    You can uncomment it

    NOTE: For easier iterating files in the folder, folder should just contain 
    only jpg and yolo files. Each jpg must have its corresponding yolo 
    <view image format.jpg for reference>
        
    NOTE: ShapeDetector.py fails to process some image files. Maybe there are some other special cases
    that ShapeDetector.py does not cover???

    Question: What is the best maxDistance? 
'''




