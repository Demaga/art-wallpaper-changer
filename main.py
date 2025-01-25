import ctypes
import os
from random import choice

import met
import vam
from util import add_text_to_image, resize_image_to_screen_width

img_path = os.environ["USERPROFILE"] + "/tmp.png"

source = choice(["MET", "VAM"])
if source == "MET":
    art = met.get_random_art()
    met.download_image(art, img_path)
elif source == "VAM":
    art = vam.get_random_art()
    vam.download_image(art, img_path)


# resize image
input_image = img_path
output_image = img_path.replace("tmp", "tmp_edited")
resize_image_to_screen_width(input_image, output_image)
add_text_to_image(output_image, str(art))

# set wallpaper in Windows
wallpaper_path = output_image
abs_path = os.path.abspath(wallpaper_path)
ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
