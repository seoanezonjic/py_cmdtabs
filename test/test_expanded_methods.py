import unittest
import os
from py_cmdtabs import CmdTabs
ROOT_PATH=os.path.dirname(__file__)
DATA_TEST_PATH = os.path.join(ROOT_PATH, 'data_tests')

class ExpandedTestCase(unittest.TestCase):
	def test_extract_fields(self):
		line = ["HGNC:21197", "483_ref", "1039_ref", "1071_ref"]
		cols_to_show = [0]
		test_result = CmdTabs.extract_fields(line, cols_to_show)
		expected_result = ["HGNC:21197"]
		self.assertEqual(expected_result, test_result)

	def test_expanded_match_i(self):
		string = "Hello world"
		pattern = "Hello"
		match_test = CmdTabs.expanded_match(string, pattern, "i")
		self.assertTrue(match_test)

	def test_expanded_match_c(self):
		string = "Hello world"
		pattern = "Hello"
		match_test = CmdTabs.expanded_match(string, pattern, "c")
		self.assertFalse(match_test)

	def test_extract_columns(self):
		sheet = CmdTabs.get_table_from_excel(os.path.join(DATA_TEST_PATH, 'cluster_genes.xlsx'), 0)
		test_result = CmdTabs.extract_columns(sheet, [0, 2])
		expected_result =[['HGNC:21197', '1039_ref'], ['HGNC:21143', '4705_ref']]
		self.assertEqual(expected_result, test_result)