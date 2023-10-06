import unittest
import sys
import os
from py_cmdtabs import CmdTabs
ROOT_PATH=os.path.dirname(__file__)
DATA_TEST_PATH = os.path.join(ROOT_PATH, 'data_tests')

class CmdTabsTestCase(unittest.TestCase):
	def setUp(self):
		CmdTabs.transposed = False
	def test_aggregate_column(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_desagg'))
		aggrgated_test = CmdTabs.aggregate_column(input_table, 0, 1, ", ") 
		expected_result = [['HGNC:21197', '483_ref, 1039_ref, 1071_ref'], ['HGNC:21143', '211_ref, 4705_ref']]
		self.assertEqual(expected_result, aggrgated_test)

	def test_desaggregate_column(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_agg'))
		desaggregated_test = CmdTabs.desaggregate_column(input_table, 1, ',')
		expected_result = [['HGNC:21197', '483_ref'], ['HGNC:21197', '1039_ref'], ['HGNC:21197', '1071_ref'], ['HGNC:21143', '211_ref'], ['HGNC:21143', '4705_ref']]
		self.assertEqual(expected_result, desaggregated_test)

	def test_create_table(self):
		metric_file = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'all_metrics'))
		attributes = []
		samples_tag = 'sample'
		metric_names, indexed_metrics = CmdTabs.index_metrics(metric_file, attributes)
		created_table, corrupted_records = CmdTabs.create_table(indexed_metrics, samples_tag, attributes, metric_names)
		expected_table = [["sample", "initial_total_sequences", "initial_read_max_length", "initial_read_min_length", "initial_%gc"], 
			["CTL_1_cell", "11437331.0", "76.0", "35.0", "45.0"], 
			["CTL_1_exo", "10668412.0", "76.0", "35.0", "48.0"]]
		expected_corrupted_records = [["sample", "initial_total_sequences", "initial_read_max_length", "initial_read_min_length", "initial_%gc"]]
		self.assertEqual(expected_table, created_table)
		self.assertEqual(expected_corrupted_records, corrupted_records)

	def test_name_replacer(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_cluster'))
		input_index = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_gene'))
		indexed_index = CmdTabs.index_array(input_index)
		replaced, unreplaced = CmdTabs.name_replaces(input_table, "\t", [0], indexed_index, remove_uns=True)
		expected_replaced = [['HGNC:16873', '19_ref'], ["HGNC:21197", "36_ref"], ["HGNC:21197", "53_ref"], ["HGNC:21144", "53_ref"], ['HGNC:3527', '54_ref'], ["HGNC:21144", "66_ref"], ['HGNC:21176', '1189_ref']] 
		expected_unreplaced = [["MONDO:0007172", "22_ref"], ["MONDO:0014823", "25_ref"], ["MONDO:0009833", "53_ref"], 
		["MONDO:0009594", "54_ref"], ["MONDO:0012176", "62_ref"]]
		self.assertEqual(expected_replaced, replaced)
		self.assertEqual(expected_unreplaced, unreplaced)
		#TEst for multiple columns, check that output is not N times the input. Is expected that the second col in not changed
		rep, unrep = CmdTabs.name_replaces(input_table, "\t", [0, 1], indexed_index, remove_uns=False)
		ext_rep =   [['HGNC:16873', '19_ref'],
		   ['MONDO:0007172', '22_ref'],
		   ['MONDO:0014823', '25_ref'],
		   ['HGNC:21197', '36_ref'],
		   ['HGNC:21197', '53_ref'],
		   ['HGNC:21144', '53_ref'],
		   ['MONDO:0009833', '53_ref'],
		   ['MONDO:0009594', '54_ref'],
		   ['HGNC:3527', '54_ref'],
		   ['MONDO:0012176', '62_ref'],
		   ['HGNC:21144', '66_ref'],
		   ['HGNC:21176', '1189_ref']]
		self.assertEqual(ext_rep, rep)
		self.assertEqual([], unrep)

	def test_link_table(self):
		input_linker = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_cluster'))
		indexed_linker = CmdTabs.index_array(input_linker)
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_gene'), "\t", 2)
		linked_test = CmdTabs.link_table(indexed_linker, input_table, False, "\t")
		expected_result = [["MONDO:0010193", "HGNC:3527", "54_ref"], ["MONDO:0008995", "HGNC:16873", "19_ref"], 
		["MONDO:0012866", "HGNC:21197"], ["MONDO:0017999", "HGNC:21197", "53_ref"], ["MONDO:0011142", "HGNC:21144", "66_ref"], 
		["MONDO:0013969", "HGNC:21176", "1189_ref"], ["MONDO:0018053", "HGNC:21157"]]
		self.assertEqual(expected_result, linked_test)

	def test_link_table_drop(self):
		input_linker = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_cluster'))
		indexed_linker = CmdTabs.index_array(input_linker)
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'disease_gene'), "\t", 2)
		linked_test = CmdTabs.link_table(indexed_linker, input_table, True, "\t")
		expected_result = [["MONDO:0010193", "HGNC:3527", "54_ref"], ["MONDO:0008995", "HGNC:16873", "19_ref"], 
		["MONDO:0017999", "HGNC:21197", "53_ref"], ["MONDO:0011142", "HGNC:21144", "66_ref"], 
		["MONDO:0013969", "HGNC:21176", "1189_ref"]]
		self.assertEqual(expected_result, linked_test)

	def test_tag_file(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_agg'))
		tags = CmdTabs.load_and_parse_tags([os.path.join(DATA_TEST_PATH, 'tracker')], "\t")
		taged_test = CmdTabs.tag_file(input_table, tags, False)
		expected_result = [['MERGED_net_no_raw_cpm', 'MERGED', 'no', 'no', 'cpm', 'HGNC:21197', '483_ref,1039_ref,1071_ref'], 
		['MERGED_net_no_raw_cpm', 'MERGED', 'no', 'no', 'cpm', 'HGNC:21143', '211_ref,4705_ref']]
		self.assertEqual(expected_result, taged_test)

	def test_tag_file_header(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_agg'))
		tags = CmdTabs.load_and_parse_tags([os.path.join(DATA_TEST_PATH, 'tracker')], "\t")
		taged_test = CmdTabs.tag_file(input_table, tags, True)
		expected_result = [['MERGED_net_no_raw_cpm', 'MERGED', 'no', 'no', 'cpm', 'HGNC:21143', '211_ref,4705_ref']]
		self.assertEqual(expected_result, taged_test)

	def test_filter_s_i(self):
		line = ["HGNC:21197", "483_ref", "1039_ref", "1071_ref"]
		col_filter = [0, 1, 2, 3]
		keywords = "HGNC&ref%ref%ref%ref"
		patterns =  CmdTabs.build_pattern(col_filter, keywords)
		filter_test = CmdTabs.filter(line, patterns, "s", "i")
		self.assertFalse(filter_test)

	def test_filter_s_i_True(self):
		line = ["HGNC:21197", "483_ref", "1039_ref", "1071_ref"]
		col_filter = [0, 1, 2, 3]
		keywords = "HGNC&ref%ref%ref%ref"
		patterns =  CmdTabs.build_pattern(col_filter, keywords)
		filter_test = CmdTabs.filter(line, patterns, "s", "i", True)
		self.assertTrue(filter_test)

	def test_filter_c_i(self):
		line = ["HGNC:21197", "483_ref", "1039_ref", "1071_ref"]
		col_filter = [0, 1, 2, 3]
		keywords = "ref%ref%ref%ref"
		patterns =  CmdTabs.build_pattern(col_filter, keywords)
		filter_test = CmdTabs.filter(line, patterns, "c", "i")
		self.assertTrue(filter_test)

	def test_filter_c_c(self):
		line = ["HGNC:21197", "483_ref", "1039_ref", "1071_ref"]
		col_filter = [0, 1, 2, 3]
		keywords = "HGNC&ref%ref%ref%ref"
		patterns =  CmdTabs.build_pattern(col_filter, keywords)
		filter_test = CmdTabs.filter(line, patterns, "c", "c")
		self.assertTrue(filter_test)

	def test_filter_columns(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_desagg'))
		options = {'col_filter' : [0], 'keywords' : "21197", 'search_mode' : "s", 'match_mode' : "i", 'reverse' : False, 'cols_to_show' : [0, 1]}
		filter_columns_test = CmdTabs.filter_columns(input_table, options)
		expected_result = [["HGNC:21197", "483_ref"], ["HGNC:21197", "1039_ref"], ["HGNC:21197", "1071_ref"]]
		self.assertEqual(expected_result, filter_columns_test)

	def test_filter_by_list(self):
		input_table = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'ids2count'))
		filterlist = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'filterlist'))
		filterlist = list(map(list, zip(*filterlist)))[0]
		filter_columns_test = CmdTabs.filter_by_whitelist(input_table, filterlist , 1)
		expected_result = [['000039', 'HP:0002140'],
		['000665', 'HP:0002140'],
		['000707', 'HP:0001082'],
		['000909', 'HP:0002315'],
		['000911', 'HP:0002140'],
		['000942', 'HP:0001082'],
		['000943', 'HP:0001082'],
		['001861', 'HP:0001082'],
		['002072', 'HP:0001082']]
		self.assertEqual(expected_result, filter_columns_test)


	def test_merge_and_filter_tables(self):
		options = {'header' : '', 'col_filter' : [0], 'keywords' : "0008995&0017999&0013969&0009594", 
			'search_mode' : "s", 'match_mode' : "i", 'reverse' : False, 'cols_to_show' : [0, 1], 'uniq' : False }
		input_tables = CmdTabs.load_several_files([os.path.join(DATA_TEST_PATH, 'disease_cluster'), os.path.join(DATA_TEST_PATH, 'disease_gene')])
		test_result = CmdTabs.merge_and_filter_tables(input_tables, options)
		expected_result = [["MONDO:0008995", "19_ref"], ["MONDO:0017999", "36_ref"], ["MONDO:0017999", "53_ref"], ["MONDO:0009594", "54_ref"], 
		["MONDO:0013969", "1189_ref"], ["MONDO:0008995", "HGNC:16873"], ["MONDO:0017999", "HGNC:21197"], ["MONDO:0013969", "HGNC:21176"]]
		self.assertEqual(expected_result, test_result)

	def test_load_files(self):
		loaded_files_ref = {
			os.path.join(DATA_TEST_PATH, "disease_gene") : [["MONDO:0010193", "HGNC:3527"], ["MONDO:0008995", "HGNC:16873"], ["MONDO:0012866", "HGNC:21197"], ["MONDO:0017999", "HGNC:21197"], ["MONDO:0011142", "HGNC:21144"], ["MONDO:0013969", "HGNC:21176"], ["MONDO:0018053", "HGNC:21157"]],
			os.path.join(DATA_TEST_PATH, "disease_cluster_uniq") : [["MONDO:0008995", "19_ref"], ["MONDO:0007172", "22_ref"], ["MONDO:0014823", "25_ref"], ["MONDO:0017999", "53_ref"], ["MONDO:0009833", "53_ref"], ["MONDO:0009594", "54_ref"], ["MONDO:0010193", "54_ref"], ["MONDO:0012176", "62_ref"], ["MONDO:0011142", "66_ref"], ["MONDO:0013969", "1189_ref"]]}
		loaded_files_to_test = CmdTabs.load_files([os.path.join(DATA_TEST_PATH, "disease_gene"), os.path.join(DATA_TEST_PATH, "disease_cluster_uniq")])
		self.assertEqual(loaded_files_ref, loaded_files_to_test)

	def test_merge_files(self):
		merged_ref_file = [["MONDO:0010193", "HGNC:3527", "54_ref"], ["MONDO:0008995", "HGNC:16873", "19_ref"], ["MONDO:0012866", "HGNC:21197", "-"], ["MONDO:0017999", "HGNC:21197", "53_ref"], ["MONDO:0011142", "HGNC:21144", "66_ref"], ["MONDO:0013969", "HGNC:21176", "1189_ref"], ["MONDO:0018053", "HGNC:21157", "-"], ["MONDO:0007172", "-", "22_ref"], ["MONDO:0014823", "-", "25_ref"], ["MONDO:0009833", "-", "53_ref"], ["MONDO:0009594", "-", "54_ref"], ["MONDO:0012176", "-", "62_ref"]]
		loaded_files_to_test = CmdTabs.load_files([os.path.join(DATA_TEST_PATH, "disease_gene"), os.path.join(DATA_TEST_PATH, "disease_cluster_uniq")])
		merged_files_to_test = CmdTabs.merge_files(loaded_files_to_test)
		self.assertEqual(merged_ref_file, merged_files_to_test)
