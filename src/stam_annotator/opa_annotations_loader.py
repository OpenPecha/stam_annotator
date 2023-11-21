from pathlib import Path
from typing import Dict, Iterator, Tuple

from pydantic import BaseModel

from stam_annotator.config import OPA_DIR
from stam_annotator.load_yaml_annotations import load_opa_annotations_from_yaml


class SegmentSource(BaseModel):
    source_id: str
    type: str
    relation: str
    lang: str
    base: str


class SegmentPair(BaseModel):
    pair_id: str
    sources: Dict[str, str]


class OpaAnnotation(BaseModel):
    segment_sources: Dict[str, SegmentSource]
    segment_pairs: Dict[str, SegmentPair]

    @classmethod
    def __init__(self, segment_sources: Dict, segment_pairs: Dict):
        self.segment_sources = {
            id: SegmentSource(source_id=id, **details)
            for id, details in segment_sources.items()
        }
        self.segment_pairs = {
            id: SegmentPair(pair_id=id, sources=value)
            for id, value in segment_pairs.items()
        }

    def items(self) -> Iterator[Tuple[str, SegmentPair]]:
        return iter(self.segment_pairs.items())


def create_opa_annotation_instance(yaml_path: Path) -> OpaAnnotation:
    data = load_opa_annotations_from_yaml(yaml_path)
    return OpaAnnotation(data["segment_sources"], data["segment_pairs"])


if __name__ == "__main__":
    file_path = OPA_DIR / "36CA.yml"
    opa_annotation = create_opa_annotation_instance(file_path)
    for pair_id, pair in opa_annotation.items():
        print(f"Pair ID: {pair_id}, Sources: {pair.sources}")
