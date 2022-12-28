from PIL import Image, ImageDraw
import random
import cv2
import numpy as np
from shapely.geometry import Polygon, MultiPoint, Point
import os


seed = [random.randint(0,359), random.randint(1,5)]

tar_files = os.listdir("target_images")

tar_path = random.choice(tar_files)

tar_img = Image.open("target_images/"+tar_path)

mask_img = Image.open("master_mask.bmp")

bgd_img = Image.open("master_background.png")

rot_img = tar_img.rotate(seed[0],expand=True, fillcolor=(0,0,0,0))
angle = seed[0]

arr = np.asarray(rot_img)
print(arr.shape)

# Find the non-zero elements of the array (i.e., the pixels of the image)
y, x,_ = np.nonzero(arr)

print(y.shape)

# Stack the x and y coordinates into a single array
points = np.column_stack((x, y))

# Calculate the minimum rotated bounding box around the points
# rect = cv2.minAreaRect()

# Convert the image to grayscale and detect the edges
# gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray, 50, 150)
#
# # Find the contours of the image
# contours= (cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))[1]

# Calculate the minimum rotated bounding box around the contours
# rect = cv2.minAreaRect(arr)
# points = np.asarray(rotated_image).nonzero()
# points = MultiPoint(points[::-1].T)
# rectangle = points.minimum_bounding_rectangle(points)
# bbox = rectangle.bounds

print(rect)

# img_draw = ImageDraw.Draw(rot_img)
# print(final_corners[1])
# img_draw.rectangle()

rot_img.show()

bgd_img.paste(rot_img, )

# bgd_img.show()
