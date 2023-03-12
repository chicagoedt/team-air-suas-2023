import numpy as np
import cv2
import os
import y_adaptToRealLife as adapt

folderPath = '/Users/mightymanh/Desktop/Testing'
imgName_list = [i for i in os.listdir(folderPath) if len(i) >= 7 and i[-4:] == '.jpg']

for imgName in imgName_list:
    print(imgName)
    imgPath = os.path.join(folderPath, imgName)
    img = cv2.imread(imgPath)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(imgGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:

        # datas
        M = cv2.moments(contour)
        if M['m00'] < 500:
            continue
        else:
            print('Area:', M['m00'])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print('Centroid:', (cx, cy))
    

        # bounding box
        rect = cv2.minAreaRect(contour)
        width, height = rect[1]
        print('Width: {}, Height: {}'.format(width, height))

        if 50 <= width and width <= 120 and 50 <= height and height <= 120:
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            img = cv2.drawContours(img,[box],0,(0,255,255),2)

        print('-----------------------------------------')

    print('#################################################')
    cv2.imshow('img', img)
    cv2.waitKey(0)
