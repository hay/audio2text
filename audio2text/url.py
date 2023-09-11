from . import DEFAULT_DOWNLOAD_TIMEOUT
from .file import get_tmp_file_path
from urllib.request import urlretrieve
import logging
import socket

logger = logging.getLogger(__name__)

def download_tmp_file(url):
    logger.debug(f"Setting default timeout to {DEFAULT_DOWNLOAD_TIMEOUT}s")
    socket.setdefaulttimeout(DEFAULT_DOWNLOAD_TIMEOUT)

    path = get_tmp_file_path(suffix = ".mp3")

    logger.debug(f"Downloading <{url}> to {path}")

    urlretrieve(url, path)
    return path