#! /usr/bin/env python

import argparse
import sys
import os
ROOT_PATH=os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from py_cmdtabs import CmdTabs

#################################################################################################
## INPUT PARSING
#################################################################################################
def list_str(values): return values.split(',')

parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
parser.add_argument("-i", "--input_file", dest="input_file",
  help="Path to input file")
parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
  help="Indicate if input file has a header line. Header will not be printed in output")
parser.add_argument("-t", "--tags", dest="tags",
  help="Strings or files (only first line will be used) sepparated by commas", type=list_str)
parser.add_argument("-s", "--sep_char", dest="sep", default="\t",
  help="Column character separator")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################

input_table = CmdTabs.load_input_data(options.input_file)
tags = CmdTabs.load_and_parse_tags(options.tags, options.sep)
taged_table = CmdTabs.tag_file(input_table, tags, options.header)
CmdTabs.write_output_data(taged_table, None, options.sep)