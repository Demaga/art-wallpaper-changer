from google.cloud import storage


def list_available_images(bucket_name: str, allowed_extensions=["jpg"]) -> list[str]:
    """Lists all available image blobs in the public GCS bucket"""
    storage_client = storage.Client.create_anonymous_client()

    images = []
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        if blob.name.split(".")[-1] not in allowed_extensions:
            continue
        images.append(blob.name)

    return images


def save_image_blob_paths_to_file(images: list[str], file_path: str) -> None:
    with open(file_path, "w") as f:
        f.write("blob_path\n")
        for image in images:
            f.write(image + "\n")


if __name__ == "__main__":
    images = list_available_images("gcs-public-data--met")
    save_image_blob_paths_to_file(images, "available_images.csv")
