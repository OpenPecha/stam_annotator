import json
from pathlib import Path
from typing import Dict, List, Tuple

from stam_annotator.definations import OPA_DIR, ORGANIZATION
from stam_annotator.github_token import GITHUB_TOKEN
from stam_annotator.utility import (
    get_json_alignment,
    json_alignment_exists_in_repo,
    make_json_alignment,
)


class Pecha:
    pecha_id: str


class Alignment:
    segment_source: Dict[str, Dict[str, str]]
    segment_pairs: Dict[str, Dict[str, str]]

    def __init__(self, id_: str, base_path: Path):
        self.id_ = id_
        self.base_path = base_path
        self.pechas: Dict = {}
        self.load_alignment()

    @property
    def alignment_fn(self):
        return self.base_path

    def load_alignment(self):
        with open(self.alignment_fn, encoding="utf-8") as file:
            data = json.load(file)
        self.segment_source = data["segment_sources"]
        self.segment_pairs = data["segment_pairs"]

    def get_segment_pairs(self):
        for id_ in self.segment_pairs:
            yield self.get_segment_pair(id_)

    def get_segment_pair(self, id_) -> List[Tuple[str, str]]:
        segment_pair = []
        for pecha_id, segment_id in self.segment_pairs[id_].items():
            segment_lang = self.segment_source[pecha_id]["lang"]
            segment_text = self.pechas[pecha_id].get_annotation(segment_id)
            segment_pair.append((segment_text, segment_lang))
        return segment_pair

    @classmethod
    def from_id(cls, id_: str) -> "Alignment":
        """load if alignment exits, else create and load"""
        if json_alignment_exists_in_repo(ORGANIZATION, id_, GITHUB_TOKEN):
            cls.base_path = get_json_alignment(ORGANIZATION, id_, GITHUB_TOKEN)
            return cls(id_, cls.base_path)

        cls.base_path = make_json_alignment(ORGANIZATION, id_, GITHUB_TOKEN)
        return cls(id_, cls.base_path)


if __name__ == "__main__":
    alignment = Alignment("A0B609189", OPA_DIR / "36CA.json")
    print(alignment)
