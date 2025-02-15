import os
import requests
from io import BytesIO
from PIL import Image
import base64

prompt = """
You are an enthusiastic and knowledgeable art expert. Your task is to analyze and discuss an artwork based on the following description:

<image_description>
{}
</image_description>

Carefully examine the description and provide an insightful analysis of the artwork. Present your analysis in an engaging and informative manner, as if you're giving a museum tour to an interested audience. Your goal is to help the listener learn about  art. Try to keep it short and concise, under 80 words. Only output what you're saying, not what you're doing.
"""

url = "https://api.anthropic.com/v1/messages"

version = "2023-06-01"

model = "claude-3-5-sonnet-20241022"

headers = {
    "x-api-key": os.environ["CLAUDE_API_KEY"],
    "content-type": "application/json",
    "anthropic-version": version,
}


def generate_description(image_path: str, metadata_text: str) -> str:

    if os.path.getsize(image_path) >= 4048227:
        with Image.open(image_path) as image_orig:
            image_orig.thumbnail((1024, 1024))
            buffered = BytesIO()
            image_orig.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
    else:
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode()

    payload = {
        "model": model,
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64,
                        },
                    },
                    {"type": "text", "text": prompt.format(metadata_text)},
                ],
            }
        ],
    }

    res = requests.post(url=url, headers=headers, json=payload)
    return res.json()["content"][0]["text"]


if __name__ == "__main__":
    text = """
    Title: Heart of the Andes
    Culture: American
    Artist: Frederic Edwin Church
    Date: 1859
    """

    root_dir = os.environ["USERPROFILE"]
    img_dir = root_dir + "/art_wallpapers"
    image_path = img_dir + "/1738396516.png"

    text = generate_description(image_path=image_path, metadata_text=text)
    print(text)
