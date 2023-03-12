'''
    read selected images and detect letters
'''

import os
import cv2
import easyocr
from y_TextDetection import *           # text detection
import y_adaptToRealLife as adapt       # get cropSize and scaledWidth
import y_imgPreprocessing as prepr      # img preprocessing


# init images
reader = easyocr.Reader(['en'])
folder_path = '/Users/mightymanh/Desktop/real-images/drive-download-20230304T223241Z-001'
imgName_list = ['p9.jpg']

for imgName in imgName_list:
    print(imgName)
    img_path = os.path.join(folder_path, imgName)
    img = cv2.imread(img_path)

    # detect letter
    scaledWidth, cropSize = adapt.getScaleAndCrop(img_path, 130, 130, 50)
    result_list = readImgDetectLetter2(img, reader, scaledWidth, 20, cropSize, cropSize) 
    narrow_list = narrowResultList(result_list)
    result_list = [i[1] for i in result_list] # simplify result_list for nicer print

    # show results
    print('What easyocr gets:', result_list)
    print('What we deduce from results get by easyocr:', narrow_list)
    print('----------------------------')
    cv2.imshow('original', img)
    cv2.imshow('processed', prepr.imgPreprocessing(img, scaledWidth, cropSize, cropSize))  # for TESTING
    cv2.waitKey(0) # for TESTING