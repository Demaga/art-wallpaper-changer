from dotenv import load_dotenv
import os
import sys


def get_env_path():
    # Get the base path of the application
    if getattr(sys, "frozen", False):
        # If the application is run as a bundle
        base_path = sys._MEIPASS
    else:
        # If the application is run from a Python interpreter
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, ".env")


load_dotenv(get_env_path())

import ctypes
from random import choice
from datetime import datetime

import met
import vam
import claude
from util import (
    add_text_to_image,
    add_description_footer_to_image,
    resize_image_to_screen_width,
)

user_dir = os.environ["USERPROFILE"]
img_dir = user_dir + "/art_wallpapers"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)


def get_latest_img() -> str | None:
    imgs = os.listdir(img_dir)
    imgs = list(filter(lambda x: "_orig" not in x, imgs))
    if len(imgs) == 0:
        return None
    return imgs[-1]


def create_wallpaper() -> str:
    img_path = img_dir + "/" + str(int(datetime.now().timestamp())) + "_orig.png"
    source = choice(["MET", "VAM"])
    if source == "MET":
        art = met.get_random_art()
        met.download_image(art, img_path)
    elif source == "VAM":
        art = vam.get_random_art()
        vam.download_image(art, img_path)

    # resize image
    edited_img_path = img_path.replace("_orig", "")
    resize_image_to_screen_width(img_path, edited_img_path)
    add_text_to_image(edited_img_path, str(art))
    description_footer = claude.generate_description(edited_img_path, str(art))
    add_description_footer_to_image(edited_img_path, description_footer)

    return edited_img_path


def set_wallpaper(wallpaper_path: str) -> None:
    # set wallpaper in Windows
    abs_path = os.path.abspath(wallpaper_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)


latest_img = get_latest_img()
if not latest_img:
    wallpaper_path = create_wallpaper()
    set_wallpaper(wallpaper_path)
    create_wallpaper()  # generate second img for future run
else:
    create_wallpaper()
