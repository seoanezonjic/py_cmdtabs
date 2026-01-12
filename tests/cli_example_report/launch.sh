#! /usr/bin/env bash

. ~soft_bio_267/initializes/init_python
#python -m venv venv --system-site-packages
source venv/bin/activate
#pip install -e ~/dev_py/py_cmdtabs
#pip install -e ~/dev_py/py_report_html

report_html -t template.txt -d "./tables/*" -s ./subtemplates -c styles.css


