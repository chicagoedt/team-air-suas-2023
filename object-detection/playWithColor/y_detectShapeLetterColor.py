from y_imgPreprocessing import *
from y_colorFunc import *

# convert a list to a frequency dict
def list2FreqDict(color_list):
    freqDict = {}
    for i in range(len(color_list)):
        if color_list[i] not in freqDict:
            freqDict[color_list[i]] = 1
        else:
            freqDict[color_list[i]] += 1
    return freqDict

# get shape color and letter color from freqDict
def getShapeAndLetterColor(freqDict):
    bestFreq = 0
    shapeColor = None  # highest freq color
    secondFreq = 0
    letterColor = None # second highest freq color
    for color, freq in freqDict.items():
        if bestFreq < freq:
            shapeColor = color
            bestFreq = freq
    
    for color, freq in freqDict.items():
        if secondFreq < freq and freq < bestFreq:
            letterColor = color
            secondFreq = freq
    return shapeColor, letterColor

# read an imgHSV and get the shape color and letter color
def readImgHSVGetShapeAndLetterColor(imgHSV):
    color_list = []
    lenY = imgHSV.shape[0]
    lenX = imgHSV.shape[1]
    for x in range(lenX):
        for y in range(lenY):
            color = getColorOfPixel(imgHSV[y][x])
            color_list.append(color)
    freqDict = list2FreqDict(color_list)
    print(freqDict) # for TESTING

    shapeColor, letterColor = getShapeAndLetterColor(freqDict)
    return shapeColor, letterColor

# read image path and get shape and letter color (assuming image is a focus target)
def readImgPathGetShapeAndLetterColor(img_path):
    img = cv2.imread(img_path)

    # preprocessing img and convert img to HSV
    cropped = cropImage(img, 30, 30)
    imgHSV = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

    # get shape and letter color
    shapeColor, letterColor = readImgHSVGetShapeAndLetterColor(imgHSV)

    # # show
    # print('shape:', shapeColor)
    # print('letter:', letterColor)
    cv2.imshow('original:', img)
    cv2.imshow('cropped:', cropped)
    cv2.waitKey(0)
    return shapeColor, letterColor



