from PIL import Image, ImageDraw
import random
import cv2
import numpy as np
from shapely.geometry import Polygon, MultiPoint, Point
import os


final_dir = "final_images/"
master_dir = "master_images/"
polygon = Polygon(([2932,2688],[2864,3500],[6800,3600],[6850,2800]))
def polygon_random_points (poly):
    min_x, min_y, max_x, max_y = poly.bounds
    points = []
    while len(points) < 1:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)
    return points[0]
def generate_final(amount):
    for _ in range(amount):
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
        # rot_img.show()
        # print(rot_img.mode)
        angle = seed[0]
        bgd_img.alpha_composite(rot_img,dest=point)

        # bgd_img.crop()

        # bgd_img.show()

        bgd_img.convert("RGB").save(master_dir + "master{}__{}__{}".format(seed[0],seed[1],seed[2])+".jpg")
        tlx_crop = random.randint(0,2864)
        tly_crop = random.randint(0,2688)
        while not(tlx_crop < seed[1] < tlx_crop+4032 and tlx_crop < seed[1]+rot_img.width < tlx_crop+4032):
            tlx_crop = random.randint(0, 2864)
            print("retry")
        while not(tly_crop < seed[2] < tly_crop+3040 and tly_crop < seed[2]+rot_img.height < tly_crop+3040):
            print("retry")
            tly_crop = random.randint(0, 2688)
        print(str(tlx_crop)+" "+str(tly_crop)+" "+str(tlx_crop+4032)+" "+str(tly_crop+3040))
        print(bgd_img.size)
        brx_crop = tlx_crop+4032
        bry_crop = tly_crop+3040
        fnl_img = bgd_img.crop((tlx_crop,tly_crop,brx_crop,bry_crop))
        fnl_img.convert("RGB").save(final_dir+"{}_{}_{}_{}.jpg".format(seed[0],seed[1]-tlx_crop,seed[2]-tly_crop,tar_path))
    return

#BIG NOTE
# Someone who knows how to do linear algebra figure out a way for us to use the amount we
# rotate each target or seed[0] and the fact that the targets are a given size