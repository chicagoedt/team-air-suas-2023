import y_adaptToRealLife as adapt
import y_TextDetection as textDetect
import y_imgPreprocessing as prepr
import cv2

def checkImgHavingLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step):
    # get scaledWidth and cropSize
    scaledWidth, cropSize = adapt.getScaleAndCrop(img, stdSize, stdScaledWidth, stdCropSize)

    # check letter
    TargetHaveLetter = textDetect.readImgCheckTargetHaveLetterWithPreprocessed(img, reader, scaledWidth, step, cropSize, cropSize)
    print('status:', TargetHaveLetter)
    
    # # show original img and preprocessed img
    # cv2.imshow('original', img)
    # cv2.imshow('preprocessed', prepr.imgPreprocessing(img, scaledWidth, cropSize, cropSize))  # for TESTING
    # cv2.waitKey(0)
    return TargetHaveLetter

def deepReadImgReadLetter(img, reader, stdSize, stdScaledWidth, stdCropSize, step):
    # get scaledWidth and cropSize
    scaledWidth, cropSize = adapt.getScaleAndCrop(img, stdSize, stdScaledWidth, stdCropSize)
    
    # detect letter
    result_list = textDetect.readImgDetectLetterWithPreprocessed(img, reader, scaledWidth, step, cropSize, cropSize) 
    narrow_list = textDetect.narrowResultList(result_list)
    result_list = [i[1] for i in result_list] # simplify result_list for nicer print

    # show results
    print('What easyocr gets:', result_list)
    print('What we deduce from results get by easyocr:', narrow_list)

    # # show original img and preprocessed img
    cv2.imshow('original', img)
    cv2.imshow('preprocessed', prepr.imgPreprocessing(img, scaledWidth, cropSize, cropSize))  # for TESTING
    cv2.waitKey(0)
