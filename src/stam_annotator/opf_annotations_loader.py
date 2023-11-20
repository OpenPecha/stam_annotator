from typing import Dict

from pydantic import BaseModel

from stam_annotator.config import OPF_DIR
from stam_annotator.load_yaml_annotations import load_opf_annotations_from_yaml


class Span(BaseModel):
    start: int
    end: int


class Annotation(BaseModel):
    uuid: str
    span: Span


class Annotations(BaseModel):
    annotations_dict: Dict[str, Annotation]

    def __init__(self, annotations: Dict[str, Dict]):
        annotations_processed = {
            uuid: Annotation(uuid=uuid, span=Span(**value["span"]))
            for uuid, value in annotations.items()
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
    for uuid, value in opf_annotation.annotations.items():
        print(f"uuid: {uuid}, start: {value.span.start} - end: {value.span.end}")
