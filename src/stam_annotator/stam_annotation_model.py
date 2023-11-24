from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field

from stam_annotator.config import OPA_DIR
from stam_annotator.opa_annotations_loader import create_opa_annotation_instance


class Annotation_Data(BaseModel):
    id: str
    type: str
    relation: str
    lang: str
    base: str
    offset: str


class Annotation(BaseModel):
    id: str
    target: Dict
    data: Annotation_Data = Field(default_factory=Annotation_Data)


class Annotation_Data_Set(BaseModel):
    id: str
    key: str


class Resource(BaseModel):
    id: str
    text: str


class Annotation_Store(BaseModel):
    id: str
    datasets: List[Annotation_Data_Set] = Field(default_factory=Annotation_Data_Set)
    resources: List[Resource] = Field(default_factory=Resource)
    annotations: List[Annotation] = Field(default_factory=Annotation)


if __name__ == "__main__":
    annotationstore_id = "SegmentAnnotations"
    segment_yaml_path = OPA_DIR / "36CA.yml"

    segment_data = create_opa_annotation_instance(Path(segment_yaml_path))
    print(segment_data.segment_sources)
