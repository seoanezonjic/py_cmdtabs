#! /usr/bin/env bash
# GEneral overview: https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14
#MAKE TEST
python -m unittest #-v tests/io_test.py
#COMPILE PACKAGE
#python3 -m build --sdist # https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#source-distributions
#CHECK BUILD
#twine check dist/*
#SEND TO (TEST)PIPY
# twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*
#SEND TO PIPY # CREATE ACCOUNT
#twine upload dist/*
