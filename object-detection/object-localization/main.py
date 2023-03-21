import cv2
import ShapeDetector


imageList = ShapeDetector.getImageNames('C:/Users/Christian/Documents/School/EDT/team-air-suas-2023/object-detection/cropped images')

ShapeDetector.findShape(imageList[1])

