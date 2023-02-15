'''
    click anywhere in image to get coordinates and hsv value of a clicked pixel
'''
import cv2
import os
import numpy as np

# mouse event
def click_event(event, x, y, flags, params):
  
    # if left click mouse on a pixel in the displayed image, you get coordinate of pixel, bgr values as well as hsv values
    if event == cv2.EVENT_LBUTTONDOWN:
  
        # displaying the coordinates
        # on the Shell
        bgr = np.uint8([[img[y][x]]])
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    
        print('{}, {}: bgr: {}, hsv: {}'.format(x, y, bgr[0][0], hsv[0][0]))
        cv2.imshow('image', img)

# path to image
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/pytorch stuff/team-air-suas-2023-fix-target/simulate-images/snapshots/target/'
filename = 'img_000_tar_037_P.jpg'
filePath = os.path.join(folder_path, filename)

# read img and scale it to big enough size
img = cv2.imread(filePath)
img = cv2.resize(img, (300, 300))
cv2.imshow('image', img)

# setting mouse handler for the image
# and calling the click_event() function
cv2.setMouseCallback('image', click_event)
  
# wait for a key to be pressed to exit
cv2.waitKey(0)
  
# close the window
cv2.destroyAllWindows()