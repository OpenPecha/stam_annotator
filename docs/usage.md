
# Usage

## Alignment (OPA) Repository

Getting started with the stam annotator is straightforward. This guide will assist you
in beginning your work with the project.

1. ***Instatiating an alignment(OPA) object with just ID.***

```python
from stam_annotator.alignment import Alignment

alignment = Alignment.from_id("AB3CAED2A", github_token)
for segment_pair in alignment.get_segment_pairs():
    print(segment_pair)
```


- This code snippet demonstrates how to import the necessary Alignment class and
    create an alignment (OPA) object.
- The from_id method is used here. It requires an alignment ID and github token
    creates an object based on that ID.
- The created object features a get_segment_pairs method, which provides a list
    of segment pairs. Each pair in the list is a tuple comprising two elements:
    i. a text string, and ii. a language identifier.
- Note that alignment OPA and pecha OPFs(segment sources of the OPA) are downloaded automatically from the
    GitHub repository if they are not already present in the local directory.



2. ***Instatiating an alignment(OPA) object with ID and custom path.***

```python
from stam_annotator.alignment import Alignment

alignment_path = Path("path/to/alignment")
alignment = Alignment("AB3CAED2A", github_token, alignment_path)
for segment_pair in alignment.get_segment_pairs():
    print(segment_pair)
```

- Similar to the first example, this code imports the Alignment class for creating
    an alignment (OPA) object.
- In this instance, the Alignment constructor is used, taking both the alignment ID and
    a custom path as arguments.If developers has a local copy of the alignment or an modified
    version of the alignment they can use this method to create an object.
- The resulting object also has the get_segment_pairs method, returning segment pairs
    as tuples of text strings and language identifiers.
- Note that the alignment OPA and pecha OPFs should already be present in the custom path
    provided when using this method.
- Here the github token is taken so that if any of the pecha OPFs are missing in the
  custom path, then it will download from the github "PechaData".


```python
alignment = Alignment.from_id("AB3CAED2A", github_token)
for segment_pair in alignment.get_segment_pairs():
    for text, language in segment_pair:
        print(f"{language}: {text}")
```

With slight modification to the first example, this code snippet would output similar to below
format:

```python
sa: atha vā sarvabhāvānāṃ śūnyatvāc chāśvatādayaḥ | kva kasya katamāḥ kasmāt saṃbhaviṣyanti dṛṣṭayaḥ || 29 ||
zh: 若亦有無邊 是二得成者 非有非無邊 是則亦應成
bo: ཡང་ན་དངོས་པོ་ཐམས་ཅད་དག་༑་སྟོང་ཕྱིར་རྟག་ལ་སོགས་ལྟ་བ་༑་༑ གང་དག་གང་དུ་གང་ལ་ནི་༑་༑ ༼༧༽ཅི་ལས་ཀུན་ཏུ་འབྱུང་བར་འགྱུར་༑་༑
en: 29. Because of the emptiness of all existing things, How will the views about “eternity,” etc., come into existence, about what, of whom, and of what kind?
```


2. ***Fetching meta data from alignment(OPA)***

```python
alignment = Alignment.from_id("AB3CAED2A", github_token)
meta_data = alignment.get_meta_data()
for key, value in meta_data.items():
    print(f"{key}:", value)
```


*Note that if the alignment does not contain any meta data then it will return an empty dictionary.*

The above code snippet will output the following:

```
id: AB3CAED2A
title: Nāgārjuna: Mūlamadhyamakakārikā
type: translation
pechas: ['I1A92E2D9', 'I5E597420', 'I96CFA399', 'IB44CB601', 'ID5FCF98D', 'I1E23F295', 'I060C85E6', 'IB0995F57', 'I998010B3', 'I9D4ABAEF']
source_metadata: {'languages': ['sa', 'zh', 'bo', 'en'], 'datatype': 'PlainText', 'created_at': '2023-02-10 00:31:44', 'last_modified_at': '2023-02-10 00:31:44'}
alignment_to_base: {'I1A92E2D9/ABFB': '9103', 'I5E597420/894F': '9103', 'I96CFA399/13AB': '9103', 'IB44CB601/308F': '9103', 'ID5FCF98D/1018': '9103', 'I1E23F295/5E06': '9103', 'I060C85E6/8BA2': '9103', 'IB0995F57/2087': '9103', 'I998010B3/C8EC': '9103', 'I9D4ABAEF/44E4': '9103'}
```



## Pecha (OPF) Repository

1. ***Instatiating an pecha(OPF) object with just ID.***

```python
from stam_annotator.alignment import Pecha

pecha_repo = Pecha.from_id("I96CFA399", github_token)
annotations = pecha_repo.get_annotations()

```

- The above ID "I96CFA399" is one of the pecha related to above alignment with
  ID "AB3CAED2A".
- This code snippet demonstrates how to import the necessary Pecha class and
    create an Pecha (OPF) object.
- The from_id method is used here. It requires an pecha ID and github token
    creates an object based on that ID.
- The method get_annotations() returns a dictionary with annotation_id as key and annotation
    text, its annotation group and annotation type as value.
- If payloads such as page number,... are present in the pecha OPF then it will
    also be included in the dictionary in the feature 'payloads'.
- Note that pecha OPF is downloaded automatically from the
    GitHub repository if they are not already present in the local directory.

```python
for key, value in annotations.items():
    print(key, value)
```
With a simple code to print the dictionary we get the following output:

```
64e5e6da40f74b34a74e85061e5d12eb {'text': '༼༡ཨ༡༽རྒྱ་གར་སྐད་དུ་༑་༑་པྲ་ཛཉའ་ནའ་མ་མའུ་ལ་མ་དྷཡའ་མ་ཀ་ཀའ་རི་ཀ་༑་བོད་སྐད་དུ་༑་༑་དབུ་མ་རྩ་བའི་ཚིག་ལེའུར་བྱས་པ་ཤེས་རབ་ཅེས་བྱ་བ་༑', 'annotation_group': 'Structure Type', 'annotation': 'Segment'}
3455712c037c4992a00f8f21ff533773 {'text': 'འཇམ་དཔལ་གཞོན་ནུར་གྱུར་པ ༼༢༽ལ་ཕྱག་འཚལ་ལོ་༑་༑', 'annotation_group': 'Structure Type', 'annotation': 'Segment'}
efa17c3f05854dc6947e05648aa20f3f {'text': 'གང་གིས་རྟེན་ཅིང་འབྲེལ་པར་འབྱུང་༑་༑་འགག་པ་མེད་པ་སྐྱེ་མེད་པ་༑་༑ ཆད་པ་མེད་པ་རྟག་མེད་པ་༑་༑་འོང་བ་མེད་པ་འགྲོ་མེད་པ་༑་༑ ཐ་དད་དོན་མིན་དོན་གཅིག་མིན་༑་༑ ༼༣༽སྤྲོས་པ་ཉེར་ཞི་ཞི་བསྟན་པ་༑་༑ རྫོགས་པའི་སངས་རྒྱས་སྨྲ་རྣམས་ཀྱི་༑་༑་དམ་པ་དེ་ལ་ཕྱག་འཚལ་ལོ་༑་༑', 'annotation_group': 'Structure Type', 'annotation': 'Segment'}
9247779d2d5f41b2bee43cd3474b9814 {'text': 'བདག་ལས་མ་ཡིན་གཞན་ལས་མིན་༑་༑་གཉིས་ལས་མ་ཡིན་རྒྱུ་མེད་མིན་༑་༑ དངོས་པོ་གང ༼༤༽དག་གང་ན་ཡང་༑་༑་སྐྱེ་བ་ནམ་ཡང་ཡོད་མ་ཡིན་༑་༑', 'annotation_group': 'Structure Type', 'annotation': 'Segment'}
fbb8ee887213447aa4f7ea6292880cc4 {'text': 'རྐྱེན་རྣམ་བཞི་སྟེ་རྒྱུ་དང་ནི་༑་༑་དམིགས་པ་དང་ནི་དེ་མ་ཐག་༑་༑ བདག་པོ་ཡང་ནི་དེ་བཞིན་ཏེ་༑་༑་རྐྱེན་ལྔ་པ་ནི་ཡོད་མ་ཡིན་༑་༑', 'annotation_group': 'Structure Type', 'annotation': 'Segment'}
1c962467f2e54424a3b8bfaf2c146b49 {'text': 'དངོས་པོ་རྣམས་ཀྱི ༼༥༽རང་བཞིན་ནི་༑་༑་རྐྱེན་ལ་སོགས་ལ་ཡོད་མ་ཡིན་༑་༑ བདག་གི་དངོས་པོ་ཡོད་མིན་ན་༑་༑་གཞན་དངོས་ཡོད་པ་མ་ཡིན་ནོ་༑་༑', 'annotation_group': 'Structure Type', 'annotation': 'Segment'}
```


2. ***Instatiating an pecha(OPF) object ID and custom path.***

```python
from stam_annotator.alignment import Pecha

pecha_path = Path("path/to/pecha")
pecha_repo = Pecha.from_id("I96CFA399", pecha_path)
annotations = pecha_repo.get_annotations()

```

- The above ID "I96CFA399" is one of the pecha related to above alignment with
  ID "AB3CAED2A".
- This code snippet demonstrates how to import the necessary Pecha class and
    create an Pecha (OPF) object.
- Here the pecha object is created with  ID and custom path.
- The method get_annotations() returns a dictionary with annotation_id as key and annotation
    text, its annotation group and annotation type as value.

3. ***Filtering annotations from pecha(OPF)***


```python
from stam_annotator.config import AnnotationGroupEnum, AnnotationEnum

pecha_repo = Pecha.from_id("P000216", github_token)
annotation_group = AnnotationGroupEnum.structure_type
annotation_type = AnnotationEnum.author
annotations = pecha_repo.get_annotations(annotation_group, annotation_type)
for key, value in annotations.items():
    print(key, value)
```

- To filter the annotations from the pecha object we need to pass the annotation group
    and annotation type.
- The annotation group and type must be from the AnnotationGroupEnum and AnnotationEnum
    respectively.
- Below are the list of annotation groups and types available in the pecha repository.

```
class AnnotationGroupEnum(Enum):
    structure_type = "Structure Type"
    translation = "Translation"


class AnnotationEnum(Enum):
    index = "index"
    book_title = "BookTitle"
    sub_title = "SubTitle"
    book_number = "BookNumber"
    poti_title = "PotiTitle"
    author = "Author"
    chapter = "Chapter"
    quotation = "Quotation"
```
