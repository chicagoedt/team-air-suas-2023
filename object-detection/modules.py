'''
    necessary modules for running y_main.py
'''
import sys
import os

currentDirectory = os.getcwd()

objectLocalization_path = os.path.join(currentDirectory, 'object-localization')
textDetection_path = os.path.join(currentDirectory, 'text-detection')

# import crop from object-localization folder
sys.path.append(objectLocalization_path)
from crop import *    # cropFolder()
sys.path.pop()

# import y_letterImageMapping from text-detection folder
sys.path.append(textDetection_path)
from y_letterImageMapping import *  # mapLettersToImages()
sys.path.pop()
