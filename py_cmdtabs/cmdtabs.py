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

	def load_several_files(all_files, sep = "\t", limit=-1):
		loaded_files = {}
		for file in all_files:
			if os.path.isdir(file):
				warn(file +" is not a valid file")
				continue
			loaded_files[file] = CmdTabs.load_input_data(file, sep, limit)
		return loaded_files

	def build_pattern(col_filter, keywords):
		pattern = defaultdict(lambda: False	)
		if col_filter != None and keywords != None:
			keys_per_col = keywords.split('%')
			if len(keys_per_col) != len(col_filter): abort('Number of keywords not equal to number of filtering columns') 
			i = 0
			for col in col_filter:
					pattern[col] = keys_per_col[i].split('&')
					i += 1
		return pattern

	def index_array(array, col_from=0, col_to=1):
		indexed_array = defaultdict(lambda: False	)
		for elements in array:
			indexed_array[elements[col_from]] = elements[col_to]
		return indexed_array

	def index_metrics(input_data, attributes):
		n_attrib = len(attributes)
		indexed_metrics = defaultdict(lambda: False	)
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


	def aggregate_column(input_table, col_index, col_agg, sep):
		aggregated_data = defaultdict(lambda: False	)
		for fields in input_table:
			CmdTabs.add2dict(aggregated_data, fields[col_index], fields[col_agg])
		aggregated_data_arr = []
		for k, value in aggregated_data.items():
			aggregated_data_arr.append([k, sep.join(value)])
		return aggregated_data_arr

	def add2dict(dict, key, val): # dict must be a defaultdict with default value set to False	
		query = dict[key]
		if not query:
			dict[key] = [val]
		else:
			query.append(val)

	def desaggregate_column(input_table, col_index, sep):
		desaggregated_data = []
		for fields in input_table:
			for field  in fields[col_index].split(sep):
				record = fields.copy()
				record[col_index] = field 
				desaggregated_data.append(record)
		return desaggregated_data

	def create_table(indexed_metrics, samples_tag, attributes, metric_names): #TODO: Corrupted entries not works. Think to move the entire library to pandas and use split with extend=true
		allTags = []
		allTags.extend(attributes)
		allTags.extend(metric_names)
		table_output = []
		corrupted_records = []
		for sample_name, sample_data in indexed_metrics.items():
			record = [sample_name]
			for tag in allTags:
				record.append(sample_data[tag])
			if record.count(None) > 0: # This not works, python split not fill empty cuts up to complete the given limit. Move to pandas
		 		warn("Record " + sample_name + "is corrupted:\n" + record.inspect + "\n")
		 		corrupted_records.append(record)
			else:
		 		table_output.append(record)
		allTags.insert(0, samples_tag)
		table_output.insert(0, allTags) # Add header
		corrupted_records.insert(0, allTags) # Add header
		return table_output, corrupted_records
	
	def name_replaces(tabular_input, sep, cols_to_replace, indexed_file_index):
		translated_fields = []
		untranslated_fields = []
		for fields in tabular_input:
			for col in cols_to_replace:
				replaced_field = indexed_file_index[fields[col]]
				if replaced_field:
					fields[col] = replaced_field 
					translated_fields.append(fields)
				else:
					untranslated_fields.append(fields)
		return translated_fields, untranslated_fields

	def link_table(indexed_linker, tabular_file, drop_line, sep):
		linked_table = []
		for fields in tabular_file:
			id = fields[0]
			info_id = indexed_linker[id]
			if info_id:
				fields.append(info_id)
				linked_table.append(fields)
			else:
				if not drop_line: linked_table.append(fields) 
		return linked_table


	def tag_file(input_file, tags, header):
		taged_file = []
		if header: empty_header = [""] * len(tags)
		n_row = 0
		for fields in input_file:
			if n_row == 0 and header:
				record = empty_header.copy()
			else:
				record = tags.copy()
			record.extend(fields)
			taged_file.append(record)
			n_row += 1
		return taged_file

	def filter(line, all_patterns, search_mode, match_mode, reverse = False	):
		filter = False	
		for col, patterns in all_patterns.items():
			is_match = False	
			for pattern in patterns:
				is_match = CmdTabs.expanded_match(line[col], pattern, match_mode)
				if is_match: break	  
			if is_match and search_mode == 's':
				filter = False	
				break
			elif not is_match and search_mode == 'c':
				filter = True
				break
			elif not is_match:
				filter = True
		if reverse: filter = not filter
		return filter

	def expanded_match(string, pattern, match_mode):
		is_match = False
		if pattern in string and match_mode == 'i': is_match = True
		if string == pattern and match_mode == 'c': is_match = True 
		return is_match

	def filter_columns(input_table, options):
		pattern = CmdTabs.build_pattern(options['col_filter'], options['keywords'])
		filtered_table = []
		for line in input_table:
			if not pattern or not CmdTabs.filter(line, pattern, options['search_mode'], options['match_mode'], options['reverse']):
				filtered_table.append(CmdTabs.shift_by_array_indexes(line, options['cols_to_show']) )
		return filtered_table

	def shift_by_array_indexes(arr_sub, indexes):
		return [ arr_sub[idx] for idx in indexes]

	def merge_and_filter_tables(input_files, options):
		header = []
		filtered_table = []
		if options.get('cols_to_show') == None: options['cols_to_show'] = [*range(0, len(input_files[0][0]), 1)] 
		for filename, file in input_files.items():
			if options.get('header') == None:
				if len(header.empty) == 0:
					header = file.pop(0)
				else:
					file.pop(0)
			filtered_table.extend(CmdTabs.filter_columns(file, options)) 
		if options.get('uniq') != None and options['uniq']: filtered_table = list(set(numbers)) 
		if len(header) > 0:
			header = CmdTabs.shift_by_array_indexes(header, options['cols_to_show'])
			filtered_table.insert(0, header)
		return filtered_table
