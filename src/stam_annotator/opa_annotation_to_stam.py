from pathlib import Path
from typing import List, Union

from pydantic import BaseModel, Field
from stam import AnnotationStore, Selector

from stam_annotator.config import OPA_DIR
from stam_annotator.opa_annotations_loader import (
    SegmentSource,
    create_opa_annotation_instance,
)
from stam_annotator.utility import (
    get_filename_without_extension,
    get_uuid,
    save_annotation_store,
)


class AnnotationData(SegmentSource):
    offset: str


class AnnotationDataContainer(BaseModel):
    annotation_data_list: List[AnnotationData] = Field(default_factory=list)


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

        annotation_data_container = AnnotationDataContainer()
        for segment_id, offset in value.sources.items():
            for source_id, source_value in segment_data.segment_sources.items():
                if source_id == segment_id:
                    annot_data_obj = AnnotationData(
                        source_id=source_value.source_id,
                        type=source_value.type,
                        base=source_value.base,
                        lang=source_value.lang,
                        relation=source_value.relation,
                        offset=offset,
                    )

                    annotation_data_container.annotation_data_list.append(
                        annot_data_obj
                    )

        # converting to json string since this is the only format the package accepts
        annotation_value_json = annotation_data_container.model_dump_json()
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
    save_annotation_store(store, output_file_path)


if __name__ == "__main__":
    annotationstore_id = "SegmentAnnotations"
    segment_yaml_path = OPA_DIR / "36CA.yml"

    segment_annotation_pipeline(annotationstore_id, segment_yaml_path)
