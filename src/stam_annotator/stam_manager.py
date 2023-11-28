from pathlib import Path
from typing import Union

import stam
from stam import AnnotationDataSet, Annotations, AnnotationStore

from stam_annotator.config import OPF_DIR
from stam_annotator.enums import KeyEnum, ValueEnum
from stam_annotator.utility import save_annotation_store


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


def combine_stam(stam1: AnnotationStore, stam2: AnnotationStore) -> AnnotationStore:

    """
    In this function, all the resources, data set and annotations are being transfered from
    stam2 to stam1.
    """
    # transfer resources
    for resource in stam2.resources():
        stam1.add_resource(id=resource.id(), text=resource.text())

    # transfer datasets
    for dataset in stam2.datasets():
        key = next(dataset.keys(), None)
        if not key:
            continue
        # if the data set already exists
        if get_annotation_data_set(stam1, key.id()):
            continue

        new_dataset = stam1.add_dataset(id=dataset.id())
        new_dataset.add_key(key.id())

    # transfer annotations
    for annotation in stam2.annotations():
        annotation_data = next(annotation.__iter__(), None)
        if not annotation_data:
            continue

        """
        if the associated data set already exists, then data_set_id of already existing is used
        with annotation,
        else data set id of new is used.

        """

        annotation_data_key = annotation_data.key().id()
        data_set = get_annotation_data_set(stam1, annotation_data_key)
        data_set_id = data_set.id() if data_set else annotation_data.dataset().id()

        data = {
            "id": annotation_data.id(),
            "key": annotation_data_key,
            "value": annotation_data.value().get(),
            "set": data_set_id,
        }
        stam1.annotate(id=annotation.id(), target=annotation.select(), data=data)
    return stam1


if __name__ == "__main__":
    file_path = OPF_DIR / "Author.json"
    stam1 = load_stam_from_json(file_path)
    file_path = OPF_DIR / "Sabche.json"
    stam2 = load_stam_from_json(file_path)
    stam3 = combine_stam(stam1, stam2)
    save_annotation_store(stam3, OPF_DIR / "combined.json")
