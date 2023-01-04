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



def gen_valid_cam():
    bgd_img = Image.open("master_background.png")
    runway = Polygon(([2932, -2688], [2864, -3500], [6800, -3600], [6850, -2800]))
    bgd = Polygon(([0, 0], [bgd_img.width, 0], [bgd_img.width, -1 * bgd_img.height], [0, -1 * bgd_img.height]))
    valid = False
    # print(valid)
    # global box, intersection, rot_tht
    while valid == False:
        # rot = random.randint(0, 359)
        rot = 0
        rot_tht = math.radians(rot)
        # print(rot)
        # print(rot)
        corner = [random.randint(0, bgd_img.width - 1), random.randint(-1*(bgd_img.height - 1),0)]
        print(corner)
        box = Polygon([[0, 0], [4032, 0], [4032, -3040], [0, -3040]])
        # print(box)
        # plt.plot(*box.exterior.xy, label="pre", color="yellow")

        box = affinity.rotate(box,rot,(0,0))
        # plt.plot(*box.exterior.xy, label = "rot", color="orange")

        # print(box)
        box = affinity.translate(box,xoff=corner[0],yoff=corner[1])
        # print(valid)
        print(box)
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
                print(*box.exterior.coords)
                print(*intersection.exterior.coords)
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




# background = Polygon(((2633, 4032), (2736, 2412), (1927, 2316), (1823.5, 4032)))
# target = Image.open("target_images/cross,Blue,Q,Yellow.png")
# tar_poly = gen_valid_tar(background,target)
# plt.plot(*(tar_poly.envelope).exterior.xy)
# plt.plot(*(tar_poly).exterior.xy)
# plt.plot(*background.exterior.xy)
# plt.show()