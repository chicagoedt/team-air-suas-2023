import cv2
import ShapeDetector

#for testing, ignore
hist_h, hist_s, hist_v = ShapeDetector.getHSVHist("star.jpg")

# Cv2 setup reading image
img = cv2.imread("star.jpg")

contourImg, coords, pointCount = ShapeDetector.findShape(img)
print("\nThe coordinate location for the shape is {} and it has {} points.... final answer".format(coords, pointCount))
cv2.imshow("contours", contourImg)

cv2.waitKey(0)
cv2.destroyAllWindows()


