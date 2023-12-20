# Getting started

Welcome to the stam annotator documentation. This document will help you get started
with the project.

## 1. Prerequisites

all the prerequisites are listed in the `pyproject.toml` file. You can jump to
step 2.

- Python version 3.9 or higher
- stam version 0.3.1 or higher
- PyYAML version 6.0.1 or higher
- pydantic version 2.5.1 or higher
- PyGithub version 2.1.1 or higher

## 2. Installation

2.1 create a virtual environment.

        python3 - venv .venv

2.2 activate the virtual environment.

2.2.1 For linux and mac

        source .venv/bin/activate

2.2.2 For windows

        .\venv\Scripts\activate


2.3  install the package

        pip install git+https://github.com/OpenPecha/stam_annotator.git



## 3. Troubleshooting

When using this package, it's beneficial to be aware of the following key points:


- ***🌐Ensure a Stable Internet Connection:***If you haven't specified a custom path for
downloading a pecha, it will be automatically downloaded and stored in a designated
directory on your local machine (refer to config.py). If the pecha containing the
required annotation isn't present in the directory, it will be fetched from the GitHub
 repository.

- ***📁Pecha ID you provid is valid Format:***The pecha ID you provide must correspond
to one available in the GitHub repository.

- ***📁Verify Proper Format of Pecha Content Attributes:***Data validation is performed
using the pydantic module to ensure the pecha content is in the correct format. If the
 content doesn't meet the format criteria, such as in an OPF file where the text offset
  start is less than the end, an error will occur.

For additional troubleshooting, refer to the (exceptions.py) file.
Further assistance is available here. [here](help.md).
