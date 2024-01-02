# Getting started

Welcome to the stam annotator documentation. This document will help you get started
with the project.

## 1. Prerequisites

- github token is required that has the permission to access and download the
GitHub repository "PechaData".

The packages below are already listed in the `pyproject.toml` file. So you don't
need to install them manually.


- Python version 3.9 or higher
- stam version 0.3.1 or higher
- PyYAML version 6.0.1 or higher
- pydantic version 2.5.1 or higher
- PyGithub version 2.1.1 or higher


## 2. Installation

2.1 Create a virtual environment.

        python3 -m venv .venv

2.2 Activate the virtual environment.

2.2.1 For linux and mac

        source .venv/bin/activate

2.2.2 For windows

        .\venv\Scripts\activate


2.3  Install the package

        pip install git+https://github.com/OpenPecha/stam_annotator.git



## 3. Troubleshooting

When using this package, it's beneficial to be aware of the following key points:


- ***🌐Ensure a Stable Internet Connection:*** If you haven't specified a custom path for
downloading a pecha, it will be automatically downloaded and stored in a designated
directory on your local machine (refer to config.py). If the pecha containing the
required annotation isn't present in the directory, it will be fetched from the GitHub
 repository.

- ***📁Pecha ID you provid is valid Format:*** The pecha ID you provide must correspond
to one available in the GitHub repository.

- ***📁Verify Proper Format of Pecha Content Attributes:*** Data validation is performed
using the pydantic module to ensure the pecha content is in the correct format. If the
 content doesn't meet the format criteria, such as in an OPF file where the text offset
  start is less than the end, an error will occur.

For additional troubleshooting, refer to the (exceptions.py) file.
Further assistance is available here. [here](help.md).
