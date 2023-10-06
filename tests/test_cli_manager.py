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


@pytest.fixture(scope="session")
def tmp_dir(tmpdir_factory):
    fn = tmpdir_factory.mktemp("./tmp_output")
    return fn


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
	table = [row.split(fs) for row in strng.split(rs)][0:-1]
	return table

def sort_table(table, sort_by, transposed=False):
	if transposed: 
		table = list(map(list, zip(*table)))
		table = sorted(table, key= lambda row: row[sort_by])
		table = list(map(list, zip(*table)))
	else:
		table = sorted(table, key= lambda row: row[sort_by])
	return table

def test_aggregate_column():
	input_file = os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_desagg')
	args = f"-i {input_file} -x 1 -s , -a 2".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.aggregate_column_data(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'cluster_genes_dis_AGG'))
	assert expected_result == test_result

def test_aggregate_column_tanspose():
	input_file = os.path.join(TRANS_DATA_TEST_PATH, 'cluster_genes_dis_desagg')
	args = f"-i {input_file} -x 1 -s , -a 2 --transposed".split(" ")
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.aggregate_column_data(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False #TODO: Check this part.
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_cluster_genes_dis_AGG'))
	assert expected_result == test_result

def test_desaggregate_column():
	input_file = os.path.join(DATA_TEST_PATH, 'cluster_genes_dis_agg')
	args = f"-i {input_file} -x 2".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.desaggregate_column_data(lsargs)

	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'cluster_genes_dis_DESAGG'))
	assert expected_result == test_result

def test_desaggregate_column_transposed():
	input_file = os.path.join(TRANS_DATA_TEST_PATH, 'cluster_genes_dis_agg')
	args = f"-i {input_file} -x 2 --transposed".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.desaggregate_column_data(lsargs)

	_, printed = script2test(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_cluster_genes_dis_DESAGG'))
	assert expected_result == test_result


def test_create_metric_table(tmp_dir):
	input_file = os.path.join(DATA_TEST_PATH, 'all_metrics')
	out_file1 = os.path.join(tmp_dir, 'metric_table')
	out_file2 = os.path.join(tmp_dir, 'TEST_file')
	expected_result_file1 = os.path.join(REF_DATA_PATH, 'metric_table')
	expected_result_file2 = os.path.join(REF_DATA_PATH, 'TEST_file')

	args = f"{input_file} sample {out_file1} -c {out_file2}".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.create_metric_table(lsargs)
	script2test(args)

	test_result_file1 = CmdTabs.load_input_data(out_file1) 
	test_result_file2 = CmdTabs.load_input_data(out_file2) 
	expected_result_file1 = CmdTabs.load_input_data(expected_result_file1) 
	expected_result_file2 = CmdTabs.load_input_data(expected_result_file2) 
	assert expected_result_file1 == test_result_file1
	assert expected_result_file2 == test_result_file2


def test_create_metric_table_transpose(tmp_dir):
	input_file = os.path.join(TRANS_DATA_TEST_PATH, 'all_metrics')
	out_file1 = os.path.join(tmp_dir, 'metric_table')
	out_file2 = os.path.join(tmp_dir, 'TEST_file')
	expected_result_file1 = os.path.join(REF_DATA_PATH, 'transposed_metric_table')
	expected_result_file2 = os.path.join(REF_DATA_PATH, 'TEST_file_transposed')

	args = f"{input_file} sample {out_file1} -c {out_file2} --transposed".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.create_metric_table(lsargs)
	script2test(args)

	test_result_file1 = CmdTabs.load_input_data(out_file1) 
	test_result_file2 = CmdTabs.load_input_data(out_file2) 
	expected_result_file1 = CmdTabs.load_input_data(expected_result_file1) 
	expected_result_file2 = CmdTabs.load_input_data(expected_result_file2) 
	assert expected_result_file1 == test_result_file1
	assert expected_result_file2 == test_result_file2


def test_merge_tabular():
	input_file1 = os.path.join(DATA_TEST_PATH, 'disease_gene')
	input_file2 = os.path.join(DATA_TEST_PATH, 'disease_cluster_uniq')
	args = f"{input_file1} {input_file2}".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.merge_tabular(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'merge_disease_cluster_gene'))
	assert expected_result == test_result

def test_merge_tabular_transpose():
	input_file1 = os.path.join(TRANS_DATA_TEST_PATH, 'disease_gene')
	input_file2 = os.path.join(TRANS_DATA_TEST_PATH, 'disease_cluster_uniq')
	args = f"{input_file1} {input_file2} --transposed".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.merge_tabular(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_merge_disease_cluster_gene'))
	assert expected_result == test_result

def test_tag_table():
	input_file1 = os.path.join(DATA_TEST_PATH, 'cluster_stats')
	input_file2 = os.path.join(DATA_TEST_PATH, 'tracker')
	args = f"-i {input_file1} -t {input_file2}".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.tag_table(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'tag_table'))
	assert expected_result == test_result

	args = f"-i {input_file1} -H -t {input_file2}".split(" ") 
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'tag_table_header'))
	assert expected_result == test_result

def test_tag_table_transpose():
	input_file1 = os.path.join(TRANS_DATA_TEST_PATH, 'cluster_stats')
	input_file2 = os.path.join(TRANS_DATA_TEST_PATH, 'tracker')
	args = f"-i {input_file1} -t {input_file2} --transposed".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.tag_table(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_tag_table'))
	assert expected_result == test_result

def test_intersect_columns():
	input_file1 = os.path.join(DATA_TEST_PATH, 'disease_cluster')
	input_file2 = os.path.join(DATA_TEST_PATH, 'disease_gene')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.intersect_columns(lsargs)

	#Default case:
	args = f"-a {input_file1} -b {input_file2} -A 1 -B 1".split(" ") 
	_, printed = script2test(args)
	test_result = sort_table(strng2table(printed), sort_by=0)
	expected_result = sort_table(CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'intersect_columns_default')), sort_by=0)
	assert expected_result == test_result

	# With -c flag:
	args = f"-a {input_file1} -b {input_file2} -A 1 -B 1 -c".split(" ") 
	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'intersect_columns_count'))
	assert expected_result == test_result

	# With full
	args = f"-a {input_file1} -b {input_file2} -A 1 -B 1 --full".split(" ") 
	_, printed = script2test(args)
	test_result = sort_table(strng2table(printed), sort_by=0)
	expected_result = sort_table(CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'intersect_columns_full')), sort_by = 0)
	assert expected_result == test_result

def test_intersect_columns_transpose():
	input_file1 = os.path.join(TRANS_DATA_TEST_PATH, 'disease_cluster')
	input_file2 = os.path.join(TRANS_DATA_TEST_PATH, 'disease_gene')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.intersect_columns(lsargs)

	args = f"-a {input_file1} -b {input_file2} -A 1 -B 1 --transposed".split(" ") 
	_, printed = script2test(args)
	test_result = sort_table(strng2table(printed), sort_by=0, transposed=True)
	CmdTabs.transposed = False
	expected_result = sort_table(CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_intersect_columns_default')), sort_by=0, transposed=True)
	assert expected_result == test_result


def test_table_linker(tmp_dir):
	input_file1 = os.path.join(DATA_TEST_PATH, 'disease_cluster')
	input_file2 = os.path.join(DATA_TEST_PATH, 'disease_gene')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.table_linker(lsargs)


	out_file = os.path.join(tmp_dir, 'linked_table')
	expected_result_file= os.path.join(REF_DATA_PATH, 'linked_table')
	args = f"-i {input_file1} -l {input_file2} -o {out_file}".split(" ") 
	script2test(args)
	test_result_file = CmdTabs.load_input_data(out_file) 
	expected_result_file = CmdTabs.load_input_data(expected_result_file) 
	assert expected_result_file == test_result_file


	out_file = os.path.join(tmp_dir, 'linked_table_2')
	expected_result_file= os.path.join(REF_DATA_PATH, 'linked_table_2')
	args = f"-i {input_file2} -l {input_file1} -o {out_file}".split(" ")
	script2test(args)
	test_result_file = CmdTabs.load_input_data(out_file) 
	expected_result_file = CmdTabs.load_input_data(expected_result_file)
	assert expected_result_file == test_result_file

	out_file = os.path.join(tmp_dir, 'linked_table_matches')
	expected_result_file= os.path.join(REF_DATA_PATH, 'linked_table_matches')
	args = f"-i {input_file1} -l {input_file2} -o {out_file} --drop".split(" ")
	script2test(args)
	test_result_file = CmdTabs.load_input_data(out_file) 
	expected_result_file = CmdTabs.load_input_data(expected_result_file)
	assert expected_result_file == test_result_file

def test_table_linker_transpose(tmp_dir):
	input_file1 = os.path.join(TRANS_DATA_TEST_PATH, 'disease_cluster')
	input_file2 = os.path.join(TRANS_DATA_TEST_PATH, 'disease_gene')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.table_linker(lsargs)


	out_file = os.path.join(tmp_dir, 'transposed_linked_table')
	expected_result_file= os.path.join(REF_DATA_PATH, 'transposed_linked_table')
	args = f"-i {input_file1} -l {input_file2} -o {out_file} --transposed".split(" ") 
	script2test(args)
	CmdTabs.transposed = False
	test_result_file = CmdTabs.load_input_data(out_file) 
	expected_result_file = CmdTabs.load_input_data(expected_result_file) 
	assert expected_result_file == test_result_file



