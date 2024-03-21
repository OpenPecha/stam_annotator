from pathlib import Path

from openpecha2.utils.opa_opf_loader import load_opf_annotations_from_yaml


def test_load_opf_with_one_annotation():
    data_folder = Path(__file__).parent.absolute() / "data"
    yaml_file_path = data_folder / "opf_author.yml"

    """ if opf file has only one annotation, an new annotation id is generated"""
    opf_annot = load_opf_annotations_from_yaml(yaml_file_path)

    expected_opf_annot = {
        "id": "5a54033501934d03bf5b8543542d9d6d",
        "annotation_type": "Author",
        "revision": "00001",
        "annotations": {"start": 19, "end": 83},
    }

    assert opf_annot["id"] == expected_opf_annot["id"]
    assert opf_annot["annotation_type"] == expected_opf_annot["annotation_type"]
    assert opf_annot["revision"] == expected_opf_annot["revision"]

    assert isinstance(
        opf_annot["annotations"], dict
    ), "Annotations must be a dictionary"

    first_annot = list(opf_annot["annotations"].values())[0]
    assert first_annot["span"] == expected_opf_annot["annotations"]


def test_load_opf_with_multiple_annotations():
    data_folder = Path(__file__).parent.absolute() / "data"
    yaml_file_path = data_folder / "opf_quotations.yml"
    opf_annot = load_opf_annotations_from_yaml(yaml_file_path)

    expected_opf_annot = {
        "id": "10eb4f16d43f41fe90064829cf241d18",
        "annotation_type": "Quotation",
        "revision": "00001",
        "annotations": {
            "a1f3e26bdb08449aaece0bba4ac4f5cc": {
                "span": {"start": 16302, "end": 16330}
            },
            "670003b927a54a5aad937c6ae0206e61": {
                "span": {"start": 16444, "end": 16450}
            },
            "4b95aa69bb6647d191e09a5e47dd5fa5": {
                "span": {"start": 17717, "end": 17770}
            },
        },
    }

    assert opf_annot["id"] == expected_opf_annot["id"]
    assert opf_annot["annotation_type"] == expected_opf_annot["annotation_type"]
    assert opf_annot["revision"] == expected_opf_annot["revision"]

    assert isinstance(
        opf_annot["annotations"], dict
    ), "Annotations must be a dictionary"

    assert opf_annot["annotations"] == expected_opf_annot["annotations"]


test_load_opf_with_one_annotation()
