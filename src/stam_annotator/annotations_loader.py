from typing import Dict, Iterator, Tuple

from stam_annotator.config import DATA_DIR
from stam_annotator.load_yaml_annotations import load_annotations_from_yaml


class Span:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


class Annotation(Span):
    def __init__(self, uuid: str, span: Dict[str, int]):
        self.uuid = uuid
        self.span = Span(**span)


class Annotations:
    def __init__(self, annotations: Dict[str, Dict]):
        self.annotations = {
            uuid: Annotation(uuid, **value) for uuid, value in annotations.items()
        }

    def items(self) -> Iterator[Tuple[str, Annotation]]:
        return iter(self.annotations.items())


class AnnotationDocument:
    def __init__(self, id: str, annotation_type: str, revision: str, annotations: Dict):
        self.id = id
        self.annotation_type = annotation_type
        self.revision = revision
        self.annotations = Annotations(annotations)


if __name__ == "__main__":
    data = load_annotations_from_yaml(DATA_DIR / "Quotation.yml")

    annotation_doc = AnnotationDocument(**data)
    print(f"id: {annotation_doc.id}")
    print(f"annotation_type: {annotation_doc.annotation_type}")
    print(f"revision: {annotation_doc.revision}")
    for uuid, value in annotation_doc.annotations.items():
        print(f"uuid: {uuid}, start:{value.span.start} - end:{value.span.end}")
