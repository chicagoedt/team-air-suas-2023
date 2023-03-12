import PIL.ImageOps
import cv2
from PIL import ImageOps,Image
import numpy as np
from matplotlib import pyplot as plt

DEBUG = True  # todo: turn this off for production


def increaseContrast(original):
    # We first blur the image to get rid of the cracks on the asphalt
    blur = cv2.GaussianBlur(original, (9, 9), 10)
    if DEBUG:
        cv2.imshow("Gaussian blur image", blur)
        cv2.waitKey(0)
    # converting to LAB color space
    lab = cv2.cvtColor(blur, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Stacking the original image with the enhanced image
    result = np.hstack((blur, enhanced_img))
    if DEBUG:
        cv2.imshow('Result', result)
        cv2.waitKey(0)

    return blur

# initial image processing for contour prep (black and white image with thresholding applied)
def contourPrep(original):
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    ret, threshImg = cv2.threshold(gray, 180, 255, cv2.THRESH_TOZERO)
    cv2.imshow("Threshold",threshImg)
    cv2.waitKey(0)
    print("We reached the breakpoint")


# input: cv2 generated image using imshow (numpy array)
# output: center coordinates of shape
def findShape(img):
    ## Manhs stuff idk wtf this does
    # img = Image.fromarray(img)
    # img_posterize = PIL.ImageOps.posterize(img,1)
    # img_posterize.show()
    # img = np.array(img_posterize)

    blurred = increaseContrast(img)
    contourPrep(blurred)


    # Get contours
    contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # first 2 values are x and y coordinates and last is the contour count (number of points)
    shapeInfo = []

    # opencv detects many contours within the image
    # including the image shape itself (which is index 0 and should be ignored)
    contourCount = 0

    if DEBUG:
        print("Found contours: ", len(contours)) # commented by MANH
    for contour in contours:
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5) # commented by MANH to unable drawing contours
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
            shapeInfo.append((x, y, len(approx)))
            # if DEBUG:
            #     print("Contour #: ", contourCount, "Number of points: ", len(approx), "Location: ({},{})".format(x, y)) # commented by MANH
        contourCount += 1

    # Getting the points count that appears the most in the shapeInfo list
    _, _, contourModeCount = max(set(shapeInfo), key=shapeInfo.count)
    if DEBUG:
        print(shapeInfo)
        print("The most occurring shape in this image has {} points".format(contourModeCount)) # commented by MANH
    # todo: handle edge case where there is no mode found
    # Getting the average coordinates for the shape with found contourModeCount value
    xSum = 0
    ySum = 0
    i = 0
    for shape in shapeInfo:
        if shape[2] == contourModeCount:
            # if DEBUG: print("Iterating thru: ", shape) # commented by MANH
            xSum = xSum + shape[0]
            ySum = ySum + shape[1]
            i += 1
    avgCoords = (int(xSum / i), int(ySum / i))
    cv2.circle(img, avgCoords, radius=1, color= (255,0,0), thickness=1)
    if DEBUG: print("Average coordinate location: ", avgCoords)
    print('exit ShapeDetector')
    return img, avgCoords, contourModeCount
