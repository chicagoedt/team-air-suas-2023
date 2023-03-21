import os
import cv2
import numpy as np

# tools_imgPreprocessing
import sys
sys.path.append("..")
import computerVisionTools.tool_imgPreprocessing as prepr

DEBUG = True  # todo: turn this off for production


def optionTwo():
    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread(args["image"])
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]


# Most likely used for testing only
# input: directory where cropped images are stored
# output: list of filenames for the shapedetector to work
def getImageNames(directory):
    # iterate over files in
    # that directory
    files = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            files.append(f)
    return files


# input: cv2 generated image using imshow (numpy array)
# output: center coordinates of shape
def findShape(img):
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel_size = 9
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    contrast = prepr.apply_brightness_contrast(blur_gray, 73, 95)
    low_threshold = 90
    high_threshold = 255
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 5  # minimum number of pixels making up a line
    max_line_gap = 10  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    # Draw the lines on the  image
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    print("Found: ", len(lines), "Lines")
    cv2.imwrite("edges.jpeg", lines_edges)
    cv2.imshow('lines', lines_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
