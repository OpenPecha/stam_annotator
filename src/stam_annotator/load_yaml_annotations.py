import yaml

from stam_annotator.config import OPF_DIR


def load_opf_annotations_from_yaml(yaml_file):
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    # Check if the annotations are a list and convert to a dictionary if so
    if isinstance(data["annotations"], list):
        # Convert list to dictionary with index-based keys or some form of UUIDs
        data["annotations"] = {
            f"{index}": item for index, item in enumerate(data["annotations"])
        }

    return data


if __name__ == "__main__":
    # Load YAML annotations
    yaml_annotations = load_opf_annotations_from_yaml(OPF_DIR / "Chapter.yml")
    print(yaml_annotations)
