from pathlib import Path
from typing import Union

import stam
from stam import AnnotationDataSet, Annotations, AnnotationStore

from stam_annotator.config import OPF_DIR
from stam_annotator.enums import KeyEnum, ValueEnum


def load_stam_from_json(file_path: Union[str, Path]) -> AnnotationStore:
    file_path = str(file_path)
    return stam.AnnotationStore(file=file_path)


def get_annotation_data_set(store: AnnotationStore, key: str) -> AnnotationDataSet:
    for data_set in store.datasets():
        for data_set_key in data_set.keys():
            if data_set_key == data_set.key(key):
                return data_set

    return None


def get_annotations(
    store: AnnotationStore, key: KeyEnum, value: ValueEnum
) -> Annotations:
    data_set = get_annotation_data_set(store, key.value)
    data_key = data_set.key(key.value)
    return data_set.data(filter=data_key, value=value.value).annotations()


if __name__ == "__main__":
    file_path = OPF_DIR / "Sabche.json"
    store = load_stam_from_json(file_path)

    value_instance = ValueEnum.tsawa
    key_instance = KeyEnum.structure_type
    annotations = get_annotations(store, key_instance, value_instance)
    for annotation in store.annotations():
        # get the text to which this annotation refers (if any)
        try:
            text = str(annotation)
        except stam.StamError:
            text = "n/a"
        for data in annotation:
            print(
                "\t".join((annotation.id(), data.key().id(), str(data.value()), text))
            )
