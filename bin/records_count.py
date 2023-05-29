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

def based_0(string): return (int(string) - 1)

parser = argparse.ArgumentParser(description='Counting how many times a record is repeated in a column.')
parser.add_argument("-i", "--input_file", dest="input",
  help="Path to input file")
parser.add_argument("-x", "--column_index", dest="col_index",
  help="Column index (1 based) to count elements", type=based_0)
parser.add_argument("--transposed", default=False, action="store_true", help="To perform the operations in rows and not columns")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################

input_table = CmdTabs.load_input_data(options.input)
counts = CmdTabs.records_count(input_table, options.col_index)
CmdTabs.write_output_data(counts)
