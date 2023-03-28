#! /usr/bin/env python

import argparse
import sys
import os
ROOT_PATH=os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT_PATH, '..'))
from py_cmdtabs import CmdTabs

#####################################################################
## OPTPARSE
######################################################################

def based_0(string): return int(string) - 1
def list_based_0(string): return CmdTabs.parse_column_indices(",", string)

parser = argparse.ArgumentParser(description='Replace substring in a tabular file with the strings listed in a dictionary file')
parser.add_argument("-i", "--input_file", dest="input_file",
  help="Path to input file")
parser.add_argument("-o", "--output_file", dest="output_file",
  help="Path to output file")
parser.add_argument("-I", "--index_file", dest="index_file",
  help="Path to index file")
parser.add_argument("-f", "--from", dest="frm", default=0, type=based_0,
  help="Column in index file to take reference value. Default 1. Numeration is 1 based")
parser.add_argument("-t", "--to", dest="to", default=1, type=based_0,
  help="Column in index file to take the value that will be used in substitution. Default 2. Numeration is 1 based")
parser.add_argument("-s", "--input_separator", dest="input_separator", default="\t",
  help="Character separator")
parser.add_argument("-c", "--columns", dest="columns", default=[1], type=list_based_0,
  help="Index of columns in base 1 to compare")
parser.add_argument("-u", "--remove_untranslated", dest="remove_untranslated", default=False, action='store_true',
  help="Activate this flag for outputting the untranslated entries")

options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################

input_index = CmdTabs.load_input_data(options.index_file)
translation_index = CmdTabs.index_array(input_index, options.frm, options.to)

input_table = CmdTabs.load_input_data(options.input_file, options.input_separator)

tabular_output_translated, _ = CmdTabs.name_replaces(input_table, options.input_separator, options.columns, translation_index, options.remove_untranslated)

CmdTabs.write_output_data(tabular_output_translated, options.output_file, options.input_separator)
