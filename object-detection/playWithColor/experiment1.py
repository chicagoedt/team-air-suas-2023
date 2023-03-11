from colorExtraction import *
from testingHelper import *

folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName_list = [i for i in os.listdir(folder_path) if len(i) == 21]

randomImgName_list = chooseRandomImages(imgName_list, 50)

for imgName in randomImgName_list:
    print(imgName)
    img_path = os.path.join(folder_path, imgName)
    readImgPathExtractShapeAndLetterMask(img_path)
    print('---------------------------------------------')
