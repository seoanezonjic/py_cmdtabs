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

parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
parser.add_argument("metric_file", metavar='M',
  help="File with tabulated metrics")
parser.add_argument("attributes", metavar='A',
  help="String with comma separated attributes")
parser.add_argument("output_file", metavar='O',
  help="Output file path")
parser.add_argument("-c", "--corrupted", dest="corrupted",
  help="File where corrupted metrics are stored")
options = parser.parse_args()

##################################################################################################
## MAIN
##################################################################################################
metric_file = CmdTabs.load_input_data(options.metric_file)
attributes = options.attributes.split(',')
samples_tag = attributes.pop(0)
metric_names, indexed_metrics = CmdTabs.index_metrics(metric_file, attributes)
table_output, corrupted_records = CmdTabs.create_table(indexed_metrics, samples_tag, attributes, metric_names)
CmdTabs.write_output_data(table_output, options.output_file)

if options.corrupted != None and len(corrupted_records) > 0:
	CmdTabs.write_output_data(corrupted_records, options.corrupted)