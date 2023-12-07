import json
from pathlib import Path
from typing import Dict, Union
from uuid import uuid4

import stam
import yaml
from github import Github
from stam import Annotations, AnnotationStore

from stam_annotator.definations import CUR_DIR


def get_filename_without_extension(file_path: Union[str, Path]):
    return Path(file_path).stem


def is_json_file_path(file_path: Path) -> bool:
    return file_path.suffix == ".json"


def get_uuid():
    return uuid4().hex


def read_json_to_dict(file_path: Path) -> Dict:
    if not is_json_file_path(file_path):
        raise ValueError(f"The file path must lead to a JSON file. Given: {file_path}")
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def convert_none_to_null_in_annotations(data):
    """
    if a value is null in yml file, it will be converted to None in python.
    and None has no value to show in annotation, so this convert None to
    string type 'null'.
    """
    if "annotations" in data and isinstance(data["annotations"], dict):
        for key, value in data["annotations"].items():
            data["annotations"][key] = {
                k: "null" if v is None else v for k, v in value.items()
            }
    return data


def load_opf_annotations_from_yaml(yaml_file):
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
        data = convert_none_to_null_in_annotations(data)

    # Check if 'annotations' key exists in the data
    if "annotations" not in data:
        data["annotations"] = {}
    elif isinstance(data["annotations"], list):
        # Convert list to dictionary with index-based keys or some form of UUIDs
        annotation_id = get_uuid()
        data["annotations"] = {
            f"{annotation_id}": item for index, item in enumerate(data["annotations"])
        }

    return data


def load_opa_annotations_from_yaml(yaml_file):
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    return data


def save_annotation_store(store: AnnotationStore, output_file_path: Union[str, Path]):
    output_file_path = Path(output_file_path)

    # Check if the file extension is .json
    if not is_json_file_path(output_file_path):
        raise ValueError(
            f"The file path must lead to a JSON file. Given: {output_file_path}"
        )

    store.set_filename(str(output_file_path))
    store.save()


def save_json_file(data: Dict, output_file_path: Union[str, Path]):
    output_file_path = Path(output_file_path)

    # Check if the file extension is .json
    if not is_json_file_path(output_file_path):
        raise ValueError(
            f"The file path must lead to a JSON file. Given: {output_file_path}"
        )

    with open(output_file_path, "w") as f:
        json.dump(data, f, indent=4)


def convert_opf_stam_annotation_to_dictionary(
    annotations: Annotations, include_payload: bool = True
) -> Dict:
    """
    This function converts the annotation object to a dictionary.
    """
    annotation_dict = {}
    for annotation in annotations:
        # get the text to which this annotation refers (if any)
        text = str(annotation) if not isinstance(annotation, stam.StamError) else "n/a"
        for data in annotation:
            annotation_dict[annotation.id()] = {
                "id": annotation.id(),
                "key": data.key().id(),
                "value": str(data.value()),
                "text": text,
            }
            if include_payload:
                payload_dictionary = {}
                for annot in annotation.annotations():
                    for data in annot:
                        payload_dictionary[data.key().id()] = {
                            "id": annot.id(),
                            "value": str(data.value()),
                        }
                annotation_dict[annotation.id()]["payload"] = payload_dictionary
    return annotation_dict


def get_files_from_opa_repo(organization, repo_name, token):
    g = Github(token)
    repo = g.get_repo(f"{organization}/{repo_name}")
    repo_files = repo.get_contents(f"{repo_name}.opa")
    return repo_files


def json_alignment_exists_in_repo(organization, repo_name, token):
    repo_files = get_files_from_opa_repo(organization, repo_name, token)
    if any(file.name == f"{repo_name}.opa.json" for file in repo_files):
        return True
    return False


def get_json_alignment(organization, repo_name, token):
    repo_files = get_files_from_opa_repo(organization, repo_name, token)
    json_alignment = next(file.name == f"{repo_name}.opa.json" for file in repo_files)
    Path(CUR_DIR / json_alignment.name).write_text(json_alignment.decoded_content)

    return CUR_DIR


def make_json_alignment(organization, repo_name, token):
    """get yml alignment from github repo and convert it to json"""
    g = Github(token)
    repo = g.get_repo(f"{organization}/{repo_name}")
    repo_files = repo.get_contents(f"{repo_name}.opa")
    yml_alignment = next(file.name != "meta.yml" for file in repo_files)
    json_content = json.dumps(yml_alignment.decoded_content, indent=4)
    Path(CUR_DIR / f"{repo_name}.opa.json").write_text(json_content)

    return CUR_DIR
