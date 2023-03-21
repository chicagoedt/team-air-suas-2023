from modules import *

ImagesByCamera_Folder = 'ImagesByCamera'
CroppedImages_Folder = 'CroppedImages' 

# input from judge
inputsFromJudge = input('Enter letters given by judge, between each pair of letters is a space, like "A B C D F" not "AB CDF".\n'
                        'You input: ')
letters = inputsFromJudge.split()

# object localization, crop
cropFolder(ImagesByCamera_Folder, CroppedImages_Folder, 100, 100)
print('#################################')

# text detection, mapping letters to each images
imageNames_list = os.listdir(CroppedImages_Folder)
results = mapLettersToImages(letters, imageNames_list, CroppedImages_Folder, 400, 20)
