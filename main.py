import ctypes
import os

import requests

from met import get_random_art
from util import add_text_to_image, resize_image_to_screen_width

img_path = os.environ["USERPROFILE"] + "/tmp.jpeg"

art = get_random_art()
img_url = art["primaryImage"]
print(img_url)

res = requests.get(img_url)
with open(img_path, "wb") as f:
    f.write(res.content)


# resize image
input_image = img_path
output_image = img_path.replace("tmp", "tmp_edited")
resize_image_to_screen_width(input_image, output_image)
text = f"""Title: {art.get('title')}
Culture: {art.get('culture')}
Period: {art.get('period')}
Artist: {art.get('artistDisplayName')}
Date: {art.get('objectDate')}
"""
add_text_to_image(output_image, text)

# set wallpaper in Windows
wallpaper_path = output_image
abs_path = os.path.abspath(wallpaper_path)
ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
