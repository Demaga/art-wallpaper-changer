import random
import time

import requests
from urllib.parse import urlencode


def get_random_art():
    object_ids = []
    for medium in ["Paintings", "Sculpture"]:
        params = {
            "q": "",
            "medium": medium,
            "hasImages": True
        }
        res = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/search?{urlencode(params)}")
        object_ids.extend(res.json()["objectIDs"])

    data = None
    i = 0
    while True and i < 5:
        obj = random.choice(object_ids)

        url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj}"
        res = requests.get(url)
        print(res.status_code)
        if res.status_code == 200 and (data := res.json()) and data.get("primaryImage"):
            print(data)
            break
        i += 1
        time.sleep(1)

    return data

if __name__=="__main__":
    print(get_random_art())
