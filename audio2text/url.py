from urllib.request import urlretrieve
from .file import get_tmp_file_path
import logging
import requests

logger = logging.getLogger(__name__)

def download_tmp_file(url):
    path = get_tmp_file_path(suffix = ".mp3")

    logger.debug(f"Downloading <{url}> to {path}")
    requests.get(url, timeout=60)
    urlretrieve(url, path)
    return path
