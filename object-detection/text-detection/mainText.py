# import Independencies
from y_letterImageMapping import *

# this folder will contains all target images cropped by localization code
folder_path = '/Users/mightymanh/Desktop/Testing'
inputsFromJudge = input('Enter letters given by judge, between each pair of letters is a space, like "A B C D F" not "AB CDF".\n'
              'You input: ')

letters = inputsFromJudge.split()
print('Letters:', letters)


# mapping letters to images
imageNames_list = os.listdir(folder_path)
results = mapLettersToImages(letters, imageNames_list, folder_path, 400, 20)
