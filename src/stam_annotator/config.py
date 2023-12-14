from enum import Enum
from pathlib import Path

CUR_DIR = Path(__file__).parent.absolute()
ROOT_DIR = CUR_DIR.parent.parent.absolute()


class AnnotationEnum(Enum):
    index = "index"

    book_title = "BookTitle"
    sub_title = "SubTitle"
    book_number = "BookNumber"
    poti_title = "PotiTitle"
    author = "Author"
    chapter = "Chapter"

    topic = "Text"
    sub_topic = "SubText"

    pagination = "Pagination"
    language = "Language"
    citation = "Citation"
    correction = "Correction"
    error_candidate = "ErrorCandidate"
    peydurma = "Peydurma"
    pedurma_note = "PedurmaNote"
    sabche = "Sabche"
    tsawa = "Tsawa"
    yigchung = "Yigchung"
    archaic = "Archaic"
    durchen = "Durchen"
    footnote = "Footnote"
    segment = "Segment"
    ocr_confidence = "OCRConfidence"
    transcription_time_span = "TranscriptionTimeSpan"


class AnnotationGroupEnum(Enum):
    structure_type = "Structure Type"
    translation = "Translation"
