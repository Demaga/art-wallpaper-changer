import ctypes
import os

from met import download_image, get_random_art
from util import add_text_to_image, resize_image_to_screen_width

img_path = os.environ["USERPROFILE"] + "/tmp.png"

art = get_random_art()
download_image(art, img_path)

# resize image
input_image = img_path
output_image = img_path.replace("tmp", "tmp_edited")
resize_image_to_screen_width(input_image, output_image)
text = f"Title: {art.get('title')}"
if culture := art.get("culture"):
    text += f"\nCulture: {culture}"
if period := art.get("period"):
    text += f"\nPeriod: {period}"
if artist := art.get("artist_display_name"):
    text += f"\nArtist: {artist}"
if date := art.get("object_date"):
    text += f"\nDate: {date}"
add_text_to_image(output_image, text)

# set wallpaper in Windows
wallpaper_path = output_image
abs_path = os.path.abspath(wallpaper_path)
ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
