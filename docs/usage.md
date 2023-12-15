
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



2. ***Instatiating an alignment(OPA) object with ID and custom path.***

        from stam_annotator.alignment import Alignment

        alignment_path = Path("path/to/alignment")
        alignment = Alignment("AB3CAED2A", alignment_path)
        for segment_pair in alignment.get_segment_pairs():
            print(segment_pair)

    - Similar to the first example, this code imports the Alignment class for creating
        an alignment (OPA) object.
    - In this instance, the Alignment constructor is used, taking both the alignment ID and
         a custom path as arguments.
    - The resulting object also has the get_segment_pairs method, returning segment pairs
        as tuples of text strings and language identifiers.
