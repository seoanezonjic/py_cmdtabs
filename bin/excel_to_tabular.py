#! /usr/bin/env python

import argparse
import sys
import os
ROOT_PATH=os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from py_cmdtabs import CmdTabs

#######################
## OPTPARSE
#######################

def based_0(string): return int(string) - 1
def list_based_0(string): return CmdTabs.parse_column_indices(",", string)

parser = argparse.ArgumentParser(description='Replace substring in a tabular file with the strings listed in a dictionary file')
parser.add_argument("-i", "--input_file", dest="input_file",
  help="Input xlsx file")
parser.add_argument("-o", "--output_file", dest="output_file",
  help="Path to output file")
parser.add_argument("-c", "--columns2extract", dest="columns2extract", default=[0], type=list_based_0,
  help="Column position to extract (1 based). Default 1")
parser.add_argument("-s", "--sheet_number", dest="sheet_number", default=0, type=based_0,
  help="Sheet number to work with. Default 1")

options = parser.parse_args()

#######################
## MAIN
#######################

sheet = CmdTabs.get_table_from_excel(options.input_file, options.sheet_number)
storage = CmdTabs.extract_columns(sheet, options.columns2extract)
CmdTabs.write_output_data(storage, options.output_file)