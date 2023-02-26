from y_detectShapeLetterColor import *
from testingHelper import *

folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName_list = [i for i in os.listdir(folder_path) if len(i) == 21] # to take only img whose format is img_XXX_tar_XXX_<letter>.jpg, the len of this string is 21

numImages = 50
randomImgName_list = chooseRandomImages(imgName_list, numImages)
for imgName in randomImgName_list:
    print(imgName)
    img_path = os.path.join(folder_path, imgName)

    # images that have shapeColor == letterColor will leads to wrong answers
    shapeColor, letterColor = readImgPathGetShapeAndLetterColor(img_path)
    print('-----------------------------------------------------')
'''
    'None' stands for undefined color: gray and other trash color
'''