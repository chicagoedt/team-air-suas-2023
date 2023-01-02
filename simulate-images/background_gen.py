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
        print("Which image it is on rn:",_)
        tl_point = polygon_random_points(polygon)

        print(tl_point)

        point = (int(tl_point.x),int(tl_point.y))

        seed = [random.randint(0,89), point[0], point[1]]

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
        print(bbox)
        # rot_img.show()
        # print(rot_img.mode)
        angle = seed[0]
        bgd_img.alpha_composite(rot_img,dest=point)
        for arr in bbox:
            arr[0] += point[0]
            arr[1] += point[1]
            print(arr)

        # bgd_img.crop()
        img = ImageDraw.Draw(bgd_img)
        for arr in bbox:
            img.point(arr,fill="Green")
            # print("point done")
        # bgd_img.show()

        print(bbox)
        print("master{}__{}__{}".format(seed[0],seed[1],seed[2])+".jpg")
        bgd_img.convert("RGB").save(master_dir + "master{}__{}__{}".format(seed[0],seed[1],seed[2])+".jpg")

        valid = False
        target = Polygon(bbox)
        fnl_box = []
        corner = []
        rot_arr = []
        rot_tht = 0
        while valid == False:
            rot = random.randint(0, 359)
            rot_tht = math.radians(rot)
            print(rot)
            corner = [random.randint(0, bgd_img.width-1), random.randint(0, bgd_img.height-1)]
            # print(corner)
            box = [[0, 0], [4032, 0], [4032, 3040], [0, 3040]]
            rot_arr = [[math.cos(rot_tht), -1 * math.sin(rot_tht)], [math.sin(rot_tht), math.cos(rot_tht)]]
            rot_box = np.dot(box, rot_arr)
            fnl_box = []
            for i in range(len(box)):
                coord = np.add(rot_box[i], corner)
                # print(coord[0])
                # print(coord[1])
                if 0 < coord[0] < bgd_img.width-1 and 0 < coord[1] < bgd_img.height-1:
                    valid = True
                    # print(valid)
                else:
                    valid = False
                    break
                fnl_box.append(list(coord))
            if len(fnl_box) == 4:
                cam = Polygon(fnl_box)
                if not (cam.contains(target)):
                    valid = False
                    # print("welp")
                else:
                    print("pog")
            # print(valid)
            # print(fnl_box)
        print(corner)
        for i in range(len(bbox)):
            bbox[i] = np.subtract(bbox[i], corner)
            print(bbox[i])
        print(rot_arr)
        # bbox = np.dot(bbox, rot_arr)
        for i in range(len(bbox)):
            bbox[i] = np.add(bbox[i], corner)
            print(bbox[i])
        print(list(bbox[0]))
        print(list(bbox[1]))

        fnl_box = np.ravel(fnl_box)
        test = ImageDraw.Draw(bgd_img)
        test.line((list(bbox[0]) + list(bbox[1])), fill="Blue", width=3)
        test.line((list(bbox[1]) + list(bbox[2])), fill="red", width=3)
        test.line((list(bbox[2]) + list(bbox[3])), fill="red", width=3)
        test.line((list(bbox[3]) + list(bbox[0])), fill="red", width=3)
        test.ellipse((corner[0]-100,corner[1]-100,corner[0]+100,corner[1]+100), fill="Blue")
        # bgd_img.show()
        fnl_img = bgd_img.transform((4032,3040), ImageTransform.QuadTransform(fnl_box))
        test2 = ImageDraw.Draw(fnl_img)
        print("test2")
        rot_tht = 1/rot_tht
        print(rot_tht)

        rot_arr = np.linalg.inv([[math.cos(rot_tht), -1 * math.sin(rot_tht)], [math.sin(rot_tht), math.cos(rot_tht)]])
        for i in range(len(bbox)):
            bbox[i] = np.subtract(bbox[i], corner)
            # print(bbox[i])
        # print(rot_arr)
        bbox = np.dot(bbox, rot_arr)
        print(list(bbox[0]))
        print(list(bbox[1]))
        test2.line((list(bbox[0]) + list(bbox[1])), fill="Red", width=3)
        test2.line((list(bbox[1]) + list(bbox[2])), fill="Purple", width=3)
        test2.line((list(bbox[2]) + list(bbox[3])), fill="Purple", width=3)
        test2.line((list(bbox[3]) + list(bbox[0])), fill="Purple", width=3)
        test2.ellipse((-100,-100,100,100), fill="Yellow")


        print("{}_{}_{}_{}.jpg".format(seed[0],seed[1],seed[2],tar_path))
        fnl_img.show()
        fnl_img.convert("RGB").save(final_dir+"{}_{}_{}_{}.jpg".format(seed[0],seed[1],seed[2],tar_path))
    return

generate_final(1)
#BIG NOTE
# Someone who knows how to do linear algebra figure out a way for us to use the amount we
# rotate each target or seed[0] and the fact that the targets are a given size