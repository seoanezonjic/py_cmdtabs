.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/py_cmdtabs.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/py_cmdtabs
    .. image:: https://readthedocs.org/projects/py_cmdtabs/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://py_cmdtabs.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/py_cmdtabs/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/py_cmdtabs
    .. image:: https://img.shields.io/pypi/v/py_cmdtabs.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/py_cmdtabs/
    .. image:: https://img.shields.io/conda/vn/conda-forge/py_cmdtabs.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/py_cmdtabs
    .. image:: https://pepy.tech/badge/py_cmdtabs/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/py_cmdtabs
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/py_cmdtabs

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

==========
py_cmdtabs
==========


    Set of tools to facilitate parsing of tabulated files


py_cmdtabs includes tools that make it easier for its user to manipulate tabulated files. It is designed to carry out the following functionalities:

* Add columns: the aggregate_columns.py script allows you to change the format of the information saved in the same file, combining its columns into a single one as specified in the script.
* Disaggregate columns: the desaggregate_columns.py script allows you to change the format of the information saved in the same file, disaggregating its columns into several using a specific pattern.
* Join tables: the merge_tabular.py script allows two or more tabular tables to be joined by a common join pattern between both.
* Tag tables: the tag_table.py script is used to include a series of specific tags to elements of a table.
* Intersect columns: the intersect_columns.py script compares the elements of two columns belonging to two different tables.
* Obtain common information: the table_linker.py script allows you to save in the same output file the information extracted from a tabulated file, based on the identifiers of a second file.
* Replace information: The standard_name_replacer.py script replaces values in a table based on a contributed value code.
* Filter columns: The column_filter.py script filters columns from a tabulated file whose elements match a specified pattern.
* Transform Excel format into tabular: the excel_to_tabular.py script transforms files with an .xlsx extension into tabular files and makes their handling easier.