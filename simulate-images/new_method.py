from PIL import Image, ImageDraw, ImageOps
import math
import numpy as np
import random
from PIL import ImageTransform
from pain import gen_valid_cam, gen_valid_tar
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import affinity
import matplotlib.pyplot as plt
import os

final_dir = "final_images/"
master_dir = "master_images/"
def gen_pics(amount):
    for _ in range(amount):
        print("Which image it is on rn:", _)

        tar_files = os.listdir("target_images")

        tar_path = random.choice(tar_files)

        # print(tar_path)

        tar_img = Image.open("target_images/" + tar_path)
        tar_img = tar_img.convert("RGBA")
        tar_img = tar_img.transpose(1)

        bgd_img = Image.open("master_background.png",mode="r")
        bgd_img = bgd_img.convert("RGBA")

        cam, intersection, bgd, rot = gen_valid_cam()
        print(rot)

        plt.plot(*cam.exterior.xy)
        plt.plot(*intersection.exterior.xy)
        plt.plot(*bgd.exterior.xy)

        test = bgd_img.transform((4032,3040),ImageTransform.QuadTransform(np.ravel(cam.exterior.coords)))
        # test.show()

        intersection = affinity.translate(intersection,-1*cam.exterior.coords[0][0],-1*cam.exterior.coords[0][1])
        cam = affinity.translate(cam,-1*cam.exterior.coords[0][0],-1*cam.exterior.coords[0][1])
        intersection = affinity.rotate(intersection,rot-90,(0,0))
        cam = affinity.rotate(cam,rot-90,(0,0))
        #Who fucking knows why but I tried combining the transformations together and they fucked everything up ever so slightly
        #Probably something to do with a memory leak bc the floats are gigantic, but idk an easy way to convert an array to a
        # smaller datatype

        plt.plot(*cam.exterior.xy)
        plt.plot(*intersection.exterior.xy)
        plt.plot(*bgd.exterior.xy)
        plt.show()

        # tar_poly, rot_tar = gen_valid_tar(intersection,tar_img)
        # # print(gen_valid_tar(intersection,target))

        # plt.plot(*cam.exterior.xy)
        # plt.plot(*tar_poly.exterior.xy)
        # plt.plot(*intersection.exterior.xy)
        # plt.plot(*bgd.exterior.xy)


        # tar_poly = affinity.translate(tar_poly,yoff=4032)
        # cam = affinity.translate(cam,yoff=4032)
        # intersection = affinity.translate(intersection,yoff=4032)
        intersection = affinity.scale(intersection,yfact=-1,origin=(0,0))
        cam = affinity.scale(cam,yfact=-1,origin=(0,0))
        # tar_poly = affinity.scale(tar_poly,yfact=-1,origin=(0,0))

        # minx, miny, maxx, maxy = tar_poly.bounds
        # tl_corner = [minx,maxy]
        # print(tl_corner)

        plt.plot(*cam.exterior.xy)
        # plt.plot(*tar_poly.exterior.xy)
        plt.plot(*intersection.exterior.xy)
        plt.plot(*bgd.exterior.xy)
        plt.show()

        test2 = ImageDraw.Draw(test)
        # pog_coords = tar_poly.envelope.exterior.coords

        # test2.line((pog_coords[0][1],pog_coords[0][0],pog_coords[1][1],pog_coords[1][0]), fill="Black", width=3)
        # test2.line((pog_coords[1][1],pog_coords[1][0],pog_coords[2][1],pog_coords[2][0]), fill="Black", width=3)
        # test2.line((pog_coords[2][1],pog_coords[2][0],pog_coords[3][1],pog_coords[3][0]), fill="Black", width=3)
        # test2.line((pog_coords[3][1],pog_coords[3][0],pog_coords[4][1],pog_coords[4][0]), fill="Black", width=3)


        # test2.line(((tar_poly.envelope).exterior.coords[1] + (tar_poly.envelope).exterior.coords[2]), fill="Purple", width=3)
        # test2.line(((tar_poly.envelope).exterior.coords[2] + (tar_poly.envelope).exterior.coords[3]), fill="Purple", width=3)
        # test2.line(((tar_poly.envelope).exterior.coords[3] + (tar_poly.envelope).exterior.coords[0]), fill="Purple", width=3)

        for i in range(len((intersection).exterior.coords)-1):
            test2.line(((intersection).exterior.coords[i] + (intersection).exterior.coords[i+1]), fill="Purple", width=3)
        test.save("final_images/test_{}.png".format(_))
        # bgd_img_drw = ImageDraw.Draw(bgd_img)
    return

gen_pics(10)
