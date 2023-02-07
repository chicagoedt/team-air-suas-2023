import easyocr 
import cv2 # img processing

img_path = 'non scaled a.png'

# read img -> matrix
img = cv2.imread(img_path)

# scale the img
sc

# initialize the easyocr model
Reader = easyocr.Reader(['en'])

# img matrix input ->easyocr-> output
result = Reader.readtext(img)
print(result)
print(type(result))

# show img with a bounding box
