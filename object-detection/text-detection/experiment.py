import cv2
import numpy as np
from text_recognition import *

# for optimizing code, ignore it

def nothing(x):
    pass

cv2.namedWindow('Parameters')
cv2.createTrackbar('BlurValue', 'Parameters', 2, 255, nothing)
cv2.createTrackbar('Threshold1', 'Parameters', 155, 255, nothing)
cv2.createTrackbar('Threshold2', 'Parameters', 100, 255, nothing)

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    
    # if input for imgArray is ([img1, img2, img3], [], ...)
    if rowsAvailable:
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        for x in range(0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (width, height), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: 
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)

    # if input for imgArray is [img1, img2, img3]
    else:
        for x in range(0, rows):
            # scale all imgs to dimension of imgArray[0].shape
            width = imgArray[0].shape[1]
            height = imgArray[0].shape[0]
            imgArray[x] = cv2.resize(imgArray[x], (width, height), None, scale, scale)

            if len(imgArray[x].shape) == 2: # this is for 2D img like the gray_scaled one
                #print(imgArray[x])
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR) # convert from 2D to 3D so that all images have len(shape) = 3
        hor = np.hstack(imgArray)
        ver = hor
    return ver

# main
if __name__ == '__main__':
    folder_path = '/Users/mightymanh/Desktop/myCode/myPy/pytorch stuff/team-air-suas-2023-fix-target/simulate-images/snapshots/target/'
    img_path = folder_path + 'img_000_tar_039_M.jpg'
    img = cv2.imread(img_path)
    img = scaleImg(img, 150)

    while True:

        # blur and gray scale the frame
        blurValue = cv2.getTrackbarPos('BlurValue', 'Parameters')
        imgBlur = cv2.GaussianBlur(img, (7,7), blurValue)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

        # track sharp edges from the frameGray
        threshold1 = cv2.getTrackbarPos('Threshold1', 'Parameters')
        threshold2 = cv2.getTrackbarPos('Threshold2', 'Parameters')
        imgCanny = cv2.Canny(imgGray, threshold1, threshold2) 

        # dilate imgs
        kernel = np.ones((7, 7))
        imgDil = cv2.dilate(imgCanny, kernel, iterations = 1)

        # thinning imgs
        kernelThinning = np.ones((5,5),np.uint8)
        imgErosion = cv2.erode(imgDil, kernelThinning, iterations = 1)

        # output
        imgStack = stackImages(1, ([img, imgBlur, imgGray], [imgCanny, imgDil, imgErosion]))

        cv2.imshow('Results', imgStack)
        cv2.setWindowProperty('Results', cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowProperty('Parameters', cv2.WND_PROP_TOPMOST, 1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
