from pathlib import Path
from typing import List, Sequence, Union

import stam
from stam import AnnotationDataSet, Annotations, AnnotationStore

from stam_annotator.definations import (
    OPA_DIR,
    OPF_BO_DIR,
    OPF_EN_DIR,
    KeyEnum,
    ValueEnum,
)
from stam_annotator.opa_loader import OpaAnnotation, create_opa_annotation_from_json
from stam_annotator.utility import convert_opf_stam_annotation_to_dictionary


def load_stam_from_json(file_path: Union[str, Path]) -> AnnotationStore:
    file_path = str(file_path)
    return stam.AnnotationStore(file=file_path)


def load_multiple_stam_from_json(
    file_paths: Sequence[Union[str, Path]]
) -> List[AnnotationStore]:
    return [load_stam_from_json(file_path) for file_path in file_paths]


def get_annotation_data_set(store: AnnotationStore, key: str) -> AnnotationDataSet:
    for data_set in store.datasets():
        for data_set_key in data_set.keys():
            if data_set_key == data_set.key(key):
                return data_set

    return None


def get_annotations(
    store: AnnotationStore, key: KeyEnum, value: ValueEnum, include_payload: bool = True
) -> Annotations:
    data_set = get_annotation_data_set(store, key.value)
    data_key = data_set.key(key.value)
    annotations = data_set.data(filter=data_key, value=value.value).annotations()
    return convert_opf_stam_annotation_to_dictionary(annotations, include_payload)


def combine_stams(stams: List[AnnotationStore]) -> AnnotationStore:
    """
    This function combines multiple stams into one.
    It requires at least two STAM objects in the list to proceed.
    """
    if len(stams) < 2:
        raise ValueError("At least two STAM objects are required.")

    stam1 = stams[0]
    for stam2 in stams[1:]:
        stam1 = combine_two_stam(stam1, stam2)
    return stam1


def combine_two_stam(stam1: AnnotationStore, stam2: AnnotationStore) -> AnnotationStore:

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


def get_alignment_annotations(
    opa_alignment: OpaAnnotation,
    opf_annotations: List[AnnotationStore],
):
    """
    This function returns the annotations of the given key and value from the alignment
    annotation store.
    """
    alignment_sources = list(opa_alignment.segment_sources.keys())
    for segment_id, segment in opa_alignment.segment_pairs.items():
        # Get if all the sources are present in the segment
        if not all(source in segment for source in alignment_sources):
            raise ValueError("The alignment is not complete.")
            break

        # get the annotation
        for source_id, segment_offset in segment.items():
            for opf_annot in opf_annotations:
                try:
                    if opf_annot.annotation(segment_offset):
                        print(opf_annot.annotation(segment_offset))
                        break
                except:  # noqa
                    pass


if __name__ == "__main__":
    opa_annot = create_opa_annotation_from_json(OPA_DIR / "36CA.json")
    bo_opf = load_stam_from_json(OPF_BO_DIR / "Segment.json")
    en_opf = load_stam_from_json(OPF_EN_DIR / "Segment.json")

    get_alignment_annotations(opa_annot, [bo_opf, en_opf])
