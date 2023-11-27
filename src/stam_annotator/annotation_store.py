from typing import List

from pydantic import BaseModel, Field, field_validator

from stam_annotator.config import OPF_DIR
from stam_annotator.load_stam import KeyEnum
from stam_annotator.load_yaml_annotations import load_opf_annotations_from_yaml
from stam_annotator.opf_annotations_loader import (
    OpfAnnotation,
    Span,
    create_opf_annotation_instance,
)
from stam_annotator.utility import get_uuid


class Annotation(BaseModel):
    annotation_id: str
    span: Span


class Annotation_Data_Set(BaseModel):
    data_set_id: str
    key: KeyEnum

    @field_validator("data_set_id", mode="before")
    @classmethod
    def set_id(cls, v):
        return v or get_uuid()


class Resource(BaseModel):
    resource_id: str
    text: str


class Annotation_Store(BaseModel):
    store_id: str
    datasets: List[Annotation_Data_Set] = Field(default_factory=list)
    resources: List[Resource] = Field(default_factory=list)
    annotations: List[Annotation] = Field(default_factory=list)

    @field_validator("store_id", mode="before")
    @classmethod
    def set_id(cls, v):
        return v or get_uuid()

    def add_data_set(self, data_set: Annotation_Data_Set):
        self.datasets.append(data_set)

    def add_annotation(self, annotation_id: str, span: Span):
        self.annotations.append(Annotation(annotation_id=annotation_id, span=span))


def create_data_set(data_set_id: str, key: KeyEnum):
    return Annotation_Data_Set(data_set_id=data_set_id, key=key)


def opf_annotation_to_stam_model(
    opf_annot: OpfAnnotation, data_set_key: KeyEnum
) -> Annotation_Store:
    annotation_store = Annotation_Store(store_id=get_uuid())
    data_set = create_data_set(data_set_id=opf_annot.id, key=data_set_key)
    annotation_store.add_data_set(data_set)

    for id, annotation in opf_annot.annotations.items():
        # create annotation data
        annotation_store.add_annotation(annotation_id=id, span=annotation.span)

    return annotation_store


if __name__ == "__main__":
    segment_yaml_path = OPF_DIR / "Sabche.yml"
    opf_data_dict = load_opf_annotations_from_yaml(segment_yaml_path)

    opf_obj = create_opf_annotation_instance(opf_data_dict)
    data_set_key = KeyEnum.structure_type
    stam_model = opf_annotation_to_stam_model(opf_obj, data_set_key)
    print(stam_model)
