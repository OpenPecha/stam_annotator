import yaml

from stam_annotator.config import DATA_DIR


# Function to load annotations from a YAML file
def load_annotations_from_yaml(yaml_file):
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    return data


if __name__ == "__main__":
    # Load YAML annotations
    yaml_annotations = load_annotations_from_yaml(DATA_DIR / "Author.yml")
    print(yaml_annotations)
