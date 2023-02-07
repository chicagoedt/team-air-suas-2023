import cv2
from text_recognition import *
import time

folder_path = '/Users/mightymanh/Desktop/myCode/myPy/pytorch stuff/team-air-suas-2023-fix-target/simulate-images/snapshots/target/'
img_name = input('Enter image file name: ')
img_path = folder_path + img_name

img = cv2.imread(img_path)
print(img.shape)

# preprocessing image
imgScale = scaleImg(img, 1000)
print(imgScale.shape)
# blur and gray scale the frame
blurValue = 1
imgBlur = cv2.GaussianBlur(imgScale, (7,7), blurValue)
imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

# get result
results = readImgDetectLetter(imgGray, 20)

cv2.imshow('Gray', imgGray)
cv2.imshow('Scale', imgScale)
cv2.setWindowProperty('Scale', cv2.WND_PROP_TOPMOST, 1)
cv2.setWindowProperty('Gray', cv2.WND_PROP_TOPMOST, 1)
cv2.waitKey(0)
    

