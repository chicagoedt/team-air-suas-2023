'''
    given target image, determine shape color and letter color
'''
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

# get shape color and letter color from freqDict (assuming shapeColor != letterColor)
# the basic idea is that shapeColor has highest frequency and letterColor has second highest frequency
# there are some special case where trash (undefined) color dominates the known color (known color are defined in colorDict in y_color.py)
def getShapeAndLetterColor(freqDict):
    bestFreq = 0
    shapeColor = None  # highest freq color
    secondFreq = 0
    letterColor = None # second highest freq color

    # get shapeColor
    for color, freq in freqDict.items():
        if bestFreq < freq:
            shapeColor = color
            bestFreq = freq
    
    # special case for shapeColor
    if shapeColor == None: 
        if freqDict[shapeColor] >= 500: 
            shapeColor = 'Gray'
        else:
            del freqDict[shapeColor]
            bestFreq = 0
            shapeColor = None  # highest freq color
            for color, freq in freqDict.items():
                if bestFreq < freq:
                    shapeColor = color
                    bestFreq = freq

    # get letterColor
    for color, freq in freqDict.items():
        if secondFreq < freq and freq < bestFreq:
            letterColor = color
            secondFreq = freq

    # special case for letterColor
    if letterColor == None:
        if len(freqDict) >= 3: # special case when trash color accidentally dominate known color
            del freqDict[letterColor]
            del freqDict[shapeColor]
            thirdFreq = 0
            thirdColor = 0
            for color, freq in freqDict.items():
                if thirdFreq < freq:
                    thirdColor = color
                    thirdFreq = freq
            if thirdFreq >= 40:
                letterColor = thirdColor
    if letterColor == None:
        letterColor = 'Gray'

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
    cropped = cropImage(img, 40, 40)
    imgHSV = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

    # get shape and letter color
    shapeColor, letterColor = readImgHSVGetShapeAndLetterColor(imgHSV)
   
    # show outputs for TESTING
    original = scaleImg(img, 500)
    print('shape:', shapeColor)
    print('letter:', letterColor)
    cv2.imshow('original:', original)
    cv2.imshow('cropped:', cropped)
    print('press any key to continue ;)') 
    cv2.waitKey(0)
    return shapeColor, letterColor



