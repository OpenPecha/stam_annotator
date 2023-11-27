from typing import List

from pydantic import BaseModel, Field, field_validator

from stam_annotator.config import OPF_DIR
from stam_annotator.enums import KeyEnum, ValueEnum
from stam_annotator.load_yaml_annotations import load_opf_annotations_from_yaml
from stam_annotator.opf_annotations_loader import (
    OpfAnnotation,
    Span,
    create_opf_annotation_instance,
)
from stam_annotator.utility import get_uuid


class Annotation_Data(BaseModel):
    annotation_data_id: str
    annotation_data_key: KeyEnum
    annotation_data_value: ValueEnum

    store_id: str


class Annotation(BaseModel):
    annotation_id: str
    span: Span
    annotation_data: Annotation_Data


class Annotation_Data_Set(BaseModel):
    data_set_id: str
    data_set_key: KeyEnum
    annotation_datas: List[Annotation_Data] = Field(default_factory=list)

    @field_validator("data_set_id", mode="before")
    @classmethod
    def set_id(cls, v):
        return v or get_uuid()

    @field_validator("annotation_datas")
    @classmethod
    def annotation_data_key_must_equal_to_data_set_key(cls, annotation_data, values):
        if (
            "data_set_key" in values
            and annotation_data.annotation_data_key != values["key"]
        ):
            raise ValueError("annotation_data_key must match data_set_key")
        return annotation_data

    def add_annotation_data(self, annotation_data: Annotation_Data):
        if annotation_data not in self.annotation_datas:
            self.annotation_datas.append(annotation_data)


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

    def add_annotation(self, annotation: Annotation):
        self.annotations.append(annotation)


def create_data_set(data_set_id: str, data_set_key: KeyEnum):
    return Annotation_Data_Set(data_set_id=data_set_id, data_set_key=data_set_key)


def create_annotation(annotation_id: str, span: Span, annotation_data: Annotation_Data):
    return Annotation(
        annotation_id=annotation_id, span=span, annotation_data=annotation_data
    )


def add_annotation_data_to_data_set(
    data_set: Annotation_Data_Set, annotation_data: Annotation_Data
):
    if annotation_data not in data_set.annotation_datas:
        data_set.annotation_datas.append(annotation_data)


def opf_annotation_to_annotation_store_format(
    opf_annot: OpfAnnotation, data_set_key: KeyEnum
) -> Annotation_Store:
    store_id = get_uuid()
    annotation_store = Annotation_Store(store_id=store_id)
    data_set = create_data_set(data_set_id=opf_annot.id, data_set_key=data_set_key)
    annotation_store.add_data_set(data_set)

    annotation_data = Annotation_Data(
        annotation_data_id=get_uuid(),
        annotation_data_key=data_set_key,
        annotation_data_value=opf_annot.annotation_type,
        store_id=store_id,
    )
    for id, annotation in opf_annot.annotations.items():
        add_annotation_data_to_data_set(data_set, annotation_data)
        annotation = create_annotation(
            annotation_id=id, span=annotation.span, annotation_data=annotation_data
        )
        annotation_store.add_annotation(annotation)

    return annotation_store


if __name__ == "__main__":
    segment_yaml_path = OPF_DIR / "Sabche.yml"
    opf_data_dict = load_opf_annotations_from_yaml(segment_yaml_path)

    opf_obj = create_opf_annotation_instance(opf_data_dict)
    data_set_key = KeyEnum.structure_type
    stam_model = opf_annotation_to_annotation_store_format(opf_obj, data_set_key)
    print(stam_model)
