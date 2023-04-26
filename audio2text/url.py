from urllib.request import urlretrieve
from .file import get_tmp_file_path

def download_tmp_file(url):
    path = get_tmp_file_path(suffix = ".mp3")

    # TODO: fix logging
    print(f"Downloading <{url}> to {path}")

    urlretrieve(url, path)
    return path