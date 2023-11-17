from pathlib import Path

from stam_annotator.load_yaml_annotations import load_opf_annotations_from_yaml
from stam_annotator.opf_annotations_loader import create_opf_annotation_instance


def test_create_annotation_loader():
    # opf_author.yml has only one annotation
    yaml_file_path = Path(__file__).parent.absolute() / "data" / "opf_author.yml"
    yaml_content = load_opf_annotations_from_yaml(yaml_file_path)

    annotation_doc = create_opf_annotation_instance(yaml_content)
    assert annotation_doc.id == "5a54033501934d03bf5b8543542d9d6d"
    assert annotation_doc.annotation_type == "Author"
    assert annotation_doc.revision == "00001"
    for uuid, annotation in annotation_doc.annotations.items():
        if uuid == "0":
            start, end = annotation.span.start, annotation.span.end
            assert start == 19
            assert end == 83

    # opf_quotations.yml has more than one annotation
    yaml_file_path = Path(__file__).parent.absolute() / "data" / "opf_quotations.yml"
    yaml_content = load_opf_annotations_from_yaml(yaml_file_path)

    annotation_doc = create_opf_annotation_instance(yaml_content)
    assert annotation_doc.id == "10eb4f16d43f41fe90064829cf241d18"
    assert annotation_doc.annotation_type == "Quotation"
    assert annotation_doc.revision == "00001"
    for uuid, annotation in annotation_doc.annotations.items():
        if uuid == "a1f3e26bdb08449aaece0bba4ac4f5cc":
            start, end = annotation.span.start, annotation.span.end
            assert start == 16302
            assert end == 16302
        if uuid == "670003b927a54a5aad937c6ae0206e61":
            start, end = annotation.span.start, annotation.span.end
            assert start == 16444
            assert end == 16444

    # print(f"id: {annotation_doc.id}")
    # print(f"annotation_type: {annotation_doc.annotation_type}")
    # print(f"revision: {annotation_doc.revision}")
    # for uuid, value in annotation_doc.annotations.items():
    #     print(f"uuid: {uuid}, start:{value.span.start} - end:{value.span.end}")


if __name__ == "__main__":
    test_create_annotation_loader()
