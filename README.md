# Trabajo Fin Master
![Python Tests](https://github.com/fbellidopazos/Trabajo-Fin-Master/actions/workflows/PythonTests.yml/badge.svg)
![Latex Compile](https://github.com/fbellidopazos/Trabajo-Fin-Master/actions/workflows/LatexCompilation.yml/badge.svg)
[![Upload Python Package](https://github.com/fbpazos/Trabajo-Fin-Master/actions/workflows/PythonPublish.yml/badge.svg)](https://github.com/fbpazos/Trabajo-Fin-Master/actions/workflows/PythonPublish.yml)
Github Repository for the Master's Thesis of Applied and Computational Mathematics at Universidad Carlos III de Madrid
 
 ## Folder Structure
 ```
.
├── .github : Folder for GitHub Actions
├── LICENSE
├── Latex : Folder for Latex Files - Document for Thesis
├── Python_BNumMet : Folder for Python Package
└── README.md 
```

## GitHub Actions
It is important to remark that every time someone updates this repository two things will activate
1. Python Tests - Github Action : It will run all tests inside "Python_BNumMet" in 3 OS with 4 Python Versions
2. Latex Compile - Github Action : It will latex-compule the main file and output it in the action
