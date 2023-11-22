from pathlib import Path
from typing import Union

import stam
from stam import AnnotationStore

from stam_annotator.config import OPF_DIR


def load_stam_from_json(file_path: Union[str, Path]) -> AnnotationStore:
    file_path = str(file_path)
    return stam.AnnotationStore(file=file_path)


if __name__ == "__main__":
    file_path = OPF_DIR / "Author.json"
    store = load_stam_from_json(file_path)
