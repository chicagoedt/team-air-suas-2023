import cv2
import os


def scaleImg(img, newWidth): 
    size = img.shape # a tuple (side1, side2, rgb)
    width = min(size[0], size[1]) # find which side is width (the smaller side)
    new_size = (int(size[1] * newWidth / width), int(size[0] * newWidth / width)) 
    scaled_img = cv2.resize(img, new_size) # scale to new_size
    return scaled_img 

def cropImage(img, width, height):
    centerCoords = (int(img.shape[1] / 2), int(img.shape[0] / 2))
    
    startRow = centerCoords[1] - int(height / 2)
    endRow = centerCoords[1] + int(height / 2)
    startCol = centerCoords[0] - int(width / 2)
    endCol = centerCoords[0] + int(width / 2)
    cropped = img[startRow:endRow, startCol:endCol]
    return cropped

def imgPreprocessing(img, newWidth): # set newWidth to 100
    # crop to only letter
    cropped = cropImage(img, 50, 50)
    croppedScale = scaleImg(cropped, newWidth)
    croppedBlur = cv2.GaussianBlur(croppedScale, (3,3), 0.5)
    croppedGray = cv2.cvtColor(croppedBlur, cv2.COLOR_BGR2GRAY)
    return croppedGray

if __name__ == "__main__":
    folder_path = '/Users/mightymanh/Desktop/myCode/myPy/team-air-suas-2023-fix-target/simulate-images/snapshots/target'
    imgName_list = [i for i in os.listdir(folder_path) if len(i) == 21]
    for img_name in imgName_list:
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        processed = imgPreprocessing(img)
        cv2.imshow('img', img)
        cv2.imshow('cropped', processed)
        cv2.waitKey(0)
