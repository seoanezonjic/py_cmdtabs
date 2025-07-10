import sys
import gzip
import os
import warnings
import copy
import os.path
import numpy as np
from collections import defaultdict
import openpyxl
import py_exp_calc.exp_calc as pxc

class CmdTabs:
	transposed = False
	compressed_input = False
	compressed_output = False

	def load_input_data(input_path, sep="\t", limit=-1, first_only=False, add_empty_fields=True):
		open_file = gzip.open if CmdTabs.compressed_input else open
		if limit > 0: # THis is due to ruby compute de cuts in other way and this fix enables ruby mode. Think if adapt to python way
			limit -= 1
		if input_path == '-':
			if CmdTabs.compressed_input: 
				input_data = gzip.decompress(sys.stdin.buffer.read()).decode().strip().split('\n')
			else: 
				input_data = sys.stdin
		else:
			with open_file(input_path, "rt") as f:
				input_data = f.readlines()
		input_data_arr = []
		for line in input_data:
			fields_number = line.count(sep) + 1
			#print('---', file=sys.stderr)
			#print(repr(), file=sys.stderr)
			fields = line.rstrip().split(sep, limit)
			if add_empty_fields:
				limit_fields = 0 if limit <= 0 else limit 
				fields = fields + ( [""] * (fields_number - len(fields) - limit_fields) )
			input_data_arr.append(fields)
			if first_only:
				break
		if CmdTabs.transposed:
			input_data_arr = CmdTabs.transpose(input_data_arr)

		return input_data_arr

	def load_several_files(all_files, sep = "\t", limit=-1, dict_keys_mapper = None, add_empty_fields=True):
		loaded_files = {}
		for file in all_files:
			if os.path.isdir(file):
				warnings.warn(file +" is not a valid file")
				continue
			key_id = file if not dict_keys_mapper else dict_keys_mapper(file)
			loaded_files[key_id] = CmdTabs.load_input_data(file, sep, limit, add_empty_fields=add_empty_fields)
		return loaded_files

	def load_files(files_path): #NO TEST # Cleaning an filling behaviour could be sent to load_input_data as options and use on load_several_files
		files = {}
		for file_name in files_path:
			input_table = CmdTabs.load_input_data(file_name)
			file = []
			for fields in input_table:
				if fields.count('') == len(fields): continue #skip blank records
				file.append([ '-' if field == "" else field for field in fields])
			files[file_name] = file
		return files

	def build_pattern(col_filter, keywords):
		pattern = defaultdict(lambda: False	)
		if col_filter != None and keywords != None:
			keys_per_col = keywords.split('%')
			if len(keys_per_col) != len(col_filter): os.abort('Number of keywords not equal to number of filtering columns') 
			i = 0
			for col in col_filter:
					pattern[col] = keys_per_col[i].split('&')
					i += 1
		return pattern

	def index_array(array, col_from=0, col_to=1, header=False):
		indexed_array = defaultdict(lambda: False)
		if type(col_to) != list:
			f = lambda x: x[col_to]
		else: 
			f = lambda x: [x[c] for c in col_to]
		if header: 
			head = array.pop(0)
			indexed_array['header'] = f(head)
		for elements in array:
			indexed_array[elements[col_from]] = f(elements)
		return indexed_array

	def index_metrics(input_data, attributes):
		n_attrib = len(attributes)
		indexed_metrics = defaultdict(lambda: False	)
		metric_names = []
		for entry in input_data:
			entry = entry.copy()
			sample_id = entry.pop(0)
			sample_attributes =  [entry.pop(0) for i in range(n_attrib)]
			if len(entry) == 2: 
				metric_name, metric = entry # The metric is full and it has key and val
			else:
				metric_name = entry[0] # The metric is corrupted and it has only the key but val
				metric = None

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
			if "-" in col: # Range of columns (both ends included)
				start, end = col.split("-")
				range_cols = [int(i) - 1 for i in range(int(start), int(end) + 1)]
				cols.extend(range_cols)
			else: # Single column
				cols.append(int(col) - 1)
		return cols

	def load_and_parse_tags(tags, sep):
		parsed_tags = []
		for tag in tags:
			if os.path.exists(tag):
				parsed_tags.extend(CmdTabs.load_input_data(tag, sep, first_only=True))
			else:
				parsed_tags.append(tag.split(sep))
		return [item for sublist in parsed_tags for item in sublist] #Flatten list

	def load_records(input_file, cols, full): # TODO: Convert list to string to be hasheable is a workaround. We must search another way to do this!!!
		records = {}
		full_row_of_records = {}
		for fields in input_file:
			field = "\t".join([fields[c] for c in cols]) # Lists are not hasheable in Python so we covert them to string
			records[field] = True
			if full: full_row_of_records[field] = ["\t".join(fields)]
		return list(records.keys()), full_row_of_records


	def aggregate_column(input_table, col_index, cols_agg, sep, agg_mode="concatenate"):
		make_aggregation = {"concatenate": lambda agg_col: sep.join(agg_col), "mean": np.mean, "median": np.median, "max": np.max, "min": np.min, "sum": np.sum, "std": np.std, "var": np.var,
					  		"count": lambda agg_col: len(agg_col), "IQR": lambda agg_col: np.percentile(agg_col, 75) - np.percentile(agg_col, 25),
							"PC25": lambda agg_col: np.percentile(agg_col, 25), "PC75": lambda agg_col: np.percentile(agg_col, 75)}
		aggregated_data = defaultdict(lambda: False	)
		if type(cols_agg) == int: cols_agg = [cols_agg]
		if type(col_index) == int: col_index = [col_index]
		for fields in input_table:
			for col_agg in cols_agg:
				pxc.add_nested_value(aggregated_data, (tuple([fields[idx] for idx in col_index]), col_agg), fields[col_agg], True)
		aggregated_data_arr = []
		for k, agg_dict in aggregated_data.items():
			col_data = [idx_col for idx_col in k]
			for aggregated_column in agg_dict.values():
				if agg_mode != "concatenate": aggregated_column = [float(item) for item in aggregated_column]
				col_data.append( str(make_aggregation[agg_mode](aggregated_column)) )
			aggregated_data_arr.append(col_data)
		return aggregated_data_arr

	def records_count(input_table, col_index):
		if len(col_index) == 1: col_index = col_index[0]
		elif len(col_index) > 1: raise ValueError("Only one column can be used to count records")
		
		aggregated_data = defaultdict(lambda: 0 )
		for fields in input_table:
			aggregated_data[fields[col_index]]+=1
			output_list = []
		for k, value in aggregated_data.items():
			output_list.append([k, str(value)])
		return output_list

	def desaggregate_column(input_table, col_index, sep):
		desaggregated_data = []
		for fields in input_table:
			desagg_dict = {col_idx: fields[col_idx].split(sep) for col_idx in col_index}
			for agg_idx in range(len(desagg_dict[col_index[0]])):
				record = fields.copy()
				for col_idx in col_index: record[col_idx] = desagg_dict[col_idx][agg_idx]
				desaggregated_data.append(record)
		return desaggregated_data

	def create_table(indexed_metrics, samples_tag, attributes, metric_names):
		allTags = []
		allTags.extend(attributes)
		allTags.extend(metric_names)
		table_output = []
		corrupted_records = []
		for sample_name, sample_data in indexed_metrics.items():
			record = [sample_name]
			for tag in allTags:
				record.append(sample_data.get(tag))
			if record.count(None) > 0:
				warnings.warn("Record " + sample_name + "is corrupted:\n" + repr(record) + "\n")
				corrupted_records.append(record)
			else:
				table_output.append(record)
		allTags.insert(0, samples_tag)
		table_output.insert(0, allTags) # Add header
		corrupted_records.insert(0, allTags) # Add header
		return table_output, corrupted_records
	
	def name_replaces(tabular_input, sep, cols_to_replace, indexed_file_index, remove_uns=False):
		translated_fields = []
		untranslated_fields = []
		for fields in tabular_input:
			replaced_field = True
			fields = copy.copy(fields) # To avoid modify original data
			for col in cols_to_replace:
				rep_field = indexed_file_index[fields[col]]
				if not rep_field: 
					replaced_field = False
				else:
					fields[col] = rep_field
			if replaced_field:
				translated_fields.append(fields)
			elif not remove_uns:
				translated_fields.append(fields)
			else:
				untranslated_fields.append(fields)
		return translated_fields, untranslated_fields

	def link_table(indexed_linker, tabular_file, drop_line, sep, header=False):
		linked_table = []
		if header: linked_table.append(tabular_file.pop(0)+indexed_linker['header'])
		for fields in tabular_file:
			id = fields[0]
			info_id = indexed_linker.get(id)
			if info_id:
				if type(info_id) == list:
					fields += info_id
				else:
					fields.append(info_id)
				linked_table.append(fields)
			else:
				if not drop_line: linked_table.append(fields) 
		return linked_table

	def tag_file(input_file, tags, header):
		taged_file = []
		n_row = 0
		for fields in input_file:
			if n_row == 0 and header:
				n_row += 1
				continue
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
				filtered_table.append(CmdTabs.extract_fields(line, options['cols_to_show']) )
		return filtered_table

	def extract_fields(arr_sub, indexes):
		if indexes == [-1]:
			return arr_sub
		else:
			return [ str(arr_sub[idx]) for idx in indexes] # The str instruction is used to ensure that always we have string data (i.e: when this function is used with excel objecb it could extrac numerical data)

	def merge_files(files, fill_character='-'): #NO TEST
		parent_table = {}
		table_length = 0
		for file_names, file in files.items():
			local_length = 0
			for fields in file:
				id = fields.pop(0) 
				local_length = len(fields)
				if not parent_table.get(id):
					parent_table[id] = [fill_character] * table_length
				elif len(parent_table[id]) < table_length:
					diference = table_length - len(parent_table[id])
					parent_table[id].extend( [fill_character] * diference)
				parent_table[id].extend(fields)				
			table_length += local_length
			
		parent_table_arr = []
		for id, fields in parent_table.items():
			diference = table_length - len(fields)
			if diference > 0: fields.extend([fill_character] * diference)
			record = [id]
			record.extend(fields)
			parent_table_arr.append(record)
		return parent_table_arr

	def merge_and_filter_tables(input_files, options):
		header = []
		filtered_table = []
		if options.get('cols_to_show') == None: options['cols_to_show'] = [*range(0, len(input_files[0][0]), 1)] 
		for filename, file in input_files.items():
			if options.get('header') != None and options['header']:
				if len(header) == 0:
					header = file.pop(0)
				else:
					file.pop(0)
			fields = CmdTabs.filter_columns(file, options)
			filtered_table.extend(fields) 
		if options.get('uniq') != None and options['uniq']: filtered_table = CmdTabs.get_uniq(filtered_table)
		if len(header) > 0:
			header = CmdTabs.extract_fields(header, options['cols_to_show'])
			filtered_table.insert(0, header)
		return filtered_table


	def filter_by_whitelist(table, terms2filter, column2filter, not_exact_match=False):
		if not_exact_match:
			filtered_table = [row for row in table if any([term in row[column2filter] for term in terms2filter])]
		else:
			terms2filter = set(terms2filter)
			terms2filter = {term: True for term in terms2filter}
			filtered_table = [row for row in table if terms2filter.get(row[column2filter])]
		return filtered_table

	def filter_by_blacklist(table, terms2filter, column2filter, not_exact_match=False):
		if not_exact_match:
			filtered_table = [row for row in table if all([term not in row[column2filter] for term in terms2filter])]
		else:
			terms2filter = set(terms2filter)
			terms2filter = {term: True for term in terms2filter}
			filtered_table = [row for row in table if not terms2filter.get(row[column2filter])]
		return filtered_table

	def get_uniq(table):
		return [list(i) for i in set(tuple(i) for i in table)] # list cannot be used by set so we use tuples change back the format

	def extract_columns(table, columns2extract):
		storage = []
		for row in table:
			storage.append(CmdTabs.extract_fields(row, columns2extract))
		return storage
	
	def extract_rows(table, rows2extract):
		if rows2extract == [-1]:
			return table
		else:
			return [ row for idx, row in enumerate(table) if idx in rows2extract ]

	def get_table_from_excel(file, sheet_number):
		x = openpyxl.load_workbook(file)
		sheets = x.sheetnames # list excel sheets by name
		ws = x[sheets[sheet_number]] #select sheet by index (so, we select by sheet order)
		sheet = []
		
		for xl_row in ws.iter_rows(min_row=1, min_col=1, max_col=ws.max_column, max_row=ws.max_row, values_only=True):
			row = []
			for val in xl_row:
				if val == None: val = ''
				row.append(val)
			sheet.append(row)

		if CmdTabs.transposed:
			sheet = CmdTabs.transpose(sheet)
			
		return sheet

	def get_groups(a_records, b_records): # inputs are list of string but should be nested lists. This is due to python don't allow to hash list in dicts.
		a_rec = set(a_records)				# For this reason, the last lines convert in lists the strings of the original list to keep the format
		b_rec = set(b_records)				# TODO: See to tranfor to tuples instead to string
		common_set = a_rec & b_rec
		a_only = [[r] for r in a_rec if r not in common_set]
		b_only = [[r] for r in b_rec if r not in common_set]
		common = [[r] for r in common_set]
		return common, a_only, b_only

	def write_output_data(output_data, output_path=None, sep="\t"):
		open_file = gzip.open if CmdTabs.compressed_output else open
		if CmdTabs.transposed:
			output_data = CmdTabs.transpose(output_data)
			
		if output_path != None:
			with open_file(output_path, 'wt') as out_file:
				for line in output_data:
					out_file.write(sep.join([str(l) for l in line]) + "\n")
		else:
			if CmdTabs.compressed_output:
				columns_joined = []
				for line in output_data:
					columns_joined.append(sep.join([str(l) for l in line]))
				all_joined = "\n".join(columns_joined) + "\n"
				sys.stdout.buffer.write(gzip.compress(bytes(all_joined, 'utf-8')))
			else:
				for line in output_data:
					print(sep.join([str(l) for l in line]))

	def transpose(table):
		transposed_table = list(map(list, zip(*table)))
		return transposed_table
	
	def subset_table(table, start_line, number_of_lines, has_header):
		final_line = start_line + number_of_lines 
		if has_header: header = table.pop(0) 
		if final_line > len(table) - 1: final_line = len(table)
		subset_table = table[start_line:final_line]
		if has_header: subset_table.insert(0, header)
		return subset_table 
	
	def transform_to_latex(input_table, header, whole, name):
		latex_table = []
		if header: input_table[0] = [f'\\textbf{{{head_item}}}' for head_item in input_table[0]]
	    
		for idx, row in enumerate(input_table):
			joined_row =  " & ".join(row) + " \\\\ \\hline"		
			if idx == 0: joined_row = "\\hline \n" + joined_row
			latex_table.append(joined_row)
		
		if whole: 
			cols_type = "|"+ "|".join(['l'] * len(input_table[0])) + "|"
			final_table = [[f'\\begin{{table}}[!htbp]\n\\centering\n\\caption{{}}\n\\begin{{tabular}}{{{cols_type}}}']]
			final_table += latex_table
			final_table += [f"\\end{{tabular}}\n\\label{{table:{name}}}\n\\end{{table}}"]
		else:
			final_table = latex_table
		return final_table