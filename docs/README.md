
# STAM ANNOTATOR

<!-- This is the project's homepage -->


The STAM Annotator is a Python package designed for working with annotations from
alignment (OPA) and pecha (OPF) repositories in "PechaData." PechaData is a GitHub page
containing data similar to OpenPecha-Data but in a format known as STAM.

## FILE FORMAT SPECIFICATION:

#### OpenPecha-Data:

In both OPA and OPF cases, the annotation files are stored in YAML format.

For OPF, the base file (which contains the text) is stored in TXT format and is located in
the same repository under the folder named "base."

#### PechaData:

In the case of OPA, the alignment files are stored in JSON format.

For OPF, the annotation files are stored in STAM format. The base file is also stored
in TXT format and is located in the same repository under the folder named "base".
Importantly, the content of the base file is also included inside the STAM JSON file.
This inclusion is necessary to generate the STAM file and to utilize the important
attributes of STAM.

## STAM:

The Stand-off Text Annotation Model (STAM) is a way of adding notes or comments to a text
 without changing the text itself. Imagine you have a page of writing and you want to make
  some notes about it. Instead of writing your notes directly on the page, you write them
  on a separate piece of paper and just refer to the part of the text you are talking
  about. This keeps the original text clean and unchanged. STAM is useful because you
  can add lots of different notes and comments to the same part of the text without
  making it confusing or cluttered. It's a helpful tool for anyone who needs to study or
   analyze texts in detail, like researchers or students.

For more information about STAM, please visit
[STAM](https://github.com/annotation/stam) and
[stam-python](https://github.com/annotation/stam-python).
