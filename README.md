# Overview

This script replaces your wallpaper with random art piece (and includes title, artist name and other metadata)!

Works for Windows only. Intended to run on system startup to replace wallpaper daily.

Bundled to exe with PyInstaller. Command to bundle:

`pyinstaller --noconsole --onefile --add-data="data/met_objects.json:data" --add-data="data/NotoSans-Medium.ttf:data"  main.py`

# Credits

- Thanks to Metropolitan Art Museum for provided datasets, images and API! https://metmuseum.github.io/

- Thanks to Victoria and Albert Museum for provided images and API! https://developers.vam.ac.uk/guide/v2/welcome.html
