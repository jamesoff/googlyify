# Googlyify

Draw googly eyes on people using Amazon Rekognition.

## Prerequisites

* AWS credentials configured
* Python >= 3.9
* optional: [Poetry](https://python-poetry.org/) installed

## Setup

1. Clone repo
1. If you don't intend to work on the code
    1. If you have Poetry installed, `poetry install --no-dev`
    1. Else create a virtualenv and install with pip: `python -m virtualenv .venv && source .venv/bin/activate && pip install .`
1. else if you intend to work on the code, `poetry install`

## Usage

With a suitable input file (less than 5MB, png or jpg)

```
poetry run python googlyify.py input.jpg output.jpg
```

or if using the virtualenv directly,

```
python googlyify.py input.jpg output.jpg
```

`output.jpg` is overwritten with the result.
