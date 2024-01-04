import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from github import Github, GithubException
from stam import AnnotationStore

from stam_annotator.config import PECHAS_PATH, AnnotationEnum, AnnotationGroupEnum
from stam_annotator.exceptions import RepoCloneError, RepoDoesNotExist
from stam_annotator.utility import get_enum_value_if_match_ignore_case

ORGANIZATION = "PechaData"


class Pecha:
    def __init__(self, id_: str, base_path: Path):
        self.id_ = id_
        self.base_path = base_path
        self.stams: Dict[str, AnnotationStore] = {}
        self.load_stams()

    @property
    def pecha_fn(self):
        return self.base_path / f"{self.id_}.opf" / "layers"

    def load_stams(self):
        json_files = list(self.pecha_fn.glob("**/*.opf.json"))
        for json_file in json_files:
            index = json_file.name.index(".opf.json")
            stam_name = json_file.name[:index]
            self.stams[stam_name] = AnnotationStore(file=str(json_file))

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

    def get_annotation(self, id_: str, pecha_stam_name) -> str:
        """stam returns annotation texts in a list, so we join them"""
        annotation_text_list = self.stams[pecha_stam_name].annotation(id_).text()
        annotation_text = " ".join(annotation_text_list)
        return annotation_text

    def get_stam_name(self):
        keys = list(self.stams.keys())
        if len(keys) != 1:
            print("Please provide the volume name as an argument as well.")
            return None
        return keys[0]

    def get_stam_annotations_in_dict_format(self, annotations) -> Dict:
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
            if annotation_payloads:
                annotation_content["payloads"] = annotation_payloads
            annotations_dict[annotation.id()] = annotation_content
        return annotations_dict

    def get_annotations(
        self,
        annotation_group: Optional[AnnotationGroupEnum] = None,
        annotation_type: Optional[AnnotationEnum] = None,
    ) -> Optional[Dict]:
        """this is for pechas with no volumes, such that only one stam is there"""
        stam_name = self.get_stam_name()
        if annotation_group is None or annotation_type is None:
            stam_annotations = self.stams[stam_name].annotations()
        else:
            stam_name = self.get_stam_name()
            stam_annotation_store = self.stams[stam_name]
            stam_dataset = next(stam_annotation_store.datasets())
            stam_key = stam_dataset.key(annotation_group.value)
            stam_annotations = stam_annotation_store.annotations(
                filter=stam_key, value=annotation_type.value
            )

        annotations_dict = self.get_stam_annotations_in_dict_format(stam_annotations)
        return annotations_dict


class Alignment:
    segment_source: Dict[str, Dict[str, str]]
    segment_pairs: Dict[str, Dict[str, str]]

    def __init__(self, id_: str, github_token: str, base_path: Path):
        self.id_ = id_
        self.github_token = github_token
        self.base_path = base_path
        self.pechas: Dict = {}
        self.load_alignment()

    @property
    def alignment_fn(self):
        return str(self.base_path / f"{self.id_}.opa" / "alignment.json")

    def load_alignment(self):
        with open(self.alignment_fn, encoding="utf-8") as file:
            data = json.load(file)
        self.segment_source = data["segment_sources"]
        self.segment_pairs = data["segment_pairs"]

        # load pechas
        for id_ in self.segment_source.keys():
            self.pechas[id_] = Pecha.from_id(id_, self.github_token)

    def get_meta_data(self):
        for file_path in self.base_path.rglob("meta.json"):
            with file_path.open() as file:
                return json.load(file)
        return {}

    def get_segment_pairs(self):
        for id_ in self.segment_pairs:
            yield self.get_segment_pair(id_)

    def get_segment_pair(self, id_) -> List[Tuple[str, str]]:
        segment_pair = []
        for pecha_id, segment_id in self.segment_pairs[id_].items():
            segment_lang = self.segment_source[pecha_id]["lang"]
            pecha_stam_name = self.segment_source[pecha_id]["base"]
            segment_text = self.pechas[pecha_id].get_annotation(
                segment_id, pecha_stam_name
            )
            segment_pair.append((segment_text, segment_lang))
        return segment_pair

    @classmethod
    def from_id(cls, id_: str, github_token: str, out_path: Path = PECHAS_PATH):
        """load if alignment exits"""
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
                print(f"Alignment {error.message}")
                return None
            except RepoCloneError as error:
                print(f"Alignment {error.message}")
                return None

        cls.base_path = out_path / f"{id_}"
        return cls(id_, github_token, cls.base_path)


def check_repo_exists(token, org_name, repo_name):
    g = Github(token)
    try:
        org = g.get_organization(org_name)
        org.get_repo(repo_name)
    except GithubException:
        raise RepoDoesNotExist(org_name, repo_name)


def clone_repo(org, repo_name, token, destination_folder: Path):
    try:
        """make a inner folder with source org name and clone the repo in it"""
        repo_url = f"https://{token}@github.com/{org}/{repo_name}.git"
        subprocess.run(["git", "clone", repo_url, destination_folder], check=True)
        print(f"Repository {repo_name} cloned successfully into {destination_folder}")

    except subprocess.CalledProcessError as e:
        raise RepoCloneError(org, repo_name, e)
