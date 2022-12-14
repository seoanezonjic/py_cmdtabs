#! /usr/bin/env python

import argparse
import sys
import os
ROOT_PATH=os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from py_cmdtabs import CmdTabs

#####################################################################
## OPTIONS
######################################################################
parser = argparse.ArgumentParser(description='Merge several tabulated files in one single file.')
parser.add_argument("files", metavar='F', nargs='+',
  help="Paths to tabulated files")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################

files = CmdTabs.load_files(options.files)
merged = CmdTabs.merge_files(files)
CmdTabs.write_output_data(merged)