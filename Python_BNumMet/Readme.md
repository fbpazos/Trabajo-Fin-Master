# BasicLineAlg
- Title: BNumMet
- Author: [Fernando Bellido Pazos](fbellidopazos@gmail.com)
- Date: 2022
- Version: 0.1
- License: ??
- Description: Basic Numerical Methods For Python 3
- Tags: 
- URL: [Trabajo Fin de Master](https://github.com/fbellidopazos/Trabajo-Fin-Master)

## Introduction

## Installation
In order to install the package, you can use the following command:

```bash
pip install bnummet # This is not yet available
```


## Usage



## Examples


## Tests
We recommend to use a virtual environment to install the package. To do so, you can use the following commands:

```bash
python3 -m venv venv # Create a virtual environment
source venv/bin/activate # Activate the virtual environment
```

Then, you can test the package using the following command:


```bash
pip install -r requirements_dev.txt # Install development dependencies (test libraries)
pip install -e . # Installs the package in editable mode
pytest -W ignore::DeprecationWarning  # Run tests without Warnings
```
Or, alternatively, you can use the \_\_init\_\_.py file to run the tests.

```bash
pip install requirements_dev.txt # Install development dependencies (test libraries)
pip install -e . # Installs the package in editable mode
python tests/__init__.py # Run tests

# It will generate a coverage report in the Tests/coverage folder in different formats (html, xml, lcov).
```

## BNumMet - Structure
```bash
.
├── Interpolation.py # Interpolation algorithms
├── LinearEquations.py # Linear equations algorithms
├── Visualizers # Visualizers
│   ├── InterpolationVisualizer.py
│   └── LUVisualizer.py
├── Zeros.py # Root-Fingind algorithms
├── __init__.py
└── module.py # Quality of life functions
```

 

