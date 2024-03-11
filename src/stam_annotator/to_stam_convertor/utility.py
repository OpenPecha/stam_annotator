import json
import subprocess
from datetime import datetime
from json import JSONEncoder
from pathlib import Path
from typing import Dict, List

import yaml
from github import Github


def create_folder_if_not_exists(folder_path):
    """
    Create a folder at the given path if it does not exist.
    This also creates any necessary parent folders.

    :param folder_path: Path of the folder to be created.
    """
    path = Path(folder_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def clone_github_repo(
    org_name: str, repo_name: str, destination_folder: Path, token: str
):
    if destination_folder.exists() and list(destination_folder.rglob("*")):
        print(
            f"[INFO]: Destination folder {destination_folder} already exists and is not empty."
        )
    else:
        try:
            repo_url = f"https://{token}@github.com/{org_name}/{repo_name}.git"
            subprocess.run(
                ["git", "clone", repo_url, str(destination_folder)],
                check=True,
                capture_output=True,
            )
            print(
                f"[INFO]: Repository {repo_name} cloned successfully into {destination_folder}"
            )

        except subprocess.CalledProcessError as e:
            print(f"[ERROR]: Error cloning {repo_name} repository: {e}")


def create_github_repo(org_name: str, repo_name: str, token: str) -> bool:
    try:
        g = Github(token)
        org = g.get_organization(org_name)
        org.create_repo(repo_name)
        print(f"[SUCCESS]: Repository {repo_name} created successfully")
        return True
    except:  # noqa
        print(f"[INFO]: Repo {repo_name} already exists")
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


def replace_parent_folder_name(path: Path, old_name: str, new_name: str) -> Path:
    """Replace the parent folder name of the path with the new name"""

    parts = path.parts
    layers_dir = "layers"
    """if there are folders(volume name) presented in layers dir, then the path is trimmed"""
    if layers_dir in parts:
        index = parts.index(layers_dir)
        trimmed_path = Path(*parts[: index + 1])
    else:
        trimmed_path = path

    return Path(str(trimmed_path).replace(old_name, new_name))


def convert_yml_file_to_json(yml_file_path: Path, json_output_path: Path):
    yml_content = yml_file_path.read_text(encoding="utf-8")
    converted_json = json.dumps(
        yaml.safe_load(yml_content), indent=4, cls=CustomEncoder
    )
    json_output_path.write_text(converted_json)


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format the date however you like
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)
