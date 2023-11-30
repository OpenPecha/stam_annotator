import json
from pathlib import Path
from typing import Dict, Union
from uuid import uuid4

from stam import AnnotationStore


def get_filename_without_extension(file_path: Union[str, Path]):
    return Path(file_path).stem


def is_json_file_path(file_path: Path) -> bool:
    return file_path.suffix == ".json"


def get_uuid():
    return uuid4().hex


def save_annotation_store(store: AnnotationStore, output_file_path: Union[str, Path]):
    output_file_path = Path(output_file_path)

    # Check if the file extension is .json
    if not is_json_file_path(output_file_path):
        raise ValueError(
            f"The file path must lead to a JSON file. Given: {output_file_path}"
        )

    store.set_filename(str(output_file_path))
    store.save()


def save_json_file(data: Dict, output_file_path: Union[str, Path]):
    output_file_path = Path(output_file_path)

    # Check if the file extension is .json
    if not is_json_file_path(output_file_path):
        raise ValueError(
            f"The file path must lead to a JSON file. Given: {output_file_path}"
        )

    with open(output_file_path, "w") as f:
        json.dump(data, f, indent=4)
