import ctypes
import textwrap
import time
import sys
import os

import requests
from google.cloud import storage
from PIL import Image, ImageDraw, ImageFont

user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)


if getattr(sys, "frozen", False):
    FONT_FILE_PATH = os.path.join(sys._MEIPASS, "data/NotoSans-Medium.ttf")
else:
    FONT_FILE_PATH = "data/NotoSans-Medium.ttf"

def resize_image_to_screen_width(image_path: str, output_path: str) -> None:
    with Image.open(image_path) as img:
        resize_ratio = min(SCREEN_WIDTH / img.width, SCREEN_HEIGHT / img.height)
        resized_img = img.resize(
            (int(img.width * resize_ratio), int(img.height * resize_ratio))
        )
    output_img = Image.new(
        "RGB", size=(SCREEN_WIDTH, SCREEN_HEIGHT), color=(250, 245, 232)
    )
    output_img.paste(
        resized_img,
        box=(
            int((SCREEN_WIDTH - resized_img.width) / 2),
            int((SCREEN_HEIGHT - resized_img.height) / 2),
        ),
    )
    output_img.save(output_path, subsampling=0, quality=100)


def create_text_rectangle(
    text: str, max_width: int = 500, font_size: int = 20, padding: int = 20
) -> Image:
    try:
        font = ImageFont.truetype(FONT_FILE_PATH, font_size)
    except Exception:
        font = ImageFont.load_default().font_variant(size=font_size)
    
    # Calculate maximum width for text
    usable_width = max_width - (2 * padding)

    # Calculate average character width using getlength
    avg_char_width = font_size * 0.6  # Approximate width of a character
    chars_per_line = int(usable_width / avg_char_width)
    
    lines_by_charcount = textwrap.wrap(
        text, width=chars_per_line, break_long_words=True, replace_whitespace=False
    )
    lines = []
    for line in lines_by_charcount:
        lines.extend(line.split("\n"))

    # Calculate text dimensions using getbbox
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = font.getbbox(line)
        line_heights.append(bbox[3] - bbox[1] + 5)
        line_widths.append(bbox[2] - bbox[0] + 5)

    text_height = sum(line_heights)
    text_width = max(line_widths)

    width = text_width + (2 * padding)
    height = text_height + (2 * padding)

    # Create the actual image
    img = Image.new("RGB", (width, height), color=(237, 170, 71))
    draw = ImageDraw.Draw(img)
    draw.fontmode = "L"

    # Calculate starting Y position to center text vertically
    current_y = (height - text_height) // 2

    # Draw each line of text
    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        draw.text((20, current_y), line, font=font, fill="black")
        current_y += line_heights[i]

    return img


def add_text_to_image(image_path: str, text: str) -> None:
    text_img = create_text_rectangle(text)
    with Image.open(image_path) as img:
        img.paste(text_img, box=(SCREEN_WIDTH - text_img.width - 200, 200))
        img.save(image_path, subsampling=0, quality=100)


def download_public_file(
    bucket_name: str, source_blob_name: str, destination_file_name: str
) -> None:
    """Downloads a public blob from the bucket."""
    download_successful = False
    retry_count = 0
    while retry_count < 3:
        try:
            storage_client = storage.Client.create_anonymous_client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
            print(
                (
                    f"Downloaded public blob {source_blob_name} from"
                    f" bucket {bucket.name} to {destination_file_name}."
                )
            )
            download_successful = True
            break
        except requests.exceptions.ConnectionError:
            # script might start execution before network service starts
            # so we have to account for that
            print("Download failed. Retrying:", retry_count + 1)
            time.sleep(3)
        retry_count += 1
    if not download_successful:
        print(
            (
                f"Failed to download public blob {source_blob_name} from"
                f" bucket {bucket.name} to {destination_file_name}."
            )
        )


def safe_get(d: dict, key: str) -> str:
    val = d.get(key)
    if not val:
        return ""
    return str(val).strip()
