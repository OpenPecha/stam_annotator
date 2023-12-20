
# Usage

Getting started with the stam annotator is straightforward. This guide will assist you
in beginning your work with the project.

1. ***Instatiating an alignment(OPA) object with just ID.***

        from stam_annotator.alignment import Alignment

        alignment = Alignment.from_id("AB3CAED2A")
        for segment_pair in alignment.get_segment_pairs():
            print(segment_pair)



- This code snippet demonstrates how to import the necessary Alignment class and
    create an alignment (OPA) object.
- The from_id method is used here. It requires an alignment ID as a parameter and
    creates an object based on that ID.
- The created object features a get_segment_pairs method, which provides a list
    of segment pairs. Each pair in the list is a tuple comprising two elements:
    i. a text string, and ii. a language identifier.
- Note that alignment OPA and pecha OPFs(segment sources of the OPA) are downloaded automatically from the
    GitHub repository if they are not already present in the local directory.



2. ***Instatiating an alignment(OPA) object with ID and custom path.***

        from stam_annotator.alignment import Alignment

        alignment_path = Path("path/to/alignment")
        alignment = Alignment("AB3CAED2A", alignment_path)
        for segment_pair in alignment.get_segment_pairs():
            print(segment_pair)

- Similar to the first example, this code imports the Alignment class for creating
    an alignment (OPA) object.
- In this instance, the Alignment constructor is used, taking both the alignment ID and
    a custom path as arguments.If developers has a local copy of the alignment or an modified
    version of the alignment they can use this method to create an object.
- The resulting object also has the get_segment_pairs method, returning segment pairs
    as tuples of text strings and language identifiers.
- Note that the alignment OPA and pecha OPFs should already be present in the custom path
    provided when using this method.



    alignment = Alignment.from_id("AB3CAED2A")
    for segment_pair in alignment.get_segment_pairs():
        for text, language in segment_pair:
            print(f"{language}: {text}")

With slight modification to the first example, this code snippet would output the following

    sa: atha vā sarvabhāvānāṃ śūnyatvāc chāśvatādayaḥ | kva kasya katamāḥ kasmāt saṃbhaviṣyanti dṛṣṭayaḥ || 29 ||
    zh: 若亦有無邊 是二得成者 非有非無邊 是則亦應成
    bo: ཡང་ན་དངོས་པོ་ཐམས་ཅད་དག་༑་སྟོང་ཕྱིར་རྟག་ལ་སོགས་ལྟ་བ་༑་༑ གང་དག་གང་དུ་གང་ལ་ནི་༑་༑ ༼༧༽ཅི་ལས་ཀུན་ཏུ་འབྱུང་བར་འགྱུར་༑་༑
    en: 29. Because of the emptiness of all existing things, How will the views about “eternity,” etc., come into existence, about what, of whom, and of what kind?
