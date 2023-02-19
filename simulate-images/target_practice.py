import os
from shutil import rmtree

from PIL import Image

import vars
from sim_images import *


def main():
    numTarget = input("How many targets? (press enter for 10 per runway snapshot) >> ") 
    numTarget = 10 if numTarget == "" else int(numTarget)

    rotateTarget = True if input("Rotate target? (press enter for yes) >> ") == "" else False

    shapeColor = input("What shape color? (press enter for random) >> ")
    shapeColor = "random" if shapeColor == "" else shapeColor

    letter = input("What letter? (press enter for random) >> ")
    letter = "random" if letter == "" else letter

    letterColor = input("What letter color? (press enter for random) >> ")
    letterColor = "random" if shapeColor == "" else shapeColor

    print(numTarget, rotateTarget, shapeColor, letter, letterColor)

    os.chdir(os.path.dirname(__file__))

    # open runway image
    runway = Image.open("reference-images/runway.png")

    # check if empty images have already been generated
    generateNew = True
    if os.path.exists(vars.noTargetDir):
        generateNew = input(
            "\nLooks like you have already generated empty runway images. Would you like to generate new ones?\n  (y/N) >> ")
        generateNew = True if generateNew == "y" else False

    if generateNew:
        if os.path.exists(vars.noTargetDir):
            rmtree(vars.noTargetDir)
        os.makedirs(vars.noTargetDir)
        generateEmptyImages(runway)


# create runway images with targets on them
def genSmallTarget(num, rotate, shapeColor, letter, letterColor):
    # check if target_practice directory exists
    if os.path.exists(vars.targetPracticeDir):
        rmtree(vars.targetPracticeDir)
    os.makedirs(vars.targetPracticeDir)
    
    # remove target-info.csv if it exists
    if os.path.exists(vars.targetPracticeInfoPath):
        os.remove(vars.targetPracticeInfoPath)
    with open(vars.targetPracticeInfoPath, "w") as info:
        info.write("filename,shape,shapeColor,letter,letterColor\n")

    # create <num> simulated images for each empty image
    for filename in os.listdir(vars.noTargetDir):
        print(f"Simulating {num} targets for {filename}")
        with Image.open(os.path.join(vars.noTargetDir, filename)) as emptyImage:
            for i in range(num):
                with emptyImage as simImage:
                    simImage = simImage.convert("RGBA")
                    simFilename = filename[:-4] + f"_tar_{i:03}"

                    t1 = placeTarget(simImage, simFilename, rotate=rotate, color=color, letter=letter)

                    # save image
                    simImage = simImage.convert("RGB")
                    simImage.save(os.path.join(vars.targetDir, simFilename + ".jpg"))


if __name__ == "__main__":
    main()
