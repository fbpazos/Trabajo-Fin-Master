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

Linux
-------
```bash
python3 -m venv venv # Create a virtual environment
source venv/bin/activate # Activate the virtual environment
```
Windows
-------
```cmd
python -m venv venv # Create a virtual environment
venv\Scripts\activate # Activate the virtual environment
```
Python Side
-------
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
# It will also format the code using the Black Library (I Might've forgottent to do so :) )
```

## SonarQube
In order to run the SonarQube analysis, you can use the following command:

Start the SonarQube server (Docker Version)
-------
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube
```
Since its running locally, you can access the server at http://localhost:9000, and the default credentials are admin/admin. 
Additionally, for simplicity with login go to Administration -> Security -> Disable "Force User Authentication". ()


Run the analysis
-------
Linux 
```bash
docker run --rm -ti -v "%cd%":"/usr/src" --link sonarqube newtmitch/sonar-scanner sonar-scanner /
    -Dsonar.projectName="BNumMet" /
    -Dsonar.projectKey="BNumMet" /
    -Dsonar.sources="src/BNumMet/" /
    -Dsonar.python.version=3 /
    -Dsonar.python.xunit.reportPath="tests/Reports/testsReport.xml"  /
    -Dsonar.python.coverage.reportPaths="tests/Reports/Coverage/xml/coverage.xml" /
    -Dsonar.scm.disabled=true /
    -Dsonar.tests="tests" /
    -Dsonar.test.inclusions="tests/**" /
    -Dsonar.test.exclusions="tests/Reports/Coverage/**"
```

Windows - just replace "$(pwd)" with "%cd%" 

```cmd
docker run --rm -ti -v "%cd%":"/usr/src" --link sonarqube newtmitch/sonar-scanner 
sonar-scanner ^
-Dsonar.projectName="BNumMet" ^
-Dsonar.projectKey="BNumMet" ^
-Dsonar.sources="src/BNumMet/" ^
-Dsonar.python.version=3 ^
-Dsonar.python.xunit.reportPath="tests/Reports/testsReport.xml"  ^
-Dsonar.python.coverage.reportPaths="tests/Reports/Coverage/xml/coverage.xml" ^
-Dsonar.scm.disabled=true ^
-Dsonar.tests="tests" ^
-Dsonar.test.inclusions="tests/**" ^
-Dsonar.test.exclusions="tests/Reports/Coverage/**"
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

 

