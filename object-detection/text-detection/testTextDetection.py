from testingHelper import *
import pandas as pd

reader = easyocr.Reader(['en'])
folderPath = '/Users/mightymanh/Desktop/myCode/myPy/target-practice/simulate-images/snapshots/target_practice'
csvPath = '/Users/mightymanh/Desktop/myCode/myPy/target-practice/simulate-images/snapshots/target_practice_info.csv'
df = pd.read_csv(csvPath)
filename_list = list(df["filename"])
letter_list = list(df["letter"])
print('Size of filename_list: {} and size of letter_list: {}'.format(len(filename_list), len(letter_list)))

# loop
letters = 'ABCDEFGHJKLMNOPQRSTUVWXYZ0123456789' # since easyocr is blind to 'I', I dont include it in here
letter_dict = {}
numIter = 30
for letter in letters:
    correct, wrong, cannotDetect = getAccuracyOfTextDetection(folderPath, reader, letter, 130, 130, 50, numIter, filename_list, letter_list)
    letter_dict[letter] = (correct, wrong, cannotDetect)

print('############## OVERALL ######################')
print('Letter, correct, wrong, cannotDetect')
for letter, tup in letter_dict.items():
    print('{}: {}'.format(letter, tup))