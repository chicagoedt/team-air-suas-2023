import time
import os
from shutil import rmtree

from PIL import Image
from shapely import affinity

import vars
from target import *
from snapshot import *


def main():
    os.chdir(os.path.dirname(__file__))

    # open runway image
    runway = Image.open("reference-images/runway.png")

    # check if empty images have already been generated
    generateNew = True
    if os.path.exists(vars.noTargetDir):
        generateNew = input(
            "Looks like you have already generated empty runway images. Would you like to generate new ones?\n  (y/N) >> ")
        generateNew = True if generateNew == "y" else False

    if generateNew:
        if os.path.exists(vars.noTargetDir):
            rmtree(vars.noTargetDir)
        os.makedirs(vars.noTargetDir)
        generateEmptyImages(runway)

    numSnapshots = len(os.listdir(vars.noTargetDir))

    numTargets = int(
        input("\nHow many target images do you want to generate for each snapshot? >> "))
    print(f"Generating {numTargets * numSnapshots} target images...")

    start_time = time.time()

    # check if target directory exists
    if os.path.exists(vars.targetDir):
        rmtree(vars.targetDir)
    os.makedirs(vars.targetDir)

    # create target images for each empty image
    for filename in os.listdir(vars.noTargetDir):
        print(f"Placing targets on {filename}...")
        with Image.open(os.path.join(vars.noTargetDir, filename)) as emptyImage:
            for targetNum in range(numTargets):
                with emptyImage as newImage:
                    placeTarget(newImage, filename, targetNum)

    print(f"time: {time.time() - start_time:.2f} seconds")


# create the runway images that the targets will be placed on
def generateEmptyImages(runway):
    print("Generating empty images...")
    start_time = time.time()

    # create snapshot polygon and shift it to the upper right corner of the air drop boundary
    snapshot = box(0, 0, vars.snapshotWidth, vars.snapshotHeight)
    snapshot = affinity.translate(
        snapshot,
        xoff=vars.airDropBoundary.bounds[0],
        yoff=vars.airDropBoundary.bounds[1]
    )

    # create images of runway
    count = 0
    while snapshot.intersects(vars.airDropBoundary):
        # save snapshot image
        droneImage = takePicture(runway, snapshot)
        droneImage = droneImage.convert("RGB")
        droneImage.save(os.path.join(vars.noTargetDir, f"img_{count:03}.jpg"))
        count += 1

        # move down and to the right as necessary
        snapshot = shiftSnapshot(snapshot)

    print(f"time: {time.time() - start_time:.2f} seconds")


# create and place a target on the empty image
def placeTarget(image, filename, num):
    newFilename = filename[:-4] + f"_tar_{num:03}"
    image = image.convert("RGBA")

    # TODO (adam): sometimes generate a second target 30 ft away
    # TODO (adam): save seed to csv

    newTarget = True
    while newTarget:
        # create the target and choose a random location
        targetImage, targetPolygon, targetSeed = createTarget()
        targetPolygon = moveTarget(targetPolygon)

        # create yolo file for target
        yoloString = writeYolo(targetPolygon)
        with open(os.path.join(vars.targetDir, newFilename + ".yolo"), "w") as yoloFile:
            yoloFile.write(yoloString)

        # place target on image
        xMin, yMin, xMax, yMax = [int(b) for b in targetPolygon.bounds]
        image.alpha_composite(targetImage, dest=(xMin, yMin))
        
        newTarget = False

    # save image
    image = image.convert("RGB")
    image.save(os.path.join(vars.targetDir, newFilename + ".jpg"))


# write the yolo file containing the location of the target on the image
def writeYolo(polygon):
    xMin, yMin, xMax, yMax = [int(b) for b in polygon.bounds]
    targetWidth = xMax - xMin
    targetHeight = yMax - yMin

    # find centerpoint of target
    targetCenter = [int(c) for c in polygon.centroid.coords[0]]
    # print("  center:", targetCenter)

    # write yolo file in this format:
    #   0 <bbox center x> <bbox center y> <bbox width> <bbox height>
    yolo = [
        targetCenter[0] / vars.imageSizePx[0],
        targetCenter[1] / vars.imageSizePx[1],
        targetWidth / vars.imageSizePx[0],
        targetHeight / vars.imageSizePx[1]
    ]  # divide by image dimensions to scale to 1

    yoloString = "0 " + " ".join([f"{y:.8f}" for y in yolo])
    # print(f"  yolo: \"{yoloString}\"")

    return yoloString


if __name__ == "__main__":
    main()
