'''
    given target image, detect shape color and letter color
'''

import os
from y_colorDetectionHelper import *

# init hyper variables
cropSize = 40
stdLightLevel = 72 # this is light level of simulated targets

# init images
folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
imgName_list = ['img_022_tar_183_Q.jpg']

for imgName in imgName_list:
    imgPath = os.path.join(folder_path, imgName)
    img = cv2.imread(imgPath)

    # get shape and letter color
    shapeColor, letterColor = readImgGetShapeAndLetterColor(img, cropSize)

