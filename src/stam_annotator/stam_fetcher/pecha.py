import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from stam import Annotation, AnnotationStore

from stam_annotator.config import PECHAS_PATH, AnnotationEnum, AnnotationGroupEnum
from stam_annotator.exceptions import RepoCloneError, RepoDoesNotExist
from stam_annotator.stam_fetcher.utility import check_repo_exists, clone_repo
from stam_annotator.utility import get_enum_value_if_match_ignore_case

ORGANIZATION = "PechaData"


class Pecha:
    def __init__(self, id_: str, base_path: Path):
        self.id_ = id_
        self.base_path = base_path
        self.pecha_volumes: Dict[str, AnnotationStore] = {}
        self.load_pecha()

    @property
    def pecha_fn(self):
        return self.base_path / f"{self.id_}.opf" / "layers"

    def load_pecha(self):
        json_files = list(self.pecha_fn.glob("**/*.opf.json"))
        for json_file in json_files:
            index = json_file.name.index(".opf.json")
            volumen_name = json_file.name[:index]
            self.pecha_volumes[volumen_name] = AnnotationStore(file=str(json_file))

    @classmethod
    def from_id(cls, id_: str, github_token: str, out_path: Path = PECHAS_PATH):
        """Check if repo exists in github"""
        if not (out_path / f"{id_}").exists():
            try:
                check_repo_exists(github_token, ORGANIZATION, repo_name=id_)
                clone_repo(
                    ORGANIZATION,
                    id_,
                    github_token,
                    destination_folder=out_path / f"{id_}",
                )
            except RepoDoesNotExist as error:
                print(f"Pecha {error.message}")
                return None
            except RepoCloneError as error:
                print(f"Pecha {error.message}")
                return None

        cls.base_path = out_path / f"{id_}"
        return cls(id_, cls.base_path)

    def get_meta_data(self):
        for file_path in self.base_path.rglob("meta.json"):
            with file_path.open() as file:
                return json.load(file)
        return {}

    def get_index_data(self):
        for file_path in self.base_path.rglob("index.json"):
            with file_path.open() as file:
                return json.load(file)
        return {}

    @staticmethod
    def get_span_from_annotation(annotation: Annotation) -> Dict:
        return {
            "start": annotation.offset().begin().value(),
            "end": annotation.offset().end().value(),
        }

    def get_annotation(self, id_: str, volume_name) -> Tuple[str, Dict]:
        """stam returns annotation texts in a list, so we join them"""
        annotation = self.pecha_volumes[volume_name].annotation(id_)
        annotation_text = " ".join(annotation.text())
        annotation_span = self.get_span_from_annotation(annotation)
        return (annotation_text, annotation_span)

    def get_pecha_volume_names(self) -> List:
        return list(self.pecha_volumes.keys())

    def format_annotations_as_dict(self, annotations) -> Dict:
        annotations_dict = {}
        for annotation in annotations:
            """get annotation text, key and type"""
            annotation_content = {}
            annotation_payloads = {}
            for annotation_data in annotation:
                key, value = annotation_data.key().id(), str(annotation_data.value())
                matched_enum = get_enum_value_if_match_ignore_case(
                    AnnotationGroupEnum, key
                )
                if matched_enum:
                    annotation_content["annotation_group"] = key
                    annotation_content["annotation"] = value
                else:
                    annotation_payloads[key] = value

            """save annotation data in a dict with annotation id """
            annotation_content["text"] = str(annotation)
            annotation_content["span"] = self.get_span_from_annotation(annotation)
            if annotation_payloads:
                annotation_content["payloads"] = annotation_payloads
            annotations_dict[annotation.id()] = annotation_content
        return annotations_dict

    def get_annotations(self) -> Optional[Dict]:
        annotations = {}
        for volume_name in self.get_pecha_volume_names():
            stam_annotations = self.pecha_volumes[volume_name].annotations()
            volume_annotations = self.format_annotations_as_dict(stam_annotations)
            annotations[volume_name] = volume_annotations
        return annotations

    def get_filtered_annotations(
        self,
        annotation_group: Optional[AnnotationGroupEnum] = None,
        annotation_type: Optional[AnnotationEnum] = None,
    ) -> Optional[Dict]:
        if annotation_group is None or annotation_type is None:
            print("Please provide annotation_group and annotation_type")
            return None

        annotations = {}
        for volume_name in self.get_pecha_volume_names():
            stam_volume = self.pecha_volumes[volume_name]
            stam_dataset = next(stam_volume.datasets())
            stam_key = stam_dataset.key(annotation_group.value)
            stam_annotations = stam_volume.annotations(
                filter=stam_key, value=annotation_type.value
            )
            volume_annotations = self.format_annotations_as_dict(stam_annotations)
            annotations[volume_name] = volume_annotations
        return annotations


if __name__ == "__main__":

    from stam_annotator.config import AnnotationEnum, AnnotationGroupEnum
    from stam_annotator.github_token import GITHUB_TOKEN

    pecha_repo = Pecha.from_id("P000216", GITHUB_TOKEN)
    annotations = pecha_repo.get_annotations()
    for key, value in annotations.items():
        print(key, value)
