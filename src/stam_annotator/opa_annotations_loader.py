from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, Tuple

from stam_annotator.config import OPA_DIR
from stam_annotator.load_yaml_annotations import load_opa_annotations_from_yaml


@dataclass
class SegmentSource:
    source_id: str
    type: str
    relation: str
    lang: str
    base: str


@dataclass
class SegmentPair:
    pair_id: str
    sources: Dict[str, str]


@dataclass
class OpaAnnotation:
    segment_sources: Dict[str, SegmentSource]
    segment_pairs: Dict[str, SegmentPair]

    @staticmethod
    def from_dict(data: Dict) -> "OpaAnnotation":
        sources = {
            id: SegmentSource(id, **details)
            for id, details in data.get("segment_sources", {}).items()
        }
        pairs = {
            id: SegmentPair(id, {key: value for key, value in pair.items()})
            for id, pair in data.get("segment_pairs", {}).items()
        }
        return OpaAnnotation(segment_sources=sources, segment_pairs=pairs)

    def items(self) -> Iterator[Tuple[str, SegmentPair]]:
        return iter(self.segment_pairs.items())


def create_opa_annotation_instance(yaml_path: Path) -> OpaAnnotation:
    data = load_opa_annotations_from_yaml(yaml_path)
    return OpaAnnotation.from_dict(data)


if __name__ == "__main__":
    file_path = OPA_DIR / "36CA.yml"
    opa_annotation = create_opa_annotation_instance(file_path)
    for pair_id, pair in opa_annotation.items():
        print(f"Pair ID: {pair_id}, Sources: {pair.sources}")
