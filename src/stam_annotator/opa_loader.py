from pathlib import Path
from typing import Dict

from pydantic import BaseModel, field_validator

from stam_annotator.definations import OPA_DIR
from stam_annotator.utility import (
    load_opa_annotations_from_yaml,
    read_json_to_dict,
    save_json_file,
)


class SegmentSource(BaseModel):
    type: str
    relation: str
    lang: str
    base: str

    @field_validator("relation")
    @classmethod
    def validate_relation(cls, v):
        if v not in ["source", "target"]:
            raise ValueError("Relation must be either 'source' or 'target'")
        return v

    @field_validator("lang")
    @classmethod
    def validate_lang(cls, v):
        if v not in ["bo", "en"]:
            raise ValueError("Language must be either 'bo' or 'en'")
        return v


class OpaAnnotation(BaseModel):
    segment_sources: Dict[str, SegmentSource]
    segment_pairs: Dict[str, Dict[str, str]]

    def items(self):
        return iter(self.segment_pairs.items())


def create_opa_annotation_instance(yaml_path: Path) -> OpaAnnotation:
    data = load_opa_annotations_from_yaml(yaml_path)
    return OpaAnnotation(
        segment_sources=data["segment_sources"], segment_pairs=data["segment_pairs"]
    )


def create_opa_annotation_from_json(json_path: Path) -> OpaAnnotation:
    """
    Reads a JSON file and returns an OpaAnnotation instance.
    """
    data = read_json_to_dict(json_path)
    return OpaAnnotation(**data)


if __name__ == "__main__":
    file_path = OPA_DIR / "36CA.yml"
    data = load_opa_annotations_from_yaml(file_path)
    opa_annotation = create_opa_annotation_instance(file_path)
    opa_json = opa_annotation.model_dump()
    save_json_file(opa_json, OPA_DIR / "36CA.json")
