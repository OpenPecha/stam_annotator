import yaml

from stam_annotator.definations import OPF_DIR
from stam_annotator.utility import get_uuid


def load_opf_annotations_from_yaml(yaml_file):
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

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


if __name__ == "__main__":
    # Load YAML annotations
    yaml_annotations = load_opf_annotations_from_yaml(OPF_DIR / "Quotation.yml")
    print(yaml_annotations)
