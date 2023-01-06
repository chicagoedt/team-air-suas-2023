from PIL import Image, ImageDraw, ImageOps
import math
from time import sleep
import vars
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
    bgd = Polygon(([0, 0], [bgd_img.width, 0], [bgd_img.width, -1 * bgd_img.height], [0, -1 * bgd_img.height]))
    valid = False
    while valid == False:
        rot = random.randint(0, 359)
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
                # plt.show()

                inter_trans = affinity.translate(intersection, xoff=-1 * corner[0],yoff=-1 * corner[1])
                inter_rot1 = affinity.rotate(inter_trans, -1 * rot, origin=(0, 0))
                inter_rot = affinity.rotate(inter_rot1, 180, origin=(vars.cam_res[0]//2,vars.cam_res[1]//-2,))
                inter_fnl = affinity.scale(inter_rot, yfact=-1, origin=(0, 0))
                inter_transformed = affinity.scale(inter_fnl, xfact=-1, origin=(vars.cam_res[0]//2,vars.cam_res[1]//-2,))

                cam_fnl_crop = affinity.scale(box, yfact=-1, origin=(0, 0))
                cam_fnl_xy = np.ravel((cam_fnl_crop.exterior.coords[3] + cam_fnl_crop.exterior.coords[4] +
                                       cam_fnl_crop.exterior.coords[1] + cam_fnl_crop.exterior.coords[2]))
                cropped_img = bgd_img.transform((4032, 3040), ImageTransform.QuadTransform(cam_fnl_xy))

                return box, intersection, inter_transformed, cropped_img






def gen_valid_tar(crop_img,runway_geom,target):
    minx,miny,maxx,maxy = runway_geom.bounds
    # print(minx,miny,maxx,maxy)
    valid = False
    while valid == False:
        rot = random.randint(0, 359)
        # rot = 0
        print(rot)
        corner = [random.randint(int(minx),int(maxx)),random.randint(int(miny),int(maxy))]
        box = Polygon([[0, 0], [target.width, 0], [target.width, target.height], [0, target.height]])

        # print(box)
        plt.plot(*box.exterior.xy, label="pre", color="yellow")

        box = affinity.rotate(box,rot,(0,0))
        plt.plot(*box.exterior.xy, label = "rot", color="orange")

        # print(box)
        box = affinity.translate(box,xoff=corner[0],yoff=corner[1])
        # print(valid)
        # print(box)
        plt.plot(*box.exterior.xy, label = "final", color="Red")

        print(*box.exterior.coords)
        if box.within(runway_geom):
            # if box.within(runway_geom):
            crop_img = crop_img.convert("RGBA")
            target = target.convert("RGBA")
            valid = True
            print("pog")
            tar_rot = target.rotate(rot,expand=True, fillcolor="#00000000")
            tar_mnx, _miny, _maxx, tar_mxy = box.bounds
            crop_img.alpha_composite(tar_rot, dest=(int(tar_mnx),int(tar_mxy)))
            # crop_img.show()
            box_real = affinity.scale(box,yfact=-1,origin=(0,tar_mxy))
            return box,rot,crop_img,box_real
        else:
            valid = False




def fnl_valid_img(amount):
    for _ in range(amount):
        print("Which image it is on rn:", _)
        bgd_img = Image.open("master_background.png")
        cam, intersection, bgd, cropped = gen_valid_cam(bgd_img)

        # plt.show()
        bgd_img_drw = ImageDraw.Draw(cropped)
        bgd_img_drw.polygon(bgd.exterior.coords,fill="Black")
        # cropped.show()

        tar_files = os.listdir("target_images")
        tar_path = random.choice(tar_files)
        print(tar_path)
        tar_img = Image.open("target_images/" + tar_path)

        box, rot, crop_img, box_real = gen_valid_tar(cropped,bgd,tar_img)

        new_drw = ImageDraw.Draw(crop_img)
        new_drw.polygon(box_real.exterior.coords,fill="white")

        final_dir = "final_images/"
        crop_img.save(final_dir+"{}_{}_{}_{}.png".format(box_real.exterior.coords))