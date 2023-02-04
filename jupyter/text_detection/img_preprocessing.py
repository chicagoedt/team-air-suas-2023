import cv2
from text_recognition import *


folder_path = 'C:\Users\ChicagoEDT\github\team-air-suas-2023\jupyter\datas\'
img_path = 'img_025_tar_214_Z.jpg'

img = cv2.imread(img_path)
print(img.shape)


# preprocessing image
imgScale = scaleImg(img, 150)
imgGray = cv2.cvtColor(imgScale, cv2.COLOR_BGR2GRAY)


results = readImgDetectLetter(imgScale, 20)

cv2.imshow('Gray', imgGray)
cv2.waitKey(0)

