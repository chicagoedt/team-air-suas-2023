from testingHelper import *

folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'

letters = 'ABCDEFGHJKLMNOPQRSTUVWXYZ' # since easyocr is blind to 'I', I dont include it in here
letter_dict = {}
for letter in letters:
    correct, wrong, cannotDetect = getAccuracyOfTextDetection(folder_path, 120, 20, letter, 30)
    letter_dict[letter] = (correct, wrong, cannotDetect)

print('############## OVERALL ######################')
print('Letter, correct, wrong, cannotDetect')
for letter, tup in letter_dict.items():
    print('{}: {}'.format(letter, tup))