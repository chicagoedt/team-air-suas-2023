import cv2
import ShapeDetector

# Cv2 setup reading image
img = cv2.imread("linear_real.jpg")
contourImg, coords, pointCount = ShapeDetector.findShape(img)


print("done")
print("\nThe coordinate location for the shape is {} and it has {} points.... final answer".format(coords, pointCount))
cv2.imshow("contours", contourImg)
cv2.imsave("poggers.jpg",contourImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
