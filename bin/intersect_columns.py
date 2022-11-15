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

def list_based_0(string): return CmdTabs.parse_column_indices(",", string)

parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
parser.add_argument("-a", "--a_file", dest="a_file",
  help="Path to input file")
parser.add_argument("-b", "--b_file", dest="b_file",
  help="Path to input file")
parser.add_argument("-A", "--a_cols", dest="a_cols", default=[0], type=list_based_0,
  help="Index of columns in base 1 to compare")
parser.add_argument("-B", "--b_cols", dest="b_cols", default=[0], type=list_based_0,
  help="Index of columns in base 1 to compare")
parser.add_argument("-s", "--separator", dest="sep", default="\t",
  help="Column character separator")
parser.add_argument("-c", "--count", dest="count", default=False, action='store_true',
  help="Only compute number of matches")
parser.add_argument("--full", dest="full", default=False, action='store_true',
  help="Give full record")
parser.add_argument("-k", "--keep", dest="keep", default='c', choices=['a', 'b', 'c' 'ab'],
  help="Keep records. c for common, 'a' for specific of file a, 'b' for specific of file b and 'ab' for specific of file a AND b")

options = parser.parse_args()

input_data_a = CmdTabs.load_input_data(options.a_file, options.sep)
input_data_b = CmdTabs.load_input_data(options.b_file, options.sep)

a_records, full_a_rec = CmdTabs.load_records(input_data_a, options.a_cols, options.full)
b_records, full_b_rec = CmdTabs.load_records(input_data_b, options.b_cols, options.full)

common, a_only, b_only = CmdTabs.get_groups(a_records, b_records)

if options.count:
  print("a: " + str(len(a_only)))
  print("b: " + str(len(b_only)))
  print("c: " + str(len(common)))
else:
  # As the groups are list with nested list with only one element: [['str1'], ['str2']..] the full mode need to access to 0 element to be use as key in full_X_rec
  if options.keep == 'c':
    result = common
    if options.full: result = [full_a_rec[r[0]] + full_b_rec[r[0]] for r in common]
  elif options.keep == 'a':
    result = a_only
    if options.full: result = [full_a_rec[r[0]] for r in a_only]
  elif options.keep == 'b':
    result = b_only
    if options.full: result = [full_b_rec[r[0]] for r in b_only]
  elif options.keep == 'ab':
    if options[:full]:
      a_only = [full_a_rec[r[0]] for r in a_only]
      b_only = [full_b_rec[r[0]] for r in b_only]
    result = a_only + b_only
  CmdTabs.write_output_data(result, None, options.sep)