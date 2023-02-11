import sys
import pytest
import os
import numpy as np
import unittest
import black


def main():
    print(f"Python version: {sys.version}")
    print(f"NumPy version: {np.__version__}")
    print(f"Pytest version: {pytest.__version__}")
    print(f"OS: {os.name}")
    print(f"Platform: {sys.platform}")

    # Initialize the test suite with coverage
    res = pytest.main(
        [
            "-v",
            "--junitxml=./tests/Reports/testsReport.xml",
            "--cov",
            "--cov-report=lcov:./tests/Reports/Coverage/lcov/lcov.info",
            "--cov-report=html:./tests/Reports/Coverage/html",
            "--cov-report=xml:./tests/Reports/Coverage/xml/coverage.xml",
            "-W ignore::DeprecationWarning",
            "tests",
        ]
    )

    # Black formatting of the code
    black.main(["src/BNumMet/", "tests", "Demos"])


if __name__ == "__main__":
    main()
