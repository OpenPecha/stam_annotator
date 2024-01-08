import csv
import logging
from pathlib import Path
from typing import Dict, List

import requests
from github import Github

from stam_annotator.config import ROOT_DIR
from stam_annotator.convert_to_stam import PechaRepo

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


def categorize_strings_by_initial(strings: List[str]) -> Dict[str, List[str]]:
    categorized_strings: Dict[str, List[str]] = {}
    for string in strings:
        initial_char = string[0]
        if initial_char not in categorized_strings:
            categorized_strings[initial_char] = []
        categorized_strings[initial_char].append(string)
    return categorized_strings


def convert_opf_files_to_stam(pecha_ids: List[str]):
    for pecha_id in pecha_ids:
        try:
            pecha_repo = PechaRepo.from_id(pecha_id)
            pecha_repo.get_pecha_repo()
            pecha_repo.convert_pecha_repo_to_stam()
        except Exception as e:
            logging.error(f"pecha id: {pecha_id}, {e}")


logging.basicConfig(
    level=logging.ERROR,  # Set the log level to ERROR or the desired level
    filename="convertion_errors.log",  # Specify the log file
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    opf_catalog_file_path = ROOT_DIR / "data" / "opf_catalog.csv"
    pecha_ids = extract_column_from_csv(opf_catalog_file_path, "Pecha ID")
    categorized_pecha_ids = categorize_strings_by_initial(pecha_ids)
    initial_D_pecha_ids = categorized_pecha_ids["D"]
    convert_opf_files_to_stam(initial_D_pecha_ids)
