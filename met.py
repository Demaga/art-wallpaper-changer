import json
import os
import random
import sys

from models import Artwork
from util import download_public_file

OBJECTS_COUNT = 377_784

if getattr(sys, "frozen", False):
    DATA_FILE_PATH = os.path.join(sys._MEIPASS, "data/met_objects.json")
else:
    DATA_FILE_PATH = "data/met_objects.json"


def get_random_art() -> Artwork:
    random_object_id = random.randint(1, 377_784)

    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == random_object_id:
                break
    data = json.loads(line)

    artwork = Artwork(
        url=data["blob_path"],
        title=data.get("title", "").strip(),
        culture=data.get("culture", "").strip(),
        period=data.get("period", "").strip(),
        artist=data.get("artist_display_name", "").strip(),
        date=data.get("object_date", "").strip(),
    )
    return artwork


def download_image(art: Artwork, image_path: str) -> None:
    """Downloads image from gcs (art.url) and saves it into image_path"""
    blob_path = art.url
    download_public_file("gcs-public-data--met", blob_path, image_path)


if __name__ == "__main__":
    print(get_random_art())
