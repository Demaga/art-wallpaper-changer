Initially, [MET API](https://metmuseum.github.io/) was used. But it lacks certain search/filter features, so maintaining a list of objects of interest that have images was a bit painful.

[Kaggle dataset](https://www.kaggle.com/datasets/metmuseum/the-met/data?select=images) contains various useful info, but is not available for download. 

So I had to turn to [GitHub](https://github.com/metmuseum/openaccess) for objects description and [Cloud Storage](https://console.cloud.google.com/marketplace/details/the-metropolitan-museum-of-art/the-met-public-domain-art-works?inv=1&invt=Abmi7Q&project=hackernews-422209) for images.

Unfortunately, not all images in dataset are available for download, so I had to filter dataset for images that are actually present in Cloud Storage now.