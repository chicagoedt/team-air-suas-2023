import easyocr
import cv2
import time
import y_TextDetectionHelper as textDetect

# check if target contains letter
def checkTargetHaveLetter(rotations_list, reader):
    targetHaveLetter = False
    # pass all rotated versions to model and get results
    for rotation in rotations_list: 
        output = reader.readtext(rotation[0])
        # print(rotation[1]) # for TESTING # angle
        # print(output) # for TESTING # detected text
        # cv2.imshow('rotation', rotation[0]) # TESTING
        # cv2.waitKey(0)
        if len(output) != 0:
            targetHaveLetter = True
            break           
    return targetHaveLetter

# read img check if target has letter
def readImgCheckTargetHaveLetter(img, reader, step):

    # get a list of rotations
    rotations_list = textDetect.listRotations(img, step)

    # check if target has text
    targetHaveLetter = checkTargetHaveLetter(rotations_list, reader)
    return targetHaveLetter

# read img check if target has letter
# with preprocess img
def deepReadImgCheckTargetHaveLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step):
    print('>> Begin deepReadImgCheckTargetHaveLetter:')
    startTime = time.time()

    # get scaledWidth and cropSize b4 passing to imgPreprocessing()
    scaledWidth, cropSize = textDetect.getScaleAndCrop(img, stdSize, stdScaledWidth, stdCropSize)

    # preprocess img
    preprocessed = textDetect.imgPreprocessing(img, scaledWidth, cropSize)

    # check letter
    TargetHaveLetter = readImgCheckTargetHaveLetter(preprocessed, reader, step)
    print('Target has letter:', TargetHaveLetter)
    
    print('Time:', time.time() - startTime)
    print('>> Finish deepReadImgCheckTargetHaveLetter!')

    # # show original img and preprocessed img
    # cv2.imshow('original', img)               # for TESTING
    # cv2.imshow('preprocessed', preprocessed)  # for TESTING
    # cv2.waitKey(0)                            # for TESTING
    return TargetHaveLetter