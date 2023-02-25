from y_TextDetection import *
from y_specialcase import *

reader = easyocr.Reader(['en'])
img_path = 'img_008_tar_039_U.jpg'
result_list = readImgPathDetectLetter(img_path, 120, 20, reader) 
narrow_list = narrowResultList(result_list)

result_list = [i[1] for i in result_list] # simplify result_list for nicer print
print('What easyocr gets:', result_list)
print('What we deduce from results get by easyocr:', narrow_list)