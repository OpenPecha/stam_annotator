from pathlib import Path

from stam_annotator.load_yaml_annotations import load_annotations_from_yaml


def test_load_annotations_from_yaml():
    # opf_author.yml has only one annotation
    yaml_file_path = Path(__file__).parent.absolute() / "data" / "opf_author.yml"
    yaml_annotations = load_annotations_from_yaml(yaml_file_path)
    assert yaml_annotations["id"] == "73d9280f0b9448ed981250b232e0f411"
    assert yaml_annotations["annotation_type"] == "Author"
    assert yaml_annotations["revision"] == "00001"
    assert yaml_annotations["annotations"][0]["span"]["start"] == 113
    assert yaml_annotations["annotations"][0]["span"]["end"] == 137

    # opf_quotations.yml has more than one annotation
    yaml_file_path = Path(__file__).parent.absolute() / "data" / "opf_quotations.yml"
    yaml_annotations = load_annotations_from_yaml(yaml_file_path)
    assert yaml_annotations["id"] == "f4ab2bb05e7d4757bf65c6d06046cf76"
    assert yaml_annotations["annotation_type"] == "Quotation"
    assert yaml_annotations["revision"] == "00001"
    assert yaml_annotations["annotations"]["21f9e2dafb3a48dc9d7c34e22fa60eb9"] == {
        "span": {"start": 45402, "end": 45527}
    }
    assert yaml_annotations["annotations"]["1466fe93cebb4c69b38c09dec2fad984"] == {
        "span": {"start": 96462, "end": 96587}
    }


if __name__ == "__main__":
    test_load_annotations_from_yaml()
