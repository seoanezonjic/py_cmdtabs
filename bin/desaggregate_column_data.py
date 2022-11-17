#! /usr/bin/env python

import argparse
import sys
import os
ROOT_PATH=os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
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
parser.add_argument("-s", "--sep_char", dest="sep", default=',',
  help="Character separator when collapse data")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################
input_table = CmdTabs.load_input_data(options.input)
desagg_data = CmdTabs.desaggregate_column(input_table, options.col_index, options.sep)
CmdTabs.write_output_data(desagg_data)
