# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="py_cmdtabs",
    version="0.1.0",
    description="Library for manage tabular files in cmd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://py_cmdtabs.readthedocs.io/",
    author="Pedro Seoane",
    author_email="example@email.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["py_cmdtabs"],
    include_package_data=True,
    scripts=['bin/aggregate_column_data.py', 'bin/column_filter.py', 'bin/create_metric_table.py', 'bin/desaggregate_column_data.py', 'bin/excel_to_tabular.py', 'bin/intersect_columns.py', 'bin/merge_tabular.py', 'bin/standard_name_replacer.py', 'bin/table_linker.py', 'bin/tag_table.py'],
    install_requires=["openpyxl"]

)
