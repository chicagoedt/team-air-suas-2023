from y_color import *

# check if hsv is in range input lower and input upper
def hsvInRangeSingle(hsv, lower, upper):
    if lower[0] > hsv[0] or hsv[0] > upper[0]:
        return False
    if lower[1] > hsv[1] or hsv[1] > upper[1]:
        return False
    if lower[2] > hsv[2] or hsv[2] > upper[2]:
        return False
    return True

# check if hsv is in range any input lower and upper
def hsvInRangeArray(hsv, lower_array, upper_array):
    lenArray = len(lower_array)
    for i in range(lenArray):
        if hsvInRangeSingle(hsv, lower_array[i], upper_array[i]):
            return True
            
    return False    
    

# get the color name that best match with input hsv
def getColorOfPixel(hsv):
    # white
    
    # black
    if hsvInRangeArray(hsv, lowerBlack_array, upperBlack_array):
        return 'Black'
    
    # gray

    # red
    if hsvInRangeArray(hsv, lowerRed_array, upperRed_array):
        return 'Red'
    
    # blue
    if hsvInRangeArray(hsv, lowerBlue_array, upperBlue_array):
        return 'Blue'
    
    # green
    if hsvInRangeArray(hsv, lowerGreen_array, upperGreen_array):
        return 'Green'
    
    # yellow
    if hsvInRangeArray(hsv, lowerYellow_array, upperYellow_array):
        return 'Yellow'

    # purple
    if hsvInRangeArray(hsv, lowerPurple_array, upperPurple_array):
        return 'Purple'

    # brown

    # orange
    if hsvInRangeArray(hsv, lowerOrange_array, upperOrange_array):
        return 'Orange'
    
    return None