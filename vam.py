import requests

from models import Artwork


def get_random_art() -> Artwork:
    req = requests.get("https://api.vam.ac.uk/v2/objects/search?random=1")
    records = req.json()["records"]

    url_template = (
        "https://framemark.vam.ac.uk/collections/{img_id}/full/full/0/default.jpg"
    )

    artwork = None
    for data in records:
        img_id = data.get("_primaryImageId")
        if not img_id:
            continue

        artist = data.get("_primaryMaker")
        if artist:
            artist = artist["name"]
        artwork = Artwork(
            url=url_template.format(img_id=img_id),
            title=data.get("_primaryTitle", "").strip(),
            date=data.get("_primaryDate", "").strip(),
            artist=artist,
        )
    return artwork


def download_image(art: Artwork, image_path: str) -> None:
    res = requests.get(art.url)
    with open(image_path, "wb") as f:
        f.write(res.content)


if __name__ == "__main__":
    art = get_random_art()
    print(art)
    download_image(art, "./vam.jpg")
