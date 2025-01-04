import ctypes
import os
import random

import requests
from PIL import Image

from met import get_random_art
from util import add_text_to_image, resize_image_to_screen_width

art = get_random_art()
img_url = art["primaryImage"]
print(img_url)

res = requests.get(img_url)
with open("tmp.jpeg", "wb") as f:
    f.write(res.content)


# resize image
input_image = "./tmp.jpeg"
output_image = "./tmp_edited.jpeg"
resize_image_to_screen_width(input_image, output_image)
text = f"""Title: {art.get('title')}
Culture: {art.get('culture')}
Period: {art.get('period')}
Artist: {art.get('artistDisplayName')}
Date: {art.get('objectDate')}
"""
add_text_to_image(output_image, text)

# set wallpaper in Windows
wallpaper_path = "./tmp_edited.jpeg"
abs_path = os.path.abspath(wallpaper_path)
ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
