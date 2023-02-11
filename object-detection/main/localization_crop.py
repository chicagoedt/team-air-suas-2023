import localization_ShapeDetector as SD
import cv2
import os

# crop img
def cropImage(img, foundCoords, width, height):
    startRow = foundCoords[1] - int(height / 2)
    endRow = foundCoords[1] + int(height / 2)
    startCol = foundCoords[0] - int(width / 2)
    endCol = foundCoords[0] + int(width / 2)
    cropped = img[startRow:endRow, startCol:endCol]
    return cropped

# crop all images in src_folder, save them in dest_folder
def cropFolder(src_folder, dest_folder, width, height):
    # clear dest_folder first
    oldFiles = os.listdir(dest_folder)
    if len(oldFiles) != 0:
        for file in oldFiles:
            os.remove(os.path.join(dest_folder, file))

    # crop folder
    images = os.listdir(src_folder)
    fails = []
    return_map = {}
    for image in images:
        print('Cropping image:', image)
        img_path = os.path.join(src_folder, image)
        try:
            img = cv2.imread(img_path)
            _, foundCoords, _ = SD.findShape(img)
            cropped = cropImage(img, foundCoords, 100, 100)
            croppedName = image[:-4] + '_' + str(foundCoords[0]) + '_' + str(foundCoords[1]) + '.jpg'
            croppedPath = os.path.join(dest_folder, croppedName)
            cv2.imwrite(croppedPath, cropped)

        except:
            print('Something is wrong with ShapeDetector???')
            fails.append(image)
            continue
    
    print('Done cropping! Number of files failed:', len(fails))
    print('Number of files cropped:', len(images) - len(fails))



    


    

