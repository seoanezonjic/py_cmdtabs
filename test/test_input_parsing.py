import unittest
import sys
import os
from py_cmdtabs import CmdTabs
ROOT_PATH=os.path.dirname(__file__)
DATA_TEST_PATH = os.path.join(ROOT_PATH, 'data_tests')

class InputParsingTestCase(unittest.TestCase):
	def test_build_pattern(self):
		col_filter = [0, 1, 2]
		keywords = "key1_col1&key2_col1%key1_col2&key2_col2%key1_col3"
		pattern_test = CmdTabs.build_pattern(col_filter, keywords)
		expected_result = {0 : ["key1_col1", "key2_col1"], 1 : ["key1_col2", "key2_col2"], 2 : ["key1_col3"]}
		self.assertEqual(expected_result, pattern_test)

	def test_parse_column_indices(self):
		cols_string = "1,3,4,7"
		col_indx_test = CmdTabs.parse_column_indices(",", cols_string)
		expected_result = [0,2,3,6]
		self.assertEqual(expected_result, col_indx_test)

	def test_load_and_parse_tags_file(self):
		input_tags = [os.path.join(DATA_TEST_PATH, 'tracker')]
		tag_test = CmdTabs.load_and_parse_tags(input_tags, "\t")
		expected_result = ['MERGED_net_no_raw_cpm', 'MERGED', 'no', 'no', 'cpm']
		self.assertEqual(expected_result, tag_test)

	def test_load_and_parse_tags_stdin(self):
		input_tags = ['MERGED_net_no_raw_cpm', 'MERGED', 'no', 'no', 'cpm']
		tag_test = CmdTabs.load_and_parse_tags(input_tags, "\t")
		expected_result = ['MERGED_net_no_raw_cpm', 'MERGED', 'no', 'no', 'cpm']
		self.assertEqual(expected_result, tag_test)

	def test_load_records(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_cluster'))
		records_test = CmdTabs.load_records(input_table, [0], False)
		expected_result = ['MONDO:0008995', 'MONDO:0007172', 'MONDO:0014823', 'MONDO:0017999', 'MONDO:0011142',
		'MONDO:0009833', 'MONDO:0009594', 'MONDO:0010193', 'MONDO:0012176', 'MONDO:0013969'], {}
		self.assertEqual(expected_result, records_test)

	def test_load_records_full(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_cluster'))
		selected_fields, full_records = CmdTabs.load_records(input_table, [0], True)
		expected_selected_fields = ['MONDO:0008995', 'MONDO:0007172', 'MONDO:0014823', 'MONDO:0017999', 'MONDO:0011142',
		'MONDO:0009833', 'MONDO:0009594', 'MONDO:0010193', 'MONDO:0012176', 'MONDO:0013969'] 
		expected_full_records = {"MONDO:0008995" : ["MONDO:0008995\t19_ref"], "MONDO:0007172" : ["MONDO:0007172\t22_ref"], 
		"MONDO:0014823" : ["MONDO:0014823\t25_ref"], "MONDO:0017999" : ["MONDO:0017999\t53_ref"],
		"MONDO:0011142" : ["MONDO:0011142\t66_ref"], "MONDO:0009833" : ["MONDO:0009833\t53_ref"],
		"MONDO:0009594" : ["MONDO:0009594\t54_ref"], "MONDO:0010193" : ["MONDO:0010193\t54_ref"], 
		"MONDO:0012176" : ["MONDO:0012176\t62_ref"], "MONDO:0013969" : ["MONDO:0013969\t1189_ref"]}
		self.assertEqual(expected_selected_fields, selected_fields)
		self.assertEqual(expected_full_records, full_records)

	def test_index_metrics(self):
		metric_file = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'all_metrics'))
		fixCols = 'sample'
		attributes = fixCols.split(',')
		attributes.pop(0)
		metric_names, indexed_metrics = CmdTabs.index_metrics(metric_file, attributes)
		expected_metric_names = ['initial_total_sequences', 'initial_read_max_length', 'initial_read_min_length', 'initial_%gc']
		expected_indexed_metrics = {'CTL_1_cell' : {'initial_total_sequences' : '11437331.0', 'initial_read_max_length' : '76.0', 
		'initial_read_min_length' : '35.0', 'initial_%gc' : '45.0'}, 'CTL_1_exo' : {'initial_total_sequences' : '10668412.0', 
		'initial_read_max_length' : '76.0', 'initial_read_min_length' : '35.0', 'initial_%gc' : '48.0'}}
		self.assertEqual(expected_metric_names, metric_names)
		self.assertEqual(expected_indexed_metrics, indexed_metrics)

	def test_index_array(self):
		input_index = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_gene'))
		indexed_test = CmdTabs.index_array(input_index)
		expected_result = {'MONDO:0010193' : 'HGNC:3527', 'MONDO:0008995' : 'HGNC:16873', 'MONDO:0012866' : 'HGNC:21197', 'MONDO:0017999' : 'HGNC:21197', 'MONDO:0011142' : 'HGNC:21144', 'MONDO:0013969' : 'HGNC:21176', 'MONDO:0018053' : 'HGNC:21157'}
		self.assertEqual(expected_result, indexed_test)
