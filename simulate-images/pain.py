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



def gen_valid_cam():
    bgd_img = Image.open("master_background.png")
    # global intersection
    # global cam
    # global bgd
    runway = Polygon(([2932, 2688], [2864, 3500], [6800, 3600], [6850, 2800]))
    bgd_w = bgd_img.width
    bgd_h = bgd_img.height
    bgd = Polygon(([0, 0], [bgd_h, 0], [bgd_h, bgd_w], [0, bgd_w]))
    valid = False
    fnl_box = []
    corner = []
    rot_arr = []
    rot_tht = 0
    while valid == False:
        rot = random.randint(0, 359)
        # rot = 0
        rot_tht = math.radians(rot)
        print(rot)
        corner = [random.randint(0, bgd_w - 1), random.randint(0, bgd_h - 1)]
        box = [[0, 0], [4032, 0], [4032, 3040], [0, 3040]]
        rot_arr = [[math.cos(rot_tht), -1 * math.sin(rot_tht)], [math.sin(rot_tht), math.cos(rot_tht)]]
        rot_box = np.dot(box, rot_arr)
        fnl_box = []
        for i in range(len(box)):
            coord = np.add(rot_box[i], corner)
            if 0 < coord[0] < bgd_img.width - 1 and 0 < coord[1] < bgd_img.height - 1:
                valid = True
            else:
                valid = False
                break
            fnl_box.append(list(coord))
        if len(fnl_box) == 4:
            cam = Polygon(fnl_box)
            if not (cam.intersects(runway)):
                valid = False
            else:
                print("pog")
                intersection = cam.intersection(runway)
                print(cam.exterior.coords)
                print(intersection.exterior.coords)
                return cam, intersection, bgd, rot
    return



def gen_valid_tar(background,target):
    minx,miny,maxx,maxy = background.bounds
    print(minx,miny,maxx,maxy)
    valid = False
    corner = []
    rot_arr = []
    rot_tht = 0
    while valid == False:
        rot = random.randint(0, 359)
        # rot = 0
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




# background = Polygon(((2633, 4032), (2736, 2412), (1927, 2316), (1823.5, 4032)))
# target = Image.open("target_images/cross,Blue,Q,Yellow.png")
# tar_poly = gen_valid_tar(background,target)
# plt.plot(*(tar_poly.envelope).exterior.xy)
# plt.plot(*(tar_poly).exterior.xy)
# plt.plot(*background.exterior.xy)
# plt.show()