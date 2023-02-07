import cv2 
import ShapeDetector 
import os 
import math

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

# check accuracy of the localization
# maxDistance is the distance that defines the valid range between foundCoord and expectedCoord
def checkAccuracyOfLocalization(folder_path, maxDistance):
    # get lists of file
    files_list = os.listdir(folder_path)
    files_list.sort() # sort them in order so each jpg file is adjacent to its corresponding yolo file

    correct = 0
    totalImages = int(len(files_list) / 2)
    errorFiles = [] # image files that ShapeDetector.py fails to process. Useful for optimizing code
    incorrect = [] # image files which ShapeDetector.py fails (isCoordCorrect() == False). Maybe useful for optimizing code

    # for every 2 files (image and yolo) check accuracy
    for i in range(0, len(files_list), 2):
        img_path = os.path.join(folder_path, files_list[i])
        yolo_path = os.path.join(folder_path, files_list[i + 1])
        print('image:', files_list[i], ', yolo:', files_list[i+1])

        # get expected Coord
        try: 
            expectedCoord = calculateExpectedCoord(img_path, yolo_path)
        except:
            print('some ERROR with reading files???? Check if folder contains other files beside jpg and yolo')
            return None

        # get foundCoord
        try:
            img = cv2.imread(img_path)
            _, foundCoord, _ = ShapeDetector.findShape(img)
            print('Expected Coord:', expectedCoord)
            # compare two coords
            if isCoordCorrect(expectedCoord, foundCoord, maxDistance):
                correct += 1
            else:
                incorrect.append(files_list)    
        except:
            errorFiles.append(files_list[i])
            print('some ERROR with ShapeDetector.py') 
            print('-----------------------------------')
            continue
        print('-----------------------------------')

    # print(errorFiles)  # uncomment to show all files that ShapeDetector finds trouble to process
    # print(incorrect) # uncomment to show all files that ShapeDetector fails 
    print('Number of errorFiles:', len(errorFiles))
    accuracy = round(correct / (totalImages), 3)
    return accuracy

#------------------------------------------
# MAIN
folder = '/Users/mightymanh/Desktop/datas/' # this will be folder that contains jpg files and yolo files
maxDistance = 20 # need to figure out what the best maxDistance is
accuracy = checkAccuracyOfLocalization(folder, maxDistance) 
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




