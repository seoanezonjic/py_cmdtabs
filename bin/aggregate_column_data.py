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

parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
parser.add_argument("-i", "--input_file", dest="input",
  help="Path to input file")
parser.add_argument("-x", "--column_index", dest="col_index",
  help="Column index (1 based) to use as reference", type=based_0)
parser.add_argument("-s", "--separator", dest="sep", default=",",
  help="Character separator when collapse data")
parser.add_argument("-a", "--column_aggregate", dest="col_aggregate",
  help="Column index (1 based) to extract data and join for each id in column index", type=based_0)
parser.add_argument("--transposed", default=False, action="store_true", help="To perform the operations in rows and not columns")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################
CmdTabs.transposed = options.transposed
input_table = CmdTabs.load_input_data(options.input)
agg_data = CmdTabs.aggregate_column(input_table, options.col_index, options.col_aggregate, options.sep)
CmdTabs.write_output_data(agg_data)

