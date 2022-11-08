import unittest
import os
from py_cmdtabs import CmdTabs
ROOT_PATH=os.path.dirname(__file__)
DATA_TEST_PATH = os.path.join(ROOT_PATH, 'data_tests')

class IOTestCase(unittest.TestCase):

	def test_load_input_data(self):
		input_file = os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_agg')
		load_data_test = CmdTabs.load_input_data(input_file)
		expected_result = [['HGNC:21197', '483_ref,1039_ref,1071_ref'], ['HGNC:21143', '211_ref,4705_ref']]
		self.assertEqual(expected_result, load_data_test)

if __name__ == '__main__':
    unittest.main()