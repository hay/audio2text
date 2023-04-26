from urllib.request import urlretrieve
from .file import get_tmp_file_path
import logging

logger = logging.getLogger(__name__)

def download_tmp_file(url):
    path = get_tmp_file_path(suffix = ".mp3")

    logger.debug(f"Downloading <{url}> to {path}")

    urlretrieve(url, path)
    return path