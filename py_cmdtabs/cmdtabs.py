import sys
import os.path
from collections import defaultdict

class CmdTabs:
	def load_input_data(input_path, sep="\t", limit=-1):
		if limit > 0: # THis is due to ruby compute de cuts in other way and this fix enables ruby mode. Think if adapt to python way
			limit -= 1
		if input_path == '-':
			input_data = sys.stdin
		else:
			file = open(input_path, "r")
			input_data = file.readlines()
			file.close()
		input_data_arr = []
		for line in input_data:
			#print('---', file=sys.stderr)
			#print(repr(), file=sys.stderr)
			input_data_arr.append(line.rstrip().split(sep, limit))
		return input_data_arr

	def build_pattern(col_filter, keywords):
	    pattern = {}
	    if col_filter != None and keywords != None:
	        keys_per_col = keywords.split('%')
	        if len(keys_per_col) != len(col_filter): abort('Number of keywords not equal to number of filtering columns') 
	        i = 0
	        for col in col_filter:
	            pattern[col] = keys_per_col[i].split('&')
	            i += 1
	    return pattern

	def index_array(array, col_from=0, col_to=1):
		indexed_array = {}
		for elements in array:
			indexed_array[elements[col_from]] = elements[col_to]
		return indexed_array

	def index_metrics(input_data, attributes):
		n_attrib = len(attributes)
		indexed_metrics = defaultdict(lambda: False)
		metric_names = []
		for entry in input_data:
			sample_id = entry.pop(0)
			sample_attributes = entry[0:n_attrib - 1]
			metric_name, metric = entry[n_attrib:n_attrib + 2] # +2 due to select the next element and the upper bound is not contained in the subset
			if metric_name not in metric_names: metric_names.append(metric_name)
			query = indexed_metrics[sample_id]
			if not query:
				indexed_metrics[sample_id] = {metric_name: metric}
				i = 0
				for attrib in attributes:
					indexed_metrics[sample_id][attrib] = sample_attributes[i] 
					i += 1
			else:
				query[metric_name] = metric
		return metric_names, indexed_metrics

	def parse_column_indices(sep, col_string):
	    cols = []
	    for col in col_string.split(sep):
	    	cols.append(int(col) - 1)
	    return cols

	def load_and_parse_tags(tags, sep):
		parsed_tags = []
		for tag in tags:
			if os.path.exists(tag):
				parsed_tags.extend(CmdTabs.load_input_data(tag, sep))
				break
			else:
				parsed_tags.append(tag.split(sep))
		return [item for sublist in parsed_tags for item in sublist] #Flatten list

	def load_records(input_file, cols, full): # TODO: Convert list to string to be hasheable is a workaround. We must search another way to do this!!!
		records = {}
		full_row_of_records = {}
		for fields in input_file:
			field = "\t".join([fields[c] for c in cols]) # Lists are not hasheable in Python so we covert them to string
			records[field] = True
			if full: full_row_of_records[field] = fields 
		return list(records.keys()), full_row_of_records