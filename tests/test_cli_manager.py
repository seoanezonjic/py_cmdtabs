import pytest
import sys
import os 
from io import StringIO
from py_cmdtabs import CmdTabs
import py_cmdtabs #TODO(Fred): Dont know if this is correct.
ROOT_PATH=os.path.dirname(__file__)
DATA_TEST_PATH = os.path.join(ROOT_PATH, 'data_tests')
TRANS_DATA_TEST_PATH = os.path.join(DATA_TEST_PATH, 'transposed')
REF_DATA_PATH=os.path.join(DATA_TEST_PATH, 'ref_output_scripts')

def capture_stdout(func):
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        tmpfile = StringIO()
        sys.stdout = tmpfile
        returned = func(*args, **kwargs)
        printed = sys.stdout.getvalue()
        sys.stdout = original_stdout
        return returned, printed
    return wrapper

def strng2table(strng, fs="\t", rs="\n"):
	return  [row.split(fs) for row in strng.split(rs)][0:-1]

def test_aggregate_column_tanspose():
	input_file = os.path.join(TRANS_DATA_TEST_PATH, 'cluster_genes_dis_desagg')
	args = f"-i {input_file} -x 1 -s , -a 2 --transposed".split(" ")
	@capture_stdout
	def aggr(lsargs):
		return py_cmdtabs.aggregate_column_data(lsargs)
	_, printed = aggr(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_cluster_genes_dis_AGG'))
	assert expected_result == test_result

def test_aggregate_column():
	input_file = os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_desagg')
	args = f"-i {input_file} -x 1 -s , -a 2".split(" ") 
	@capture_stdout
	def aggr(lsargs):
		return py_cmdtabs.aggregate_column_data(lsargs)
	_, printed = aggr(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'cluster_genes_dis_AGG'))
	assert expected_result == test_result

def test_desaggregate_column():
	input_file = os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_agg')
	args = f"-i {input_file} -x 2".split(" ") 
	@capture_stdout
	def aggr(lsargs):
		return py_cmdtabs.desaggregate_column_data(lsargs)

	_, printed = aggr(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'cluster_genes_dis_DESAGG'))
	assert expected_result == test_result

def test_desaggregate_column_transposed():
	input_file = os.path.join(TRANS_DATA_TEST_PATH, 'cluster_genes_dis_agg')
	args = f"-i {input_file} -x 2 --transposed".split(" ") 
	@capture_stdout
	def aggr(lsargs):
		return py_cmdtabs.desaggregate_column_data(lsargs)

	_, printed = aggr(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_cluster_genes_dis_DESAGG'))
	assert expected_result == test_result


""" create_metric_table $test_data/all_metrics sample $out/metric_table -c $out/TEST_file

def test_create_metric_table():
	input_file = os.path.join(DATA_TEST_PATH, 'all_metrics')
	args = f"-i {input_file} sample-x 2".split(" ") 
	@capture_stdout
	def aggr(lsargs):
		return py_cmdtabs.desaggregate_column_data(lsargs)

	_, printed = aggr(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'cluster_genes_dis_DESAGG_to_test')) 
	assert expected_result == test_result """