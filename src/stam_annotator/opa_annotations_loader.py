from pathlib import Path
from typing import Dict, Iterator, Tuple

from stam_annotator.config import OPA_DIR
from stam_annotator.load_yaml_annotations import load_opa_annotations_from_yaml


class SegmentSource:
    def __init__(self, source_id: str, type: str, relation: str, lang: str, base: str):
        self.source_id = source_id
        self.type = type
        self.relation = relation
        self.lang = lang
        self.base = base


class SegmentPair:
    def __init__(self, pair_id: str, sources: Dict[str, str]):
        self.pair_id = pair_id
        self.sources = sources


class SegmentData:
    def __init__(
        self,
        segment_sources: Dict[str, SegmentSource],
        segment_pairs: Dict[str, SegmentPair],
    ):
        self.segment_sources = segment_sources
        self.segment_pairs = segment_pairs

    @staticmethod
    def from_dict(data: Dict) -> "SegmentData":
        sources = {
            id: SegmentSource(id, **details)
            for id, details in data.get("segment_sources", {}).items()
        }
        pairs = {
            id: SegmentPair(id, {key: value for key, value in pair.items()})
            for id, pair in data.get("segment_pairs", {}).items()
        }
        return SegmentData(segment_sources=sources, segment_pairs=pairs)

    def items(self) -> Iterator[Tuple[str, SegmentPair]]:
        return iter(self.segment_pairs.items())


def create_opa_annotation_instance(yaml_path: Path) -> SegmentData:

    data = load_opa_annotations_from_yaml(yaml_path)
    return SegmentData.from_dict(data)


if __name__ == "__main__":
    file_path = OPA_DIR / "36CA.yml"

    segment_data = create_opa_annotation_instance(file_path)
    for pair_id, pair in segment_data.items():
        print(f"Pair ID: {pair_id}, Sources: {pair.sources}")
