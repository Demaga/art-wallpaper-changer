import os
import ctypes

user_dir = os.environ["USERPROFILE"]
img_dir = user_dir + "/art_wallpapers"

imgs = os.listdir(img_dir)
imgs = list(filter(lambda x: "_orig" not in x, imgs))

latest_img = imgs[-1]
abs_path = os.path.abspath(img_dir + "/" + latest_img)
ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
