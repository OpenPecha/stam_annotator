from pathlib import Path


def get_filename_without_extension(file_path):
    return Path(file_path).stem
