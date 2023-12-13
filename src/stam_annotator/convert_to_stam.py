import json
import shutil
import subprocess
from datetime import datetime
from json import JSONEncoder
from pathlib import Path
from typing import Dict, List

import yaml
from github import Github

from stam_annotator.definations import ROOT_DIR, KeyEnum
from stam_annotator.github_token import GITHUB_TOKEN
from stam_annotator.opf_to_stam import opf_to_stam_pipeline
from stam_annotator.stam_manager import combine_stams
from stam_annotator.utility import save_annotation_store

SOURCE_ORG = "OpenPecha-Data"
DESTINATION_ORG = "PechaData"


class PechaRepo:
    pecha_id: str
    source_org: str
    destination_org: str

    def __init__(self, id_: str, base_path: Path):
        self.pecha_id = id_
        self.source_org = SOURCE_ORG
        self.destination_org = DESTINATION_ORG
        self.base_path = base_path

    @property
    def pecha_repo_fn(self):
        return self.base_path / f"{self.source_org}"

    @classmethod
    def from_id(cls, id_: str) -> "PechaRepo":
        cls.base_path = make_local_folder(ROOT_DIR / id_)
        return PechaRepo(id_, cls.base_path)

    def get_pecha_repo(self):
        try:
            org, repo_name, token = self.source_org, self.pecha_id, GITHUB_TOKEN
            """make a inner folder with source org name and clone the repo in it"""
            destination_folder = self.base_path / org
            repo_url = f"https://{token}@github.com/{org}/{repo_name}.git"
            subprocess.run(["git", "clone", repo_url, destination_folder], check=True)
            print(
                f"Repository {repo_name} cloned successfully into {destination_folder}"
            )

        except subprocess.CalledProcessError as e:
            print(f"Error cloning {repo_name} repository: {e}")

    def convert_pecha_repo_to_stam(self):
        group_files = get_folder_structure(self.base_path / self.source_org)
        make_local_folder(self.base_path / self.destination_org)
        for parent_dir, documents in group_files.items():
            new_parent_dir = replace_parent_folder_name(
                parent_dir, self.source_org, self.destination_org
            )
            """store all the converted stams in same dir and then combine"""
            stams_in_dir = []
            """loop through a files and folder in same dir."""
            for doc, tag in documents:
                if tag == "folder":
                    make_local_folder(new_parent_dir / doc)
                    continue
                if doc in ["meta.yml", "index.yml"]:
                    json_file_path = parent_dir / doc
                    yml_file_path = new_parent_dir / doc.replace(".yml", ".json")
                    convert_yml_file_to_json(json_file_path, yml_file_path)
                    continue
                if not doc.endswith(".yml"):
                    shutil.copy(parent_dir / doc, new_parent_dir / doc)
                    continue
                """convert yml files to stam"""
                if parent_dir.parent.name == "layers":
                    base_file_path = next(
                        self.pecha_repo_fn.rglob(f"{parent_dir.name}.txt")
                    )
                    curr_stam = opf_to_stam_pipeline(
                        parent_dir / doc, base_file_path, KeyEnum.structure_type
                    )
                    stams_in_dir.append(curr_stam)
                    continue
            if len(stams_in_dir) == 1:
                curr_stam = stams_in_dir[0]
                save_annotation_store(
                    curr_stam, new_parent_dir / f"{parent_dir.name}.opf.json"
                )

                continue
            if len(stams_in_dir) > 1:
                curr_stam = combine_stams(stams_in_dir)
                save_annotation_store(
                    curr_stam, new_parent_dir / f"{parent_dir.name}opf.json"
                )
                continue

    def upload_pecha_repo(self):
        org_name, repo_name = DESTINATION_ORG, self.pecha_id
        repo_is_created = create_github_repo(org_name, repo_name, GITHUB_TOKEN)
        if repo_is_created:
            project_path = self.base_path / self.destination_org
            repo_name = self.pecha_id
            upload_files_to_github_repo(org_name, repo_name, project_path, GITHUB_TOKEN)
            print(f"Pecha repo {repo_name} uploaded successfully")


class AlignmentRepo:
    alignment_id: str
    source_org: str
    destination_org: str
    pechas: Dict[str, PechaRepo]

    def __init__(self, id_: str, base_path: Path):
        self.alignment_id = id_
        self.source_org = SOURCE_ORG
        self.destination_org = DESTINATION_ORG
        self.base_path = base_path
        self.pecha_repos: Dict[str, PechaRepo] = {}

    @property
    def alignment_repo_fn(self):
        return (
            self.base_path
            / f"{self.destination_org}"
            / f"{self.alignment_id}.opa"
            / "meta.json"
        )

    @classmethod
    def from_id(cls, id_: str) -> "AlignmentRepo":
        cls.base_path = make_local_folder(ROOT_DIR / id_)
        return AlignmentRepo(id_, cls.base_path)

    def load_pecha_repos(self):
        with open(self.alignment_repo_fn, encoding="utf-8") as file:
            data = json.load(file)
        pechas = data["pechas"]
        for pecha_id in pechas:
            self.pecha_repos[pecha_id] = PechaRepo.from_id(pecha_id)

    def get_alignment_repo(self):
        try:
            org, repo_name, token = self.source_org, self.alignment_id, GITHUB_TOKEN
            """make a inner folder with source org name and clone the repo in it"""
            destination_folder = self.base_path / org
            repo_url = f"https://{token}@github.com/{org}/{repo_name}.git"
            subprocess.run(["git", "clone", repo_url, destination_folder], check=True)
            print(
                f"Repository {repo_name} cloned successfully into {destination_folder}"
            )

        except subprocess.CalledProcessError as e:
            print(f"Error cloning {repo_name} repository: {e}")

    def convert_alignment_repo_to_json(self):
        group_files = get_folder_structure(self.base_path / self.source_org)
        make_local_folder(self.base_path / self.destination_org)
        for parent_dir, documents in group_files.items():
            new_parent_dir = replace_parent_folder_name(
                parent_dir, self.source_org, self.destination_org
            )
            """loop through a files and folder in same dir."""
            for doc, tag in documents:
                if tag == "folder":
                    make_local_folder(new_parent_dir / doc)
                    continue
                if doc.endswith(".yml"):
                    yml_file_path = parent_dir / doc
                    json_file_path = new_parent_dir / doc.replace(".yml", ".json")
                    convert_yml_file_to_json(yml_file_path, json_file_path)
                    continue

                shutil.copy(parent_dir / doc, new_parent_dir / doc)
                continue

    def upload_alignment_repo(self):
        org_name, repo_name = DESTINATION_ORG, self.alignment_id
        repo_is_created = create_github_repo(org_name, repo_name, GITHUB_TOKEN)
        if repo_is_created:
            project_path = self.base_path / self.destination_org
            repo_name = self.alignment_id
            upload_files_to_github_repo(org_name, repo_name, project_path, GITHUB_TOKEN)
            print(f"Alignment repo {repo_name} uploaded successfully")

    def get_aligned_pechas(self):
        self.load_pecha_repos()
        for _, pecha in self.pecha_repos.items():
            pecha.get_pecha_repo()

    def upload_aligned_pechas(self):
        for _, pecha_repo in self.pecha_repos.items():
            pecha_repo.upload_pecha_repo()


def create_github_repo(org_name: str, repo_name: str, token: str) -> bool:
    try:
        g = Github(token)
        org = g.get_organization(org_name)
        org.create_repo(repo_name)
        print(f"Repository {repo_name} created successfully")
        return True
    except:  # noqa
        print(f"Repo {repo_name} already exists")
        return False


def upload_files_to_github_repo(
    org_name: str,
    repo_name: str,
    project_path: Path,
    token: str,
    commit_message: str = "upload file",
):
    g = Github(token)
    repo = g.get_organization(org_name).get_repo(repo_name)
    for file in project_path.rglob("*"):
        if file.is_dir():
            continue
        with open(file, encoding="utf-8") as f:
            data = f.read()
        """upload file to github repo """
        relative_file_path = file.relative_to(project_path)
        repo.create_file(str(relative_file_path), commit_message, data, branch="main")


def make_local_folder(destination_folder: Path) -> Path:
    """make local folder to clone the alignment and pecha repo"""
    destination_folder.mkdir(parents=True, exist_ok=True)
    return destination_folder


def get_folder_structure(path: Path):
    base_path = Path(path)
    grouped_files: Dict[Path, List] = {}

    for file in base_path.rglob("*"):
        if ".git" not in file.parts:
            # Group files and folders by their parent directory
            file_tag_pair = (file.name, "file" if file.is_file() else "folder")
            if file.parent not in grouped_files:
                grouped_files[file.parent] = [file_tag_pair]
            else:
                grouped_files[file.parent].append(file_tag_pair)

    return grouped_files


def replace_parent_folder_name(path: Path, old_name: str, new_name: str):
    """Replace the parent folder name of the path with the new name"""

    new_path = str(path).replace(old_name, new_name)
    return Path(new_path)


def convert_yml_file_to_json(yml_file_path: Path, json_file_path: Path):
    yml_content = yml_file_path.read_text(encoding="utf-8")
    converted_json = json.dumps(
        yaml.safe_load(yml_content), indent=4, cls=CustomEncoder
    )
    json_file_path.write_text(converted_json)


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format the date however you like
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)


if __name__ == "__main__":

    # repo = AlignmentRepo.from_id("AB3CAED2A")
    # repo.get_alignment_repo()
    # repo.convert_alignment_repo_to_json()
    # repo.get_aligned_pechas()
    # for pecha_id, pecha_repo in repo.pecha_repos.items():
    #     pecha_repo = PechaRepo(pecha_id, ROOT_DIR / pecha_id)
    #     pecha_repo.convert_pecha_repo_to_stam()
    repo = AlignmentRepo("AB3CAED2A", ROOT_DIR / "AB3CAED2A")
    # repo.upload_alignment_repo()
    repo.load_pecha_repos()
    repo.upload_aligned_pechas()
