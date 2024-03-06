from pathlib import Path
from typing import Dict, List

from antx import transfer

from stam_annotator.config import PECHAS_PATH
from stam_annotator.stam_fetcher.pecha import Pecha


class Pecha_MD_formatter:
    def __init__(self, pecha: Pecha):
        self.pecha = pecha
        self.pecha_id = pecha.id_
        self.base_texts = self.load_base_texts()
        self.grouped_annotations = self.group_annotations_by_type()

    @classmethod
    def from_id(cls, pecha_id: str, github_token: str, out_path: Path = PECHAS_PATH):
        pecha = Pecha.from_id(pecha_id, github_token, out_path)
        return cls(pecha) if pecha else None

    def load_base_texts(self):
        base_texts = {}
        for volume_name in self.pecha.get_pecha_volume_names():
            base_texts[volume_name] = self.pecha.get_base_text(volume_name)
        return base_texts

    def group_annotations_by_type(self):
        grouped_annotations: Dict[str, Dict[str, List]] = {}
        annotations = self.pecha.get_annotations()
        for volume_id, volume_annotations in annotations.items():
            grouped_annotations[volume_id] = {}
            for annotation_id, annotation_details in volume_annotations.items():
                annotation_type = annotation_details["annotation"]
                annotation_entry = {
                    "text": annotation_details["text"],
                    "span": annotation_details["span"],
                }
                if annotation_type not in grouped_annotations[volume_id]:
                    grouped_annotations[volume_id][annotation_type] = [annotation_entry]
                else:
                    grouped_annotations[volume_id][annotation_type].append(
                        annotation_entry
                    )
        return grouped_annotations

    def serialize(self, output_dir: Path):
        for volume_name in self.pecha.get_pecha_volume_names():
            self.serialize_volume(volume_name, output_dir)

    def serialize_volume(self, volume_name: str, output_dir: Path):
        base_text = self.base_texts[volume_name]
        volume_annotations = self.grouped_annotations[volume_name]
        for annotation_type, annotations in volume_annotations.items():
            base_text = self.apply_annotation(base_text, annotation_type, annotations)

        output_md_file = output_dir / f"{self.pecha_id}_{volume_name}.md"
        output_md_file.write_text(base_text)

    @staticmethod
    def apply_annotation(base_text: str, ann_type: str, annotations: List[Dict]) -> str:
        if ann_type == "BookTitle":
            ann_style = [["BookTitle start", r"<h1>"], ["BookTitle end", r"</h1>"]]
        if ann_type == "Chapter":
            ann_style = [["Chapter start", r"<h2>"], ["Chapter end", r"</h2>"]]
        if ann_type == "Sabche":
            ann_style = [["Sabche start", r"<h3>"], ["Sabche end", r"</h3>"]]
        if ann_type == "Author":
            ann_style = [["Author start", r"<i>—"], ["Author end", r"—</i>"]]
        if ann_type == "Yigchung":
            ann_style = [["Yigchung start", r"<i>"], ["Yigchung end", r"</i>"]]
        if ann_type == "Quotation":
            ann_style = [
                ["Quotation start", r"<blockquote>"],
                ["Quotation end", r"</blockquote>"],
            ]

        for annotation in annotations:
            start, end = annotation["span"]["start"], annotation["span"]["end"]
            base_text_with_annotation = (
                base_text[:start]
                + ann_style[0][1]
                + base_text[start:end]
                + ann_style[1][1]
                + base_text[end:]
            )
            result = transfer(
                base_text_with_annotation, ann_style, base_text, output="txt"
            )
            base_text = result

        return base_text


if __name__ == "__main__":
    from stam_annotator.github_token import GITHUB_TOKEN

    pecha_id = "P000216"
    formatter = Pecha_MD_formatter.from_id(pecha_id, GITHUB_TOKEN)

    output_dir = Path(".")
    formatter.serialize(output_dir)
