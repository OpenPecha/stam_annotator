from pathlib import Path
from typing import Union

from stam import AnnotationStore, Offset, Selector

from stam_annotator.config import OPF_DIR
from stam_annotator.load_yaml_annotations import load_opf_annotations_from_yaml
from stam_annotator.opf_annotations_loader import create_opf_annotation_instance
from stam_annotator.utility import (
    get_filename_without_extension,
    get_uuid,
    save_annotation_store,
)


def create_annotationstore(id: str):
    return AnnotationStore(id=id)


def create_resource(store: AnnotationStore, text_file_path: Path):
    text = text_file_path.read_text(encoding="utf-8")
    resource_id = get_filename_without_extension(text_file_path)
    return store.add_resource(id=resource_id, text=text)


def create_dataset(store: AnnotationStore, id: str, key: str):
    dataset = store.add_dataset(id=id)
    dataset.add_key(key)
    return dataset


def create_annotation(store: AnnotationStore, id: str, target: Selector, data: dict):
    return store.annotate(id=id, target=target, data=data)


def annotation_pipeline(
    annotationstore_id: str,
    text_file_path: Union[str, Path],
    annotation_yaml_path: Union[str, Path],
    dataset_key: str,
) -> None:
    # Create annotation store
    store = create_annotationstore(id=annotationstore_id)
    # Create resource
    resource = create_resource(store=store, text_file_path=Path(text_file_path))
    # Create dataset
    yaml_data = load_opf_annotations_from_yaml(Path(annotation_yaml_path))
    annotation_doc = create_opf_annotation_instance(yaml_data)

    dataset = create_dataset(store=store, id=annotation_doc.id, key=dataset_key)

    unique_uuid = get_uuid()
    # Create annotation
    for id, value in annotation_doc.annotations.items():

        data = dataset.add_data(
            dataset_key, annotation_doc.annotation_type, unique_uuid
        )
        create_annotation(
            store=store,
            id=id,
            target=Selector.textselector(
                resource, Offset.simple(value.span.start, value.span.end)
            ),
            data=data,
        )

    output_file_name = get_filename_without_extension(annotation_yaml_path)
    output_file_path = OPF_DIR / f"{output_file_name}.json"
    save_annotation_store(store, output_file_path)


if __name__ == "__main__":
    # Define your file paths and other parameters
    annotationstore_id = "P000218_Volume_1"
    text_file_path = OPF_DIR / "v001.txt"
    annotation_yaml_path = OPF_DIR / "Quotation.yml"
    dataset_key = "Structure Type"

    # Run the pipeline
    annotation_pipeline(
        annotationstore_id, text_file_path, annotation_yaml_path, dataset_key
    )
