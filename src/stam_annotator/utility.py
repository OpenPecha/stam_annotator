from pathlib import Path
from typing import Union
from uuid import uuid4

from stam import AnnotationStore


def get_filename_without_extension(file_path):
    return Path(file_path).stem


def get_uuid():
    return uuid4().hex


def save_annotation_store(store: AnnotationStore, output_file_path: Union[str, Path]):
    output_file_path = Path(output_file_path)

    # Check if the file extension is .json
    if output_file_path.suffix != ".json":
        raise ValueError(
            f"The file path must lead to a JSON file. Given: {output_file_path}"
        )

    store.set_filename(str(output_file_path))
    store.save()
