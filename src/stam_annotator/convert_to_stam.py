import json
import shutil
import subprocess
from datetime import datetime
from json import JSONEncoder
from pathlib import Path
from typing import Dict, List

import yaml

from stam_annotator.definations import ROOT_DIR
from stam_annotator.github_token import GITHUB_TOKEN


class Repo:
    alignment_id: str
    source_org: str
    destination_org: str

    def __init__(self, id_: str, source_org: str, destination_org: str):
        self.alignment_id = id_
        self.source_org = source_org
        self.destination_org = destination_org
        self.base_path = make_local_folder(ROOT_DIR / self.alignment_id)

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
                    yml_content = Path(parent_dir / doc).read_text(encoding="utf-8")
                    opa_json = json.dumps(
                        yaml.safe_load(yml_content), indent=4, cls=CustomEncoder
                    )
                    Path(new_parent_dir / doc.replace(".yml", ".json")).write_text(
                        opa_json
                    )
                    continue

                shutil.copy(parent_dir / doc, new_parent_dir / doc)
                continue


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


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format the date however you like
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)


if __name__ == "__main__":
    repo = Repo("AB3CAED2A", "OpenPecha-Data", "tenzin3")
    # repo.get_alignment_repo()
    repo.convert_alignment_repo_to_json()
