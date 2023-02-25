from y_detectShapeLetterColor import *

img_path = 'img_008_tar_030_C.jpg' 
shapeColor, letterColor = readImgPathGetShapeAndLetterColor(img_path)
print('Shape color:', shapeColor)
print('Letter color:', letterColor)

'''
    'None' stands for undefined color: white, brown, gray
'''