import json
from pathlib import Path
from typing import Union

from stam import AnnotationStore, Selector

from stam_annotator.config import OPA_DIR
from stam_annotator.opa_annotations_loader import create_opa_annotation_instance
from stam_annotator.utility import get_filename_without_extension, get_uuid


def create_annotationstore(id: str):
    return AnnotationStore(id=id)


def create_resource(store: AnnotationStore, id: str, filename: str):
    return store.add_resource(id=id, filename=filename)


def create_dataset(store: AnnotationStore, id: str, key: str):
    dataset = store.add_dataset(id=id)
    dataset.add_key(key)
    return dataset


def create_annotation(store: AnnotationStore, id: str, target: Selector, data: dict):
    return store.annotate(id=id, target=target, data=data)


def segment_annotation_pipeline(
    annotationstore_id: str, segment_yaml_path: Union[str, Path]
) -> None:
    # Create annotation store
    store = create_annotationstore(id=annotationstore_id)

    # Load segment data
    segment_data = create_opa_annotation_instance(Path(segment_yaml_path))

    dataset = store.add_dataset(id="dataset")
    first_key = next(iter(segment_data.segment_sources))
    dataset.add_key(segment_data.segment_sources[first_key].type)

    # Create annotation
    for uuid, value in segment_data.segment_pairs.items():
        key = "translation"

        annotation_value = []
        for segment_id, segment_value in value.sources.items():
            for source_id, source_value in segment_data.segment_sources.items():
                if source_id == segment_id:
                    value_dict = {
                        "base": source_value.base,
                        "lang": source_value.lang,
                        "relation": source_value.relation,
                        "source_id": source_id,
                        "type": source_value.type,
                        "offset": segment_value,
                    }

                    annotation_value.append(value_dict)

        # converting to json string since this is the only format the package accepts
        annotation_value_json = json.dumps(annotation_value)
        # Add data to dataset
        data = dataset.add_data(key, annotation_value_json, get_uuid())

        create_annotation(
            store=store,
            id=uuid,
            target=Selector.datasetselector(store.dataset("dataset")),
            data=data,
        )
    # Save the store
    output_file_name = get_filename_without_extension(segment_yaml_path)
    output_file_path = Path(segment_yaml_path).parent / f"{output_file_name}.json"
    store.set_filename(str(output_file_path))
    store.save()


if __name__ == "__main__":
    annotationstore_id = "SegmentAnnotations"
    segment_yaml_path = OPA_DIR / "36CA.yml"

    segment_annotation_pipeline(annotationstore_id, segment_yaml_path)
