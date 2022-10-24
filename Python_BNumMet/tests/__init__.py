import sys
import pytest 
import os
import numpy as np
import unittest



def main():
    # Initialize the test suite with coverage
    res = pytest.main(
        [
            "-v",
            "--cov",
            "--cov-report=lcov:Coverage/lcov/lcov.info",
            "--cov-report=html:Coverage/html",
            "--cov-report=xml:Coverage/xml/coverage.xml",
             "-W ignore::DeprecationWarning",
            "tests"
            ]
    )




if __name__ == '__main__':
    main()
