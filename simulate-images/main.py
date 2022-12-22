from PIL import Image, ImageDraw

# filename = input("what is the file path?")
filename = "runway_final.png"

# bounding_coord =
# cant have it within 4026 x 731
paper_size = [26,34]
# make image elsewere and just import them
orig_img = Image.open(filename)

orig_img.show()

