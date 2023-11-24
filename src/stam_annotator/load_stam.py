from pathlib import Path
from typing import Union

import stam
from stam import AnnotationData, AnnotationDataSet, AnnotationStore

from stam_annotator.config import OPF_DIR


def load_stam_from_json(file_path: Union[str, Path]) -> AnnotationStore:
    file_path = str(file_path)
    return stam.AnnotationStore(file=file_path)


def get_annotation_data_set(store: AnnotationStore, key: str) -> AnnotationDataSet:
    for data_set in store.datasets():
        for data_set_key in data_set.keys():
            if data_set_key.__str__() == key:
                return data_set

    return None


def get_annotation_data(store: AnnotationStore, key: str, value: str) -> AnnotationData:
    data_set = get_annotation_data_set(store, key)
    for annotation_data in data_set.__iter__():
        if annotation_data.value().__str__() == value:
            return annotation_data
    return None


if __name__ == "__main__":
    file_path = OPF_DIR / "Author.json"
    store = load_stam_from_json(file_path)
    data_set = get_annotation_data_set(store, "Structure Type")
    annotation_data = get_annotation_data(store, "Structure Type", "Author")
    print(annotation_data)
    print(type(annotation_data))
    print(annotation_data.id())
