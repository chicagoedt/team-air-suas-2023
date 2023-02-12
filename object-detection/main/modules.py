import sys

objectLocalization_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023/object-detection/object-localization'
textDetection_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023/object-detection/text-detection'

# append crop from object-localization folder
sys.path.append(objectLocalization_path)
from crop import *
sys.path.pop()

# append y_letterImageMapping from text-detection folder
sys.path.append(textDetection_path)
from y_letterImageMapping import *
sys.path.pop()
