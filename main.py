import ctypes
import os
from random import choice
from datetime import datetime

import met
import vam
from util import add_text_to_image, resize_image_to_screen_width


root_dir = os.environ["USERPROFILE"]
img_dir = root_dir + "/art_wallpapers"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)


def get_latest_img() -> str | None:
    imgs = os.listdir(img_dir)
    if len(imgs) == 0:
        return None
    imgs.sort()
    return imgs[-1]


def create_wallpaper() -> str:
    img_path = img_dir + "/" + str(int(datetime.now().timestamp())) + ".png"
    source = choice(["MET", "VAM"])
    if source == "MET":
        art = met.get_random_art()
        met.download_image(art, img_path)
    elif source == "VAM":
        art = vam.get_random_art()
        vam.download_image(art, img_path)

    # resize image
    edited_img_path = img_path.replace("tmp", "tmp_edited")
    resize_image_to_screen_width(img_path, edited_img_path)
    add_text_to_image(edited_img_path, str(art))

    return edited_img_path


def set_wallpaper(wallpaper_path: str) -> None:
    # set wallpaper in Windows
    abs_path = os.path.abspath(wallpaper_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)


latest_img = get_latest_img()
print(latest_img)
if not latest_img:
    wallpaper_path = create_wallpaper()
    set_wallpaper(wallpaper_path)
    create_wallpaper() # generate second img for future run
else:
    set_wallpaper(img_dir + "/" + latest_img)
    create_wallpaper()
