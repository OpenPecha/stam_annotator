from pathlib import Path
from uuid import uuid4


def get_filename_without_extension(file_path):
    return Path(file_path).stem


def get_uuid():
    return uuid4().hex
