from testingHelper import *

folder_path = '/Users/mightymanh/Desktop/myCode/myPy/pytorch stuff/team-air-suas-2023-fix-target/simulate-images/snapshots/target/'

accuracy_list = []
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for letter in letters:
    print('##########################################')
    accuracy = getAccuracyOfTextDetection(folder_path, 400, 30, letter, 30)
    accuracy_list.append(accuracy)
    print('Finish letter:', letter)
    print('##########################################')


print('Result:')
for i in range(len(letters)):
    print(letters[i], ': ', accuracy_list[i])