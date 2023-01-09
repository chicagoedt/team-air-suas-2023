import os
import numpy as np
from time import sleep
import csv


final_dir = "final_images"
i = 0
orig_names = os.listdir(final_dir)

header = ["orig_name","new_name","coord1_x","coord1_y","coord2_x","coord2_y","coord3_x","coord3_y","coord4_x","coord4_y",]

with open('data.csv', mode='w') as csvfile:
    csvwriter = csv.writer(csvfile,delimiter=',')
    csvwriter.writerow(header)
    for file in orig_names:
        data = []
        data.append(file)
        i += 1
        # name.append("img_{}".format(i))
        name = "img_{}.jpg".format(i)
        data.append(name)
        coords = ((file.strip(".jpg")).translate({ord(letter): None for letter in "() "})).split("_")
        print(coords)
        not_fnl_coords = []
        for coord in coords:
            not_fnl_coords.append([int(round(float(x))) for x in coord.split(",")])

        print(not_fnl_coords)
        not_fnl_coords = np.ravel(not_fnl_coords)
        data = data + list(not_fnl_coords)
        print(data)
        print(len(data))
        csvwriter.writerow(data)
        os.rename(final_dir+"/"+file,final_dir + "/" +name)
    # print(name,fnl_coords,min_coord,max_coord,centroid)
    # sleep(30)


# writer = csv.


