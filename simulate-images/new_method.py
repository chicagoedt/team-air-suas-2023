from PIL import Image, ImageDraw, ImageOps
import math
import numpy as np
import random
from PIL import ImageTransform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import affinity
import matplotlib.pyplot as plt
import os

final_dir = "final_images/"
master_dir = "master_images/"
# def gen_pics(amount):
# for _ in range(amount):
# # print("Which image it is on rn:", _)

tar_files = os.listdir("target_images")

tar_path = random.choice(tar_files)

# print(tar_path)

tar_img = Image.open("target_images/" + tar_path)
tar_img = tar_img.convert("RGBA")
tar_img = tar_img.transpose(1)

bgd_img = Image.open("master_background.png",mode="r")
bgd_img = bgd_img.convert("RGBA")

img = Image.open("target_images/cross,Blue,Q,Yellow.png")
img
bgd_img = Image.open("master_background.png")
#%%
cam, intersection, bgd, rot = gen_valid_cam()
print(rot)
#%%

plt.plot(*cam.exterior.xy)
plt.plot(*intersection.exterior.xy)
plt.plot(*bgd.exterior.xy)

test = bgd_img.transform((4032,3040),ImageTransform.QuadTransform(np.ravel(cam.exterior.coords)))
test.show()
#%%
# Translation
dx = -1 * cam.exterior.coords[0][0]
dy = -1 * cam.exterior.coords[0][1]

# Rotation
cos_theta = np.cos(np.deg2rad(rot-90))
sin_theta = np.sin(np.deg2rad(rot-90))

# Create the 6-tuple for the affine transform
affine_tuple = (cos_theta, -sin_theta, dx, sin_theta, cos_theta, dy)

# Apply the affine transform
intersection = affinity.affine_transform(intersection, affine_tuple)
cam = affinity.affine_transform(cam, affine_tuple)

# intersection = affinity.translate(intersection,yoff=-1*cam.exterior.coords[1][1])
# cam = affinity.translate(cam,yoff=-1*cam.exterior.coords[1][1])

# cam = affinity.translate(cam,-1*cam.exterior.coords[0][0],-1*cam.exterior.coords[0][1])

plt.plot(*cam.exterior.xy)
plt.plot(*intersection.exterior.xy)
plt.plot(*bgd.exterior.xy)


valid_bbox = False
fnl_bbox = []
rot_bbox = 0
corner_bbox = []
while valid_bbox == False:
    rot_bbox = random.randint(0, 359)
    rot_bbox_tht = math.radians(rot_bbox)
    # print(rot_bbox)
    minx, miny, maxx, maxy = intersection.bounds
    corner_bbox = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
    while not intersection.contains(corner_bbox):
        corner_bbox = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
    # print(corner_bbox)
    box = [[0, 0], [24, 0], [24, 36], [0, 36]]
    rot_bbox_arr = [[math.cos(rot_bbox_tht), -1 * math.sin(rot_bbox_tht)], [math.sin(rot_bbox_tht), math.cos(rot_bbox_tht)]]
    rot_bbox_box = np.dot(box, rot_bbox_arr)
    fnl_bbox = []
    for i in range(len(box)):
            # print(rot_bbox_box[i])
            # # print(corner_bbox.x)
            coord_bbox = np.add(rot_bbox_box[i], [corner_bbox.x, corner_bbox.y])
            # print(coord_bbox)
            fnl_bbox.append(list(coord_bbox))
    # print(fnl_bbox)
    poly_bbox = Polygon(fnl_bbox)
    if poly_bbox.within(intersection):
        valid_bbox = True
        # print("pog")
    else:
        valid_bbox = False

# # print(poly_bbox)

# print("______________________")

# print()

bgd_img.show()
corner[0] *= -1
corner[1] *= -1

rot_tht = rot_tht - int(rot_tht/(math.pi / 2)) * math.pi/2
# rot_arr = [math.cos(rot_tht), -1 * math.sin(rot_tht)], [math.sin(rot_tht), math.cos(rot_tht)]
corner = np.dot(rot_arr,corner)
print(corner)
mat = [math.cos(rot_tht), -1 * math.sin(rot_tht), math.sin(rot_tht), math.cos(rot_tht), corner[0], corner[1]]
cam_coord = list(cam.exterior.coords)
cam_coord.pop()
# print(cam_coord, "cam")
fnl_img = bgd_img.transform((4032,3040), ImageTransform.QuadTransform(np.ravel(cam_coord)))
# fnl_img.show()

# print(corner)

intersection = affinity.affine_transform(intersection, mat)
cam = affinity.affine_transform(cam, mat)
bgd = affinity.affine_transform(bgd, mat)
poly_bbox = affinity.affine_transform(poly_bbox, mat)

# print("test")
# print(intersection)
# print(list(cam.exterior.coords))
# print(bgd)
# print(poly_bbox)



plt.plot(*intersection.exterior.xy)
plt.plot(*cam.exterior.xy)
# plt.plot(*bgd.exterior.xy)
plt.plot(*poly_bbox.exterior.xy)
plt.plot(*poly_bbox.envelope.exterior.xy)

# print(list(cam.exterior.coords))

# # print(bound)
# # print(bound)

# plt.plot()

fnl_img_draw = ImageDraw.Draw(fnl_img)
# print("<<<<<<<<<<<")
# print(poly_bbox.exterior.coords[0])
# fnl_img_draw.line((poly_bbox.exterior.coords[0] + poly_bbox.exterior.coords[1]), fill="Red", width=3)
fnl_img.show()

plt.show()
