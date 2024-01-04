import csv
from pathlib import Path
from typing import Dict, List

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


def extract_column_from_csv(csv_file_path, column_name) -> list:
    column_values = []
    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if column_name in row:
                column_values.append(row[column_name])
    return column_values


def categorize_file_names_by_initial(file_names: List[str]) -> Dict[str, List[str]]:
    categorized_file_names: Dict[str, List[str]] = {}
    for file_name in file_names:
        initial = file_name[0]
        if initial not in categorized_file_names:
            categorized_file_names[initial] = []
        categorized_file_names[initial].append(file_name)
    return categorized_file_names


if __name__ == "__main__":
    opf_catalog_file_path = ROOT_DIR / "data" / "opf_catalog.csv"
    file_names = extract_column_from_csv(opf_catalog_file_path, "Pecha ID")
    categorized_file_names = categorize_file_names_by_initial(file_names)
    for initial, file_names in categorized_file_names.items():
        print(initial, len(file_names))
