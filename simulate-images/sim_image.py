# imports
import os
from random import randint, choice

from PIL import Image, ImageDraw, ImageFont
from shapely import affinity
from shapely.geometry import box


# constants
SHAPES = (
    "triangle", "square", "pentagon", "hexagon", "heptagon",
    "octagon", "circle", "semicircle", "quartercircle",
    "rect", "star", "trap", "cross"
)
SPECIAL_CASES = ["semicircle", "quartercircle",
                 "rect", "star", "trap", "cross"]
POLYGONS = ["triangle", "square", "pentagon", "hexagon", "heptagon", "octagon"]

COLORS = {
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


# choose a color from colors, excluding if necessary
def chooseColor(exclude=None):
    validColors = list(COLORS.keys())
    if exclude:
        validColors = [c for c in validColors if c != exclude]

    return choice(validColors)


# create a seed for the target with some params specified
def generateSeed(params=None) -> dict:
    seed = {
        "rotation": None,
        "shape": None,
        "shapeColor": None,
        "letter": None,
        "letterColor": None,
    }

    if params:
        for k, v in params.items():
            seed[k] = v

    if not seed["rotation"]:
        seed["rotation"] = randint(0, 359)

    seed["shape"] = SHAPES[randint(0, 12)]

    if not seed["shapeColor"]:
        seed["shapeColor"] = chooseColor(exclude=seed.get("letterColor"))

    if not seed["letter"]:
        seed["letter"] = chr(randint(65, 90))

    if not seed["letterColor"]:
        seed["letterColor"] = chooseColor(exclude=seed.get("shapeColor"))

    return seed


# draw shape on target
def drawShape(img, shape, color):
    draw = ImageDraw.Draw(img)

    if (shape == "circle"):
        draw.ellipse([0, 0, img.size], fill=COLORS[color], width=0)
    elif (shape in SPECIAL_CASES):
        with Image.open(vars.resourceDir + shape + ".bmp") as bitFile:
            scaleFactor = vars.targetSize[0] / bitFile.width
            newSize = [int(bitFile.width * scaleFactor),
                       int(bitFile.height * scaleFactor)]
            scaledBitFile = bitFile.resize(newSize)
            draw.bitmap([0, 0], scaledBitFile, fill=COLORS[color])
    else:
        draw.regular_polygon(
            [img.size[0] / 2, img.size[1] / 2, img.size[0] / 2],
            POLYGONS.index(shape) + 3,
            fill=color
        )

    return img


# draw letter on target
def drawLetter(img, letter, color):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        vars.resourceDir + "arial.ttf", int(vars.targetSize[0] / 2))

    draw.text(
        [vars.targetSize[0] / 2, vars.targetSize[1] / 2],
        letter,
        fill=COLORS[color],
        anchor="mm",
        font=font
    )

    return img


class SimImage:
    def __init__(self, s=None, f=None):
        self.snapshot = s
        self.filename = f
        self.targets = []

    def createTarget(self, **kwargs):
        seed = generateSeed(kwargs)

        # create a new image, draw shape and letter
        target = Image.new(mode="RGBA", size=vars.targetSize, color="#0000")
        target = drawShape(target, seed["shape"], seed["shapeColor"])
        target = drawLetter(target, seed["letter"], seed["letterColor"])

        # create a polygon for the target
        polygon = box(0, 0, target.size[0], target.size[1])

        # rotate the target
        target = target.rotate(
            seed["rotation"],
            expand=True,
            fillcolor="#0000"
        )

        # rotate the polygon (negative for different origin)
        polygon = affinity.rotate(polygon, -seed["rotation"])
        polygon = affinity.translate(
            polygon,
            xoff=-polygon.bounds[0],
            yoff=-polygon.bounds[1]
        )  # snap to axes

        self.targets.append({
            "target": target,
            "polygon": polygon,
            "seed": seed,
        })

    def saveImage(self):
        self.snapshot.convert("RGB") \
            .save(os.path.join(vars.targetDir, self.filename + ".jpg"))


if __name__ == "__main__":
    s = SimImage()
    s.createTarget()
    s.createTarget(shapeColor="red", letter="4")
    print(s.targets)
