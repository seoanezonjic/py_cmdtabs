#! /usr/bin/env python

import argparse
import sys
import os
import glob
ROOT_PATH=os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT_PATH, '..'))
from py_cmdtabs import CmdTabs

#################################################################################################
## INPUT PARSING
#################################################################################################

def list_based_0(string): return CmdTabs.parse_column_indices(",", string)

parser = argparse.ArgumentParser(description='Get records from table an extract desired columns.')
parser.add_argument("-t", "--table_file", dest="table_file",
  help="Input tabulated file")
parser.add_argument("-c", "--column", dest="cols_to_show", type=list_based_0,
  help="Column/s to show (1 based). Format: x,y,z..")
parser.add_argument("-f", "--col_filter", dest="col_filter", type=list_based_0,
  help="Select columns where search keywords. Format: x,y,z..")
parser.add_argument("-p", "--separator", dest="separator", default="\t",
  help="Column character separator")
parser.add_argument("-k", "--keywords", dest="keywords",
  help="Keywords for select rows. Format: key1_col1&key2_col1%key1_col2&key2_col2")
parser.add_argument("-s", "--search", dest="search_mode", default='c', choices=['c', 's'],
  help="c for match in every columns set, s some match in some column. Default c")
parser.add_argument("-m", "--match_mode", dest="match_mode", default='i', choices=['i', 'c'],
  help="i string must include the keyword, c for fullmatch. Default i")
parser.add_argument("-r", "--reverse", dest="reverse", default=False, action='store_true',
  help="Select not matching")
parser.add_argument("-u", "--uniq", dest="uniq", default=False, action='store_true',
  help="Delete redundant items")
parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
  help="Indicate if files have header")
parser.add_argument("--transposed", default=False, action="store_true", help="To perform the operations in rows and not columns")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################
if options.table_file == None: sys.exit('Tabulated file not specified') 
CmdTabs.transposed = options.transposed
file_names = glob.glob(options.table_file)
input_files = CmdTabs.load_several_files(file_names, options.separator)
filtered_table = CmdTabs.merge_and_filter_tables(input_files, vars(options))
CmdTabs.write_output_data(filtered_table)
 