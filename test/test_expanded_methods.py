import unittest
import os
import openpyxl
from py_cmdtabs import CmdTabs
ROOT_PATH=os.path.dirname(__file__)
DATA_TEST_PATH = os.path.join(ROOT_PATH, 'data_tests')

class ExpandedTestCase(unittest.TestCase):
	def test_shift_by_array_indexes(self):
		line = ["HGNC:21197", "483_ref", "1039_ref", "1071_ref"]
		cols_to_show = [0]
		test_result = CmdTabs.shift_by_array_indexes(line, cols_to_show)
		expected_result = ["HGNC:21197"]
		self.assertEqual(expected_result, test_result)

	def test_expanded_match_i(self):
		string = "Hello world"
		pattern = "Hello"
		match_test = CmdTabs.expanded_match(string, pattern, "i")
		expected_result = True
		self.assertEqual(expected_result, match_test)

	def test_expanded_match_c(self):
		string = "Hello world"
		pattern = "Hello"
		match_test = CmdTabs.expanded_match(string, pattern, "c")
		expected_result = False
		self.assertEqual(expected_result, match_test)

	def test_extract_columns(self):
		x = openpyxl.load_workbook(os.path.join(DATA_TEST_PATH, 'cluster_genes.xlsx'))
		x.active=1
		#sheet = x.sheets[0].to_a
		test_result = CmdTabs.extract_columns(x, [0, 2])
		expected_result =[['HGNC:21197', '1039_ref'], ['HGNC:21143', '4705_ref']]
		self.assertEqual(expected_result, test_result)