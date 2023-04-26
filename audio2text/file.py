from . import TMP_FILE_FOLDER
from pathlib import Path
from shortuuid import uuid

def get_tmp_file_path(suffix = ""):
    filename = uuid()

    if suffix:
        filename = filename + suffix

    return Path(TMP_FILE_FOLDER) / filename