'''
    given target image, detect shape color and letter color
'''

import os
from y_colorDetectionHelper import *

# init hyper variables
cropSize = 40

# init images
folder_path = 'cropImages'
imgName_list = ['81_1458_Brown.jpg']

for imgName in imgName_list:
    imgPath = os.path.join(folder_path, imgName)
    img = cv2.imread(imgPath)

    # get shape and letter color
    shapeColor, letterColor = readImgGetShapeAndLetterColor(img, cropSize)

