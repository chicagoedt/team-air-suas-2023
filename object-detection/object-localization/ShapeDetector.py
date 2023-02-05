import cv2

DEBUG = True  # todo: turn this off for production


# messing around ignore this function
def getHSVHist(path):
    img = cv2.imread(path)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = img2[:, :, 0], img2[:, :, 1], img2[:, :, 2]
    hist_h = cv2.calcHist([h], [0], None, [256], [0, 256])
    hist_s = cv2.calcHist([s], [0], None, [256], [0, 256])
    hist_v = cv2.calcHist([v], [0], None, [256], [0, 256])
    return hist_h, hist_s, hist_v


# input: cv2 generated image using imshow (numpy array)
# output: center coordinates of shape
def findShape(img):
    # initial image processing for contour prep (black and white image with thresholding applied)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, threshImg = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Get contours
    contours, _ = cv2.findContours(threshImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # first 2 values are x and y coordinates and last is the contour count (number of points)
    shapeInfo = []

    # opencv detects many contours within the image
    # including the image shape itself (which is index 0 and should be ignored)
    contourCount = 0
    if DEBUG:
        print("Found contours: ", len(contours))
    for contour in contours:
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
            shapeInfo.append((x, y, len(approx)))
            if DEBUG:
                print("Contour #: ", contourCount, "Number of points: ", len(approx), "Location: ({},{})".format(x, y))
        contourCount += 1

    # Getting the points count that appears the most in the shapeInfo list
    _, _, contourModeCount = max(set(shapeInfo), key=shapeInfo.count)
    if DEBUG:
        print("The most occurring shape in this image has {} points".format(contourModeCount))

    # Getting the average coordinates for the shape with found contourModeCount value
    xSum = 0
    ySum = 0
    i = 0
    for shape in shapeInfo:
        if shape[2] == contourModeCount:
            if DEBUG: print("Iterating thru: ", shape)
            xSum = xSum + shape[0]
            ySum = ySum + shape[1]
            i += 1
    avgCoords = (int(xSum / i), int(ySum / i))
    cv2.circle(img, avgCoords, radius=1, color= (255,0,0), thickness=1)
    if DEBUG: print("Average coordinate location: ", avgCoords)
    return img, avgCoords, contourModeCount
