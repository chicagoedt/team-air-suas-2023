# imports
from random import randint, choice


# constants
shapes = (
    "triangle", "square", "pentagon", "hexagon", "heptagon",
    "octagon", "circle", "semicircle", "quartercircle",
    "rect", "star", "trap", "cross"
)

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


# choose a color from colors, excluding if necessary
def chooseColor(exclude=None):
    validColors = list(colors.keys())
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

    seed["shape"] = shapes[randint(0, 12)]

    if not seed["shapeColor"]:
        seed["shapeColor"] = chooseColor(exclude=seed.get("letterColor"))

    if not seed["letter"]:
        seed["letter"] = chr(randint(65, 90))

    if not seed["letterColor"]:
        seed["letterColor"] = chooseColor(exclude=seed.get("shapeColor"))

    return seed


class SimImage:
    def __init__(self, s=None):
        self.snapshot = s
        self.targets = []

    def createTarget(self, **kwargs):
        seed = generateSeed(kwargs)

        target = None

        polygon = None

        self.targets.append((target, polygon, seed))


if __name__ == "__main__":
    s = SimImage()
    s.createTarget()
    s.createTarget(shapeColor="red", letter="4")
    print(s.targets)
