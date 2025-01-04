import ctypes
import textwrap

from PIL import Image, ImageDraw, ImageFont

user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

def resize_image_to_screen_width(image_path, output_path):
    with Image.open(image_path) as img:
        resize_ratio = min(SCREEN_WIDTH/img.width, SCREEN_HEIGHT/img.height)
        resized_img = img.resize((int(img.width * resize_ratio), int(img.height * resize_ratio)))
    output_img = Image.new("RGB", size=(SCREEN_WIDTH, SCREEN_HEIGHT), color=(250, 245, 232))
    output_img.paste(resized_img, box=(int((SCREEN_WIDTH - resized_img.width) / 2), int((SCREEN_HEIGHT - resized_img.height) / 2)))
    output_img.save(output_path)

def create_text_rectangle(text, max_width=500, font_size=20, padding=20):
    # Try to load Arial, fallback to default font if not available
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default(font_size)

    # Calculate maximum width for text
    usable_width = max_width - (2 * padding)

    # Calculate average character width using getlength
    avg_char_width = font.getlength("x")
    chars_per_line = max(1, int(usable_width / avg_char_width))
    lines_by_charcount = textwrap.wrap(text, width=chars_per_line, break_long_words=True, replace_whitespace=False)
    lines = []
    for line in lines_by_charcount:
        lines.extend(line.split('\n'))

    # Calculate text dimensions using getbbox
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = font.getbbox(line)
        line_heights.append(bbox[3] - bbox[1] + 3)
        line_widths.append(bbox[2] - bbox[0] + 5)

    text_height = sum(line_heights)
    text_width = max(line_widths)

    # Calculate image dimensions maintaining 16:9 aspect ratio when possible
    width = min(max_width, text_width + (2 * padding))
    min_height = text_height + (2 * padding)

    # Check if 16:9 aspect ratio would make the image too tall
    aspect_height = int(width * 9 / 16)
    height = max(min_height, aspect_height)

    # Create the actual image
    img = Image.new("RGB", (width, height), color=(237, 170, 71))
    draw = ImageDraw.Draw(img)
    draw.fontmode = "L"

    # Calculate starting Y position to center text vertically
    current_y = (height - text_height) // 2

    # Draw each line of text
    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        x = 20
        draw.text((x, current_y), line, font=font, fill="black")
        current_y += line_heights[i]

    return img


def add_text_to_image(image_path, text):
    text_img = create_text_rectangle(text)
    with Image.open(image_path) as img:
        img.paste(text_img, box=(SCREEN_WIDTH - text_img.width - 200, 200))
        img.save(image_path)
