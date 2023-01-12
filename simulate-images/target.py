import random

from PIL import Image, ImageDraw, ImageFont
from shapely import affinity
from shapely.geometry import box

import vars

# constants
colors = {
    "white": (255, 255, 255),  # White
    "black": (0, 0, 0),  # Black
    "gray": (127, 127, 127),  # Gray
    "red": (255, 0, 0),  # Red
    "green": (0, 255, 0),  # Green
    "blue": (0, 0, 255),  # Blue
    "yellow": (255, 255, 0),  # Yellow
    "purple": (127, 0, 255),  # Purple
    "orange": (255, 127, 0),  # Orange
    "brown": (72, 59, 39),  # Brown
}

shapes = (
    "triangle", "square", "pentagon", "hexagon", "heptagon",
    "octagon", "circle", "semicircle", "quartercircle",
    "rect", "star", "trap", "cross"
)

special_cases = ["semicircle", "quartercircle",
                 "rect", "star", "trap", "cross"]
polygons = ["triangle", "square", "pentagon", "hexagon", "heptagon", "octagon"]


# create a rotated target image and polygon
def createTarget():
    # choose colors for shape and letter
    randColors = random.sample(list(colors.keys()), k=2)
    seed = {
        "shape": shapes[random.randint(0, 12)],
        "shapeColor": randColors[0],
        "letter": chr(random.randint(65, 90)),
        "letterColor": randColors[1],
    }

    # open a new image
    img = Image.new(mode="RGBA", size=vars.targetSize, color="#0000")
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype(
        vars.resourceDir + "arial.ttf", int(vars.targetSize[0] / 2))

    # draw the shape
    if (seed["shape"] == "circle"):
        img_draw.ellipse([0, 0, img.size],
                         fill=colors[seed["shapeColor"]], width=0)
    elif (seed["shape"] in special_cases):
        with Image.open(vars.resourceDir + seed["shape"] + ".bmp") as bitFile:
            scaleFactor = vars.targetSize[0] / bitFile.width
            newSize = [int(bitFile.width * scaleFactor),
                       int(bitFile.height * scaleFactor)]
            scaledBitFile = bitFile.resize(newSize)
            img_draw.bitmap([0, 0], scaledBitFile,
                            fill=colors[seed["shapeColor"]])
    else:
        img_draw.regular_polygon(
            [img.size[0] / 2, img.size[1] / 2, img.size[0] / 2],
            polygons.index(seed["shape"]) + 3,
            fill=seed["shapeColor"]
        )

    # draw the letter
    img_draw.text(
        [vars.targetSize[0] / 2, vars.targetSize[1] / 2],
        seed["letter"],
        fill=colors[seed["letterColor"]],
        anchor="mm",
        font=img_font
    )

    # create a polygon for the target
    polygon = box(0, 0, img.size[0], img.size[1])

    # rotate the target
    targetRotation = random.randint(0, 359)
    img = img.rotate(targetRotation, expand=True, fillcolor="#0000")

    # rotate the polygon
    # negative for different origin
    polygon = affinity.rotate(polygon, -targetRotation)
    polygon = affinity.translate(
        polygon,
        xoff=-polygon.bounds[0],
        yoff=-polygon.bounds[1]
    )  # snap to axes

    return (img, polygon)


# move the target polygon to a random location within the snapshot
def moveTarget(polygon):
    xMin, yMin, xMax, yMax = [int(b) for b in polygon.bounds]
    targetWidth = xMax - xMin
    targetHeight = yMax - yMin

    # choose random location
    offset = [
        random.randint(0, vars.imageSizePx[0] - targetWidth),
        random.randint(0, vars.imageSizePx[1] - targetHeight),
    ]  # upper left corner of target

    # move to location
    polygon = affinity.translate(polygon, xoff=offset[0], yoff=offset[1])

    return polygon
