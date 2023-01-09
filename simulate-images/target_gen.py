from PIL import Image, ImageDraw, ImageFont, ImageColor
import random
import csv
import vars

special_case_dir = "special_imgs/"

tar_shapes = [
"triangle","square","pentagon","hexagon","heptagon","octagon",
"circle",
"semicircle","quartercircle","rectangle","star","trap","cross"
]

tar_colors=[
    [255,255,255], #White
    [0,0,0], #Black
    [127,127,127], #Gray
    [255,0,0], #Red
    [0,255,0], #Green
    [0,0,255], #Blue
    [255,255,0], #Yellow
    [127,0,255], #Purple
    [255,127,0], #Orange
    [72, 59, 39],  #Brown
]

tar_colors_names=[
    "White"
    , "Black"
    , "Gray"
    , "Red"
    , "Green"
    , "Blue"
    , "Yellow"
    , "Purple"
    , "Orange"
    , "Brown"
]
def gen_targets(amount):
    for x in range(amount):
        rand_color = random.sample(range(10), k=2)
        seed = [random.randint(0,12),rand_color[0],chr(random.randint(65,90)), rand_color[1]]
        # seed = [6, 4, chr(65), 0]
        #first is selecting a random shape from tar_shape, second is random from colors, thrid is the letter, 4 is rotation
        print("seed: {} {} {} {}".format(seed[0],seed[1], seed[2], seed[3]))

        img = Image.new(mode="RGBA", size=vars.tar_res, color="white")
        img_draw = ImageDraw.Draw(img)
        img_font = ImageFont.truetype("special_imgs/arial.ttf", 12)
        img_fp = ("./target_images/"+"{},{},{},{}".format(tar_shapes[seed[0]], tar_colors_names[seed[1]], seed[2],tar_colors_names[seed[3]]))+".png"
        # print(tar_colors[seed[1]])
        # print(ImageColor.getcolor([0,0,255],"RGBA"))

        if(seed[0] == 6):
            img_draw.ellipse([0,0,img.size], fill=tar_colors_names[seed[1]], width=0)
        if(seed[0] > 6):
            special_cases = ["semicircle.bmp",
            "quartercircle.bmp",
            "rect.bmp",
            "star.bmp",
            "trap.bmp",
            "cross.bmp"
            ]
            bit_file = Image.open(special_case_dir+(special_cases[seed[0]-7]))
            img_draw.bitmap([0,0],bit_file, fill=tar_colors_names[seed[1]])
        if(seed[0] <= 5):
            img_draw.regular_polygon([img.size[0]/2,img.size[1]/2,img.size[0]/2], seed[0]+3, fill=tar_colors_names[seed[1]])

        # img.show()
        # im = img.rotate(seed[3], fillcolor=(0,0,0,0),expand=True)
        im_draw = ImageDraw.Draw(img)
        # print("pog")
        im_draw.text([vars.tar_res[0]/2,vars.tar_res[1]/2],seed[2], fill=tar_colors_names[seed[3]] , anchor="mm", font=img_font)
        # img.show()
        img.save(img_fp,format="PNG")
    return

# gen_targets(10)