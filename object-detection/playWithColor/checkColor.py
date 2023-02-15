'''
    Enter an HSV color, show it visually
'''
import cv2
import numpy as np

red = [175, 200, 152]

reds = np.zeros((300, 300, 3), dtype = np.uint8)
height = len(reds)
width = len(reds[0])
for y in range(height):
    for x in range(width):
        reds[y][x][0] = red[0]
        reds[y][x][1] = red[1]
        reds[y][x][2] = red[2]

reds = cv2.cvtColor(reds, cv2.COLOR_HSV2BGR)
cv2.imshow('red', reds)
cv2.waitKey(0)
