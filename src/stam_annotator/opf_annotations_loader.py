from typing import Dict

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from stam_annotator.config import OPF_DIR
from stam_annotator.load_yaml_annotations import load_opf_annotations_from_yaml
from stam_annotator.utility import get_uuid


class Span(BaseModel):
    start: int = Field(ge=0)
    end: int = Field(ge=0)

    @field_validator("end")
    @classmethod
    def end_must_not_be_less_than_start(cls, v: int, values: ValidationInfo) -> int:
        if "start" in values.data and v < values.data["start"]:
            raise ValueError("Span end must not be less than start")
        return v


class Annotation(BaseModel):
    id: str
    span: Span

    @field_validator("id", mode="before")
    @classmethod
    def set_id(cls, v):
        return v or get_uuid()


class Annotations(BaseModel):
    annotations_dict: Dict[str, Annotation]

    def __init__(self, annotations: Dict[str, Dict]):
        if annotations is None or not annotations:
            annotations_processed = {}
        else:
            annotations_processed = {
                id: Annotation(id=id, span=Span(**value["span"]))
                for id, value in annotations.items()
            }
        super().__init__(annotations_dict=annotations_processed)

    def __getitem__(self, item):
        return self.annotations_dict[item]

    def items(self):
        return self.annotations_dict.items()


class OpfAnnotation(BaseModel):
    id: str
    annotation_type: str
    revision: str
    annotations: Annotations

    @field_validator("id", mode="before")
    @classmethod
    def set_id(cls, v):
        return v or get_uuid()

    @field_validator("annotation_type")
    @classmethod
    def annotation_type_must_alphabets(cls, v):
        if not v.isalpha():
            raise ValueError("annotation_type must be alphabetic")
        return v

    @field_validator("revision")
    @classmethod
    def revision_must_int_parsible(cls, v):
        if not v.isdigit():
            raise ValueError(
                "revision must be parsable to an integer and consist only of digits"
            )
        return v


def create_opf_annotation_instance(data: Dict) -> OpfAnnotation:
    annotations = Annotations(data["annotations"])
    return OpfAnnotation(
        id=data["id"],
        annotation_type=data["annotation_type"],
        revision=data["revision"],
        annotations=annotations,
    )


if __name__ == "__main__":
    opf_yml_data = load_opf_annotations_from_yaml(OPF_DIR / "Quotation.yml")
    opf_annotation = create_opf_annotation_instance(opf_yml_data)
    print(f"id: {opf_annotation.id}")
    print(f"annotation_type: {opf_annotation.annotation_type}")
    print(f"revision: {opf_annotation.revision}")
    for id, value in opf_annotation.annotations.items():
        print(f"id: {id}, start: {value.span.start} - end: {value.span.end}")
