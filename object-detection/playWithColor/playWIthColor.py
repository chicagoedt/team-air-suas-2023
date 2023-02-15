'''
    extract red from image
'''
# Task: find the range for red
import os
import cv2
import numpy as np

folder_path = '/Users/mightymanh/Desktop/myCode/myPy/pytorch stuff/team-air-suas-2023-fix-target/simulate-images/snapshots/target/'
filename = 'img_000_tar_028_I.jpg'

# path to image
file_path = os.path.join(folder_path, filename)
img = cv2.imread(file_path)

# scale target so it's big enough
imgScaled = cv2.resize(img, (300, 300))
imgScaled = cv2.cvtColor(imgScaled, cv2.COLOR_BGR2HSV)

# hsv bounds for red
lower1 = np.array([0, 187, 152])
upper1 = np.array([5, 255, 255])
lower2 = np.array([157, 187, 152])
upper2 = np.array([179, 255, 255])

# extract red from imgScaled
mask = cv2.inRange(imgScaled, lower1, upper1)
mask2 = cv2.inRange(imgScaled, lower2, upper2)
result = cv2.bitwise_or(mask, mask2)

# show photos 
cv2.imshow('Scaled', imgScaled)
cv2.imshow('mask', mask)
cv2.imshow('mask2', mask2)
cv2.imshow('result', result)
cv2.setWindowProperty('Scaled', cv2.WND_PROP_TOPMOST, 1)
cv2.setWindowProperty('mask', cv2.WND_PROP_TOPMOST, 1)
cv2.setWindowProperty('mask2', cv2.WND_PROP_TOPMOST, 1)
cv2.setWindowProperty('result', cv2.WND_PROP_TOPMOST, 1)
cv2.waitKey(0)

