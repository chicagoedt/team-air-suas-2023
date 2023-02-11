from text_recognition import *
import os

folder_path = '/Users/mightymanh/Desktop/myCode/myPy/pytorch stuff/team-air-suas-2023-fix-target/simulate-images/snapshots/target/'
targets_list = [i for i in os.listdir(folder_path) if len(i) == 21]
targets_list.sort()
answers_list = [i[-5] for i in targets_list]
num_files = len(targets_list)

# test some image
for i in range(num_files):
    print('------------------------------')
    print('reading:', targets_list[i])
    img_path = os.path.join(folder_path, targets_list[i])
    expectedLetter = answers_list[i]
    result = readImgPathDetectLetter(img_path, 500, 20)
    if len(result) == 0:
        actualLetter = ''
    else:
        actualLetter = result[1]

    print(result)
    print('actual letter', actualLetter)
    print('expected letter', expectedLetter)
    

    print('------------------------------')


# Plan for testing:
# gonna iterate through all files and if correct then cool.
# if wrong then write img into a pdf file and keep appending
#

    

