from PIL import Image, ImageDraw, ImageTransform
import random
import math
import cv2
import numpy as np
import vars
from shapely.geometry import Polygon, MultiPoint, Point
import os


final_dir = "final_images/"
master_dir = "master_images/"
polygon = Polygon((
        (3033, -2693),
        (2971, -3551),
        (6754, -3670),
        (6786, -2824)
    ))
def polygon_random_points (poly):
    min_x, min_y, max_x, max_y = poly.bounds
    points = []
    while len(points) < 1:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)
    return points[0]

def generate_master(amount):
    # for _ in range(amount):
    # print("Which image it is on rn:",_)
    tl_point = polygon_random_points(polygon)

    print(tl_point)

    point = (int(tl_point.x),int(tl_point.y))

    seed = [random.randint(0,359), point[0], point[1]]

    tar_files = os.listdir("target_images")

    tar_path = random.choice(tar_files)

    print(tar_path)

    tar_img = Image.open("target_images/"+tar_path)
    tar_img = tar_img.convert("RGBA")
    bgd_img = Image.open("master_background.png",mode="r")
    bgd_img = bgd_img.convert("RGBA")
    # print(bgd_img.mode)




    rot_img = tar_img.rotate(seed[0],expand=True, fillcolor="#00000000")
    theta_rad = math.radians(seed[0])
    bbox = [0, 0, 0, 0]
    bbox[0] = [0,int(math.sin(theta_rad) * vars.tar_res[0])]
    bbox[1] = [int(math.cos(theta_rad) * vars.tar_res[0]),0]
    bbox[2] = [rot_img.width-1,int(math.cos(theta_rad) * vars.tar_res[1])]
    bbox[3] = [int(math.sin(theta_rad) * vars.tar_res[1]),rot_img.height-1]
    bgd_img.alpha_composite(rot_img,dest=point)
    for arr in bbox:
        arr[0] += point[0]
        arr[1] += point[1]
        print(arr)

    print(bbox)
    # bgd_img.show()
    print("master{}__{}__{}".format(seed[0],seed[1],seed[2])+".jpg")
    # bgd_img.convert("RGB").save(master_dir + "master{}__{}__{}".format(seed[0],seed[1],seed[2])+".jpg")
    return bgd_img

generate_final(1)
#BIG NOTE
# Someone who knows how to do linear algebra figure out a way for us to use the amount we
# rotate each target or seed[0] and the fact that the targets are a given size