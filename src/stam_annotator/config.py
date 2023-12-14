from enum import Enum
from pathlib import Path

CUR_DIR = Path(__file__).parent.absolute()
ROOT_DIR = CUR_DIR.parent.parent.absolute()


class ValueEnum(Enum):
    author = "Author"
    book_title = "BookTitle"
    chapter = "Chapter"
    quotation = "Quotation"
    sabche = "Sabche"
    tsawa = "Tsawa"
    yigchung = "Yigchung"

    correction = "Correction"
    pagination = "Pagination"
    error_candidate = "ErrorCandidate"
    peydurma = "Peydurma"

    segment = "Segment"


class KeyEnum(Enum):
    structure_type = "Structure Type"
    translation = "Translation"
