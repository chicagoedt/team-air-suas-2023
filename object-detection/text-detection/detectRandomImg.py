'''
    read random images and detect letters
'''

from y_TextDetection import * 
from testingHelper import chooseRandomImages
import os

reader = easyocr.Reader(['en'])
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/target-practice/simulate-images/snapshots/target_practice'
imgName_list = [i for i in os.listdir(folder_path) if len(i) == 19]
imgName_list = chooseRandomImages(imgName_list, 30)

for imgName in imgName_list:
    print(imgName)
    img_path = os.path.join(folder_path, imgName)
    result_list = readImgPathDetectLetter(img_path, reader, 120, 20, 50, 50) 
    narrow_list = narrowResultList(result_list)
    result_list = [i[1] for i in result_list] # simplify result_list for nicer print

    # show results
    print('What easyocr gets:', result_list)
    print('What we deduce from results get by easyocr:', narrow_list)
    print('----------------------------')
    cv2.imshow('processed', prepr.imgPreprocessing(cv2.imread(img_path), 120, 50, 50))  # for TESTING
    cv2.waitKey(0) # for TESTING