import random
import numpy as np
import cv2
import os

# Generate a random 26x34 image
background = cv2.imread("master_background.png", cv2.IMREAD_UNCHANGED)

# Generate a random larger background image
tar_files = os.listdir("target_images")

tar_path = random.choice(tar_files)

image = cv2.imread("target_images/"+tar_path, cv2.IMREAD_UNCHANGED)

# Define the four corners of the irregular quadrilateral region
quad_points = np.array([[3014, 2843], [3014+3806, 2843], [3014+3806, 2843+654], [3014, 2843+654]], dtype=np.int32)

# Generate a random rotation angle
angle = random.uniform(-180, 180)

# Rotate the image
rows, cols, _ = image.shape
M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
rotated_image = cv2.warpAffine(image, M, (cols, rows))

# Find the bounding box of the rotated image
cv2.imshow("pog", rotated_image)

# rect = cv2.minAreaRect(rotated_image)
# points = cv2.boxPoints(rect)
# x, y, w, h = cv2.boundingRect(points)

# Find a random position within the irregular quadrilateral region to paste the image
# found = False
# while not found:
#     x_offset = random.randint(0, quad_points[:,0].max() - w)
#     y_offset = random.randint(0, quad_points[:,1].max() - h)
#     if cv2.pointPolygonTest(quad_points, (x_offset+w/2, y_offset+h/2), False) > 0:
#         found = True

# Paste the rotated image onto the background
# result = background.copy()
# result[y_offset:y_offset+h, x_offset:x_offset+w] = rotated_image

# Print the four corners of the pasted image
# print((x_offset, y_offset))
# print((x_offset+w, y_offset))
# print((x_offset, y_offset+h))
# print((x_offset+w, y_offset+h))

# Display the result
# cv2.imshow("Result", result)
cv2.waitKey(0)
