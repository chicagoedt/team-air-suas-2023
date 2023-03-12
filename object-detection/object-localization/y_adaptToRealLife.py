import cv2
import y_imgPreprocessing as prepr
import numpy as np

# stdSize = 130, stdScaledWidth = 130, stdCropSize = 60
def getScaleAndCrop(img_path, stdSize, stdScaledWidth, stdCropSize):
    img = cv2.imread(img_path)
    height = img.shape[0]
    width = img.shape[1]
    print(f'height: {height}, width: {width}')
    averageSize = int((height + width) / 2)
    cropSize = int(stdCropSize * averageSize / stdSize)
    scaledWidth = int(stdScaledWidth * averageSize / stdSize)

    # special case
    if cropSize < stdCropSize:
        cropSize = stdCropSize
    if scaledWidth < stdScaledWidth:
        scaledWidth = stdScaledWidth
    print(f'cropSize: {cropSize}, scaledWidth: {scaledWidth}')
    return scaledWidth, cropSize

# function that changes brightness and contrast level of an img
# borrow from Stack overflow, similar to what GIMP does
# input value for brightness and contrast should be in range -127 to 127, including both ends
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

# get light level of background img
def measureBackgroundLightLevel(img):
    imgScaled = prepr.scaleImg(img, 30)
    height = imgScaled.shape[0]
    width = imgScaled.shape[1]
    numPixel = height * width

    # sum all pixels and get average
    sumB = 0
    sumG = 0
    sumR = 0
    for y in range(height):
        for x in range(width):
            sumB += imgScaled[y][x][0]
            sumG += imgScaled[y][x][1]
            sumR += imgScaled[y][x][2]
    
    averageColor = np.array([[[int(sumB / numPixel), int(sumG / numPixel), int(sumR / numPixel)]]], dtype = np.uint8)
    averageColorHSV = cv2.cvtColor(averageColor, cv2.COLOR_BGR2HSV)
    
    # light level of the average is the V value
    lightLevel = averageColorHSV[0][0][2]
    
    # show output
    print('average color:', averageColor)
    print('light level:', lightLevel)
    return lightLevel

# get light level of target img
def measureTargetLightLevel(img):
    print(img.shape)
    height = img.shape[0]
    width = img.shape[1]
    numPixel = height + width - 1

    # sum pixels in first row and first column, get average
    sumB = 0
    sumG = 0
    sumR = 0
    for y in range(height):
        print(y)
        sumB += img[y][0][0] #+ img[y][width - 1][0]
        sumG += img[y][0][1] #+ img[y][width - 1][1]
        sumR += img[y][0][2] #+ img[y][width - 1][2]

    for x in range(1, width):
        print(x)
        sumB += img[0][x][0]
        sumG += img[0][x][1]
        sumR += img[0][x][2]
    
    averageColor = np.array([[[int(sumB / numPixel), int(sumG / numPixel), int(sumR / numPixel)]]], dtype = np.uint8)
    averageColorHSV = cv2.cvtColor(averageColor, cv2.COLOR_BGR2HSV)
    
    # light level is the V value of average HSV pixel
    lightLevel = averageColorHSV[0][0][2]

    # show output
    print('average color:', averageColor)
    print('light level:', lightLevel)

    return lightLevel


