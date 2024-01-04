from pathlib import Path

import requests
from github import Github

from stam_annotator.config import ROOT_DIR

REPO_OWNER = "OpenPecha-Data"
REPO_NAME = "catalog"

OPA_OPF_CATALOG_FILE_NAMES = ["opa_catalog.csv", "opf_catalog.csv"]


def download_openpecha_opa_opf_catalog(token, destination_folder_path: Path):
    if not destination_folder_path.exists():
        destination_folder_path.mkdir(parents=True)
    try:
        g = Github(token)
        repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
        file_names = repo.get_contents("")
        for file_name in file_names:
            if file_name.name in OPA_OPF_CATALOG_FILE_NAMES:
                download_file_with_link(
                    file_name.download_url, destination_folder_path / file_name.name
                )
    except Exception as e:
        print(e)


def download_file_with_link(url, destination_folder_path: Path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination_folder_path, "w", newline="", encoding="utf-8") as file:
            file.write(response.text)
        print(f"file downloaded: {destination_folder_path}")
    else:
        print(f"Failed to download: {response.status_code}")


if __name__ == "__main__":
    from stam_annotator.github_token import GITHUB_TOKEN

    destination_folder_path = ROOT_DIR / "data"
    download_openpecha_opa_opf_catalog(GITHUB_TOKEN, destination_folder_path)
