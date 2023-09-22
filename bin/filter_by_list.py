#!/usr/bin/env python
import argparse
import os
import sys
ROOT_PATH=os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT_PATH, '..'))
from py_cmdtabs import CmdTabs

####################### ARGPARSE #################
##################################################
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files2befiltered", default= None, type = lambda x: x.split(","), required=True, help="The root to the files that has to be filtered, separated by commas")
parser.add_argument("-c", "--columns2befiltered", default = None, type = lambda	x: [list(map(int,r.split(","))) for r in x.split(";")] ,help="The columns that need to be filtered for each file, separated by semicolons, with each set of columns separated by commas")
parser.add_argument("-t", "--terms2befiltered", default= None, required=True, help="The PATH to the list of terms to be filtered")
parser.add_argument("--transposed", dest= "transposed", default= False, action="store_true", help="To perform the operations in rows and not columns")
parser.add_argument("--prefix", dest= "prefix", default= "filtered_", help="To select which prefix to add in new filterd files")
parser.add_argument("-o", "--output_path", default=".", help="The name of the output path")
parser.add_argument("--metrics", default=False, action="store_true", help= "Getting a table with the proportion of lines removed for each file")
options = parser.parse_args()

##################### MAIN #######################
##################################################

terms2befiltered = CmdTabs.load_input_data(options.terms2befiltered)
terms2befiltered = list(map(list, zip(*terms2befiltered )))[0]

CmdTabs.transposed = options.transposed
files2befiltered = options.files2befiltered
columns2befiltered = options.columns2befiltered
files_columns2befiltered = list(zip(files2befiltered,columns2befiltered))
loaded_files = CmdTabs.load_several_files(options.files2befiltered)

output_path = options.output_path

file_filteredfile = {}
for file_columns in files_columns2befiltered:
	file = file_columns[0]
	columns = file_columns[1]
	table = loaded_files[file]
	for column in columns:
		table = CmdTabs.filter_by_whitelist(table, terms2befiltered, column)
	file_filteredfile[file] = table


for file_path, filtered_table in file_filteredfile.items():
	file_name = os.path.basename(file_path)
	CmdTabs.write_output_data(filtered_table, output_path=os.path.join(output_path, options.prefix + file_name))

if options.metrics:
	for file2befiltered in options.files2befiltered:
		filtered_file = file_filteredfile.get(file2befiltered)
		if filtered_file is None:
			print(file2befiltered + "\t" + "Not Filtered")
		else:
			ratio_lines_removed = round(100*(len(file_filteredfile[file2befiltered])/len(loaded_files[file2befiltered])),2)
			print(file2befiltered + "\t" + str(ratio_lines_removed))

