###########  README ####################
# This file contains constants that are used within the code.
# It is made to achieve easy adjustments during the competition.
# Use this to fine tune the image processing and other settings so that the
# targets are easily readable.

########### IMPORTANT DETAILS (2023) #################

# Valid shapes for the standard object include:
#       circle, semicircle, quarter circle,
#       triangle, square, rectangle,
#       trapezoid, pentagon, hexagon,
#       heptagon, octagon, star, and cross.

# Valid colors include:
#       white, black, gray, red,
#       blue, green, yellow,
#       purple, brown, and orange.

################################################

# Color ranges
# Location: ShapeDetector.py
# todo: identify valid range of colors and update this list
WHITE = 0
BLACK = 0
GRAY = 0
RED = 0
BLUE = 0
GREEN = 0
YELLOW = 0
PURPLE = 0
BROWN = 0
ORANGE = 0

# Blur sensitivity settings
# Location: ShapeDetector.py
BLUR_KERNEL = (9, 9)  # strong
BLUR_SIGMA = 10


