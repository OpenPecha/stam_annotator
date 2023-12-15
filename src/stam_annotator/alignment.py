import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

from github import Github, GithubException
from stam import AnnotationStore

from stam_annotator.config import PECHAS_PATH
from stam_annotator.exceptions import RepoDoesNotExist
from stam_annotator.github_token import GITHUB_TOKEN

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
        json_files = list(self.pecha_fn.glob("**/*.json"))
        for json_file in json_files:
            self.stams[json_file.parent.name] = AnnotationStore(file=str(json_file))

    @classmethod
    def from_id(cls, id_: str, out_path: Path = PECHAS_PATH):
        """Check if repo exists in github"""
        if not (out_path / f"{id_}").exists():
            try:
                check_repo_exists(GITHUB_TOKEN, ORGANIZATION, repo_name=id_)
                clone_repo(
                    ORGANIZATION,
                    id_,
                    GITHUB_TOKEN,
                    destination_folder=out_path / f"{id_}",
                )
            except RepoDoesNotExist as error:
                print(f"Pecha {error.message}")
                return None
        cls.base_path = out_path / f"{id_}"
        return cls(id_, cls.base_path)

    def get_annotation(self, id_: str, pecha_stam_name) -> str:
        """stam returns annotation texts in a list, so we join them"""
        annotation_text_list = self.stams[pecha_stam_name].annotation(id_).text()
        annotation_text = " ".join(annotation_text_list)
        return annotation_text


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
        return str(self.base_path / f"{self.id_}.opa" / "alignment.json")

    def load_alignment(self):
        with open(self.alignment_fn, encoding="utf-8") as file:
            data = json.load(file)
        self.segment_source = data["segment_sources"]
        self.segment_pairs = data["segment_pairs"]

        # load pechas
        for id_ in self.segment_source.keys():
            self.pechas[id_] = Pecha.from_id(id_)

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
    def from_id(cls, id_: str, out_path: Path = PECHAS_PATH):
        """load if alignment exits"""
        if not (out_path / f"{id_}").exists():
            try:
                check_repo_exists(GITHUB_TOKEN, ORGANIZATION, repo_name=id_)
                clone_repo(
                    ORGANIZATION,
                    id_,
                    GITHUB_TOKEN,
                    destination_folder=out_path / f"{id_}",
                )
            except RepoDoesNotExist as error:
                print(f"Alignment {error.message}")
                return None

        cls.base_path = out_path / f"{id_}"
        return cls(id_, cls.base_path)


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
        print(f"Error cloning {repo_name} repository: {e}")


if __name__ == "__main__":
    alignment = Alignment.from_id("AB3CAED2A")
    for segment_pair in alignment.get_segment_pairs():
        print(segment_pair)
