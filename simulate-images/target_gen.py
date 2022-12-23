from PIL import Image, ImageDraw, ImageFont
import random
import csv
import vars

tar_shapes = [
"circle","semicircle","quarter circle",
"triangle","square","pentagon","hexagon","heptagon","octagon",
"rectangle","trapezoid","star","cross"
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

# def gen_targets(amounts):

# seed = [random.randint(0,12),random.randint(0,9),random.randint(65,90)]
seed = [0, 1, chr(65)]
#first is selecting a random shape from tar_shape, second is random from colors, thrid is the letter
print("seed: {} {} {}".format(seed[0],seed[1], seed[2]))

img = Image.new(mode="RGB", size=vars.tar_res, color="white")
img_draw = ImageDraw.Draw(img)
img_font = ImageFont.truetype("arial.ttf", 12)
img_fp = ("./target_images/"+"{},{},{}".format(seed[0],seed[1], seed[2]))+".png"

if(seed[0] == 0):
    img_draw.ellipse([0,0,vars.tar_res[0]-1,vars.tar_res[1]-1], fill=seed[1], width=1)
    img_draw.text([vars.tar_res[0]/2,vars.tar_res[1]/2],seed[2], fill=None , anchor="mm", font=img_font)
    # img.show()

img.save(img_fp,format="PNG")

