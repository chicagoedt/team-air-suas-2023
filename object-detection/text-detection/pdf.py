'''
    Stack multiple images into pdf. 
    Each page will contain original image, image after preprocessing and rotated that gets result,
    the text of process and compared with answer
'''

from PIL import Image # for reading pdf
import cv2
import numpy as np
import os

folder_path = '/Users/mightymanh/Desktop/experiment/'
# images_name = ['img_001_tar_196_A.jpg', 'img_001_tar_197_E.jpg', 'img_001_tar_198_O.jpg']
# images_name.sort()
# images = [Image.open(os.path.join(folder_path, i)) for i in images_name]


# pdf_path = '/Users/mightymanh/Desktop/experiment/exp.pdf'

# images[0].save(
#     pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
# )

image_path = folder_path + 'img_001_tar_196_A.jpg'
img = cv2.imread(image_path)
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img_pil = Image.fromarray(img)

img2 = cv2.imread(folder_path + 'img_001_tar_197_E.jpg')
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
# img2_pil = Image.fromarray(img2)
# img_pil.save('experiment.pdf', save_all = True, append_images = [img2_pil])

img3 = cv2.imread(folder_path + 'img_001_tar_198_O.jpg')
# img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
# img3_pil = Image.fromarray(img3)


height = img.shape[0]
gutter = np.full((height, 3, 3), 255, dtype = np.uint8)
img_h = cv2.hconcat([img, gutter, imgRGB])
img_h_pil = Image.fromarray(img_h)
img_h_pil.save('experiment.pdf')

# img_h = cv2.cvtColor(img_h, cv2.COLOR_BGR2RGB)
# img_h_pil = Image.fromarray(i)



