import cv2
import numpy as np
import os

def nothing(x):
    pass

# create trackbars
cv2.namedWindow('Parameters')
cv2.createTrackbar('Threshold1', 'Parameters', 17, 255, nothing)
cv2.createTrackbar('Threshold2', 'Parameters', 27, 255, nothing)

# initialize img
folderPath = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName = 'img_010_tar_149.jpg'
imgPath = os.path.join(folderPath, imgName)
img = cv2.imread(imgPath)

while True:

    # blur and gray scale the frame
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # track sharp edges from the frameGray
    threshold1 = cv2.getTrackbarPos('Threshold1', 'Parameters')
    threshold2 = cv2.getTrackbarPos('Threshold2', 'Parameters')
    print('threshold1: {},   threshold2: {}'.format(threshold1, threshold2))
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2) 

    # dilate imgs
    kernel = np.ones((7, 7))
    results = cv2.dilate(imgCanny, kernel, iterations = 1)

    
    

    cv2.imshow('Results', results)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
