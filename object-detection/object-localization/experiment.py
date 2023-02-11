import shutil
import os
import cv2

# list files in the folder datas and sort it, check its behavior
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/pytorch stuff/team-air-suas-2023-fix-target/simulate-images/snapshots/target/'
jpgs_list = [i for i in os.listdir(folder_path) if (not os.path.isdir(i)) and len(i) == 19]
yolos_list = [i for i in os.listdir(folder_path) if (not os.path.isdir(i)) and len(i) == 20]
targets_list = [i for i in os.listdir(folder_path) if (not os.path.isdir(i) and len(i) >= 21)]
jpgs_list.sort()
yolos_list.sort()
targets_list.sort()

print(len(jpgs_list))
print(len(yolos_list))
print(len(targets_list))

for i in range(len(jpgs_list)):
    if jpgs_list[i][:15] == yolos_list[i][:15] and yolos_list[i][:15] == targets_list[i][:15]:
        print('Yes')

