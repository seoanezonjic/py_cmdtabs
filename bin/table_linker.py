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

parser = argparse.ArgumentParser(description='Merge tabular files.')
parser.add_argument("-i", "--input_file", dest="input_file",
  help="Path to input file")
parser.add_argument("-o", "--output_file", dest="output_file",
  help="Path to output file")
parser.add_argument("-l", "--linker_file", dest="linker_file",
  help="Path to file linker")
parser.add_argument("--drop", dest="drop_line", default=False, action='store_true',
  help="Write the lines whose identifiers have been matched")
parser.add_argument("-s", "--separator", dest="sep", default="\t",
  help="Character separator when collapse data")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################

input_linker = CmdTabs.load_input_data(options.linker_file)
indexed_linker = CmdTabs.index_array(input_linker)
input_table = CmdTabs.load_input_data(options.input_file, "\t", 2)

linked_table = CmdTabs.link_table(indexed_linker, input_table, options.drop_line, options.sep)
CmdTabs.write_output_data(linked_table, options.output_file)