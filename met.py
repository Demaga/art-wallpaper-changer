import json
import os
import random
import sys

from util import download_public_file

OBJECTS_COUNT = 377_784

if getattr(sys, "frozen", False):
    DATA_FILE_PATH = os.path.join(sys._MEIPASS, "data/met_objects.json")
else:
    DATA_FILE_PATH = "data/met_objects.json"


def get_random_art():
    random_object_id = random.randint(1, 377_784)

    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == random_object_id:
                break
    data = json.loads(line)
    return data


def download_image(art, image_path):
    blob_path = art["blob_path"]
    download_public_file("gcs-public-data--met", blob_path, image_path)


if __name__ == "__main__":
    print(get_random_art())
