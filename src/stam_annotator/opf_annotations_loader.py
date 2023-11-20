from dataclasses import dataclass
from typing import Dict, Iterator, Tuple

from stam_annotator.config import OPF_DIR
from stam_annotator.load_yaml_annotations import load_opf_annotations_from_yaml


@dataclass
class Span:
    start: int
    end: int


@dataclass
class Annotation:
    uuid: str
    span: Span


class Annotations:
    def __init__(self, annotations: Dict[str, Dict]):
        self.annotations = {
            uuid: Annotation(uuid, Span(**value["span"]))
            for uuid, value in annotations.items()
        }

    def items(self) -> Iterator[Tuple[str, Annotation]]:
        return iter(self.annotations.items())


@dataclass
class OpfAnnotation:
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
