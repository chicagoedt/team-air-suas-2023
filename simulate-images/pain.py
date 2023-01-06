from PIL import Image, ImageDraw, ImageOps
import math
from time import sleep
import numpy as np
import random
from PIL import ImageTransform
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import affinity
import matplotlib.pyplot as plt
import os



def gen_valid_cam(bgd_img):
    runway = Polygon((
        (3033, -2693),
        (2971, -3551),
        (6754, -3670),
        (6786, -2824)
    ))
    runway_flip = affinity.scale(runway,yfact=-1,origin=(0,0))
    # runway_flip = affinity.scale(runway,yfact=,xfact=.95,origin="centroid")
    # bgd_img_draw = ImageDraw.Draw(bgd_img)
    # print(*runway_flip.exterior.coords)
    # bgd_img_draw.polygon(runway_flip.exterior.coords,fill="black")
    # bgd_img.show()
    bgd = Polygon(([0, 0], [bgd_img.width, 0], [bgd_img.width, -1 * bgd_img.height], [0, -1 * bgd_img.height]))
    valid = False
    # print(valid)
    # global box, intersection, rot_tht
    while valid == False:
        rot = random.randint(0, 359)
        # rot = 0
        rot_tht = math.radians(rot)
        # print(rot)
        # print(rot)
        corner = [random.randint(0, bgd_img.width - 1), random.randint(-1*(bgd_img.height - 1),0)]
        # print(corner)
        box = Polygon([[0, 0], [4032, 0], [4032, -3040], [0, -3040]])
        # print(box)
        plt.plot(*box.exterior.xy, label="pre", color="yellow")

        box = affinity.rotate(box,rot,(0,0))
        plt.plot(*box.exterior.xy, label = "rot", color="orange")

        # print(box)
        box = affinity.translate(box,xoff=corner[0],yoff=corner[1])
        # print(valid)
        # print(box)
        plt.plot(*box.exterior.xy, label = "final", color="Red")

        # plt.show()
        # sleep(10)
        if box.within(bgd):
            # print("enter looop")
            if not (box.intersects(runway)):
                valid = False
            else:
                print("pog")
                intersection = box.intersection(runway)
                # print(*box.exterior.coords)
                # print(*intersection.exterior.coords)
                valid = True
                plt.plot(*intersection.exterior.xy)
                plt.show()
                return box, intersection, bgd, rot






def gen_valid_tar(background,target):
    minx,miny,maxx,maxy = background.bounds
    print(minx,miny,maxx,maxy)
    valid = False
    corner = []
    rot_arr = []
    rot_tht = 0
    while valid == False:
        # rot = random.randint(0, 359)
        rot = 0
        print(rot)
        corner = [random.randint(int(minx),int(maxx)),random.randint(int(miny),int(maxy))]
        box = Polygon([[0, 0], [target.width, 0], [target.width, target.height], [0, target.height]])

        dx = corner[0]
        dy = corner[1]

        box = affinity.rotate(box, rot, (0, 0))
        box = affinity.translate(box,dx,dy)

        plt.plot(*box.exterior.xy)
        print(*box.exterior.coords)
        if box.within(background):
            valid = True
            print("pog")
            return box,rot
        else:
            valid = False




bgd_img = Image.open("master_background.png")
cam, intersection, bgd, rot = gen_valid_cam(bgd_img)

print(cam.exterior.coords[0])
cam_trans = affinity.translate(cam,xoff=-1 * cam.exterior.coords[0][0], yoff=-1 * cam.exterior.coords[0][1])
inter_trans= affinity.translate(intersection,xoff=-1 * cam.exterior.coords[0][0], yoff=-1 * cam.exterior.coords[0][1])

inter_rot1 = affinity.rotate(inter_trans,-1*rot,origin=(0,0))
cam_rot = affinity.rotate(cam_trans,-1*rot,origin=(0,0))
inter_rot = affinity.rotate(inter_rot1,180,origin=(cam_rot.centroid))

cam_fnl = affinity.scale(cam_rot,yfact=-1, origin=(0,0))
cam_fnl_crop = affinity.scale(cam,yfact=-1, origin=(0,0))

inter_fnl = affinity.scale(inter_rot,yfact=-1, origin=(0,0))

inter_fnl = affinity.scale(inter_fnl,xfact=-1, origin=(cam_fnl.centroid))

bgd = affinity.scale(bgd,yfact=-1, origin=(0,0))
plt.plot(*cam.exterior.xy)
plt.plot(*intersection.exterior.xy)
plt.plot(*inter_rot1.exterior.xy)
plt.plot(*cam_rot.exterior.xy)

plt.plot(*inter_fnl.exterior.xy)
plt.plot(*cam_fnl.exterior.xy)



plt.show()
cam_fnl_xy = np.ravel((cam_fnl_crop.exterior.coords[3]+cam_fnl_crop.exterior.coords[4]+cam_fnl_crop.exterior.coords[1]+cam_fnl_crop.exterior.coords[2]))
print(*cam_fnl_crop.exterior.coords)

test = bgd_img.transform((4032,3040),ImageTransform.QuadTransform(cam_fnl_xy))
bgd_img_drw = ImageDraw.Draw(test)
bgd_img_drw.polygon(inter_fnl.exterior.coords,fill="Black")
test.show()
