import pytest
import sys
import os
import gzip
import io 
from io import StringIO, BytesIO
from contextlib import redirect_stdout
from base64 import b64encode
from py_cmdtabs import CmdTabs
import py_cmdtabs 
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

	input_file_3_cols = os.path.join(DATA_TEST_PATH, 'agg_data_3_columns.txt')
	args=f"-i {input_file_3_cols} -x 1 -a 2,3 -s ,"
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.aggregate_column_data(lsargs)
	_, printed = script2test(args.split(" "))
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'agg_data_3_columns_result.txt'))
	assert expected_result == test_result

	#Testing new aggregation modes
	input_2index_2values = os.path.join(DATA_TEST_PATH, 'agg_2index_2values.txt')
	args=f"-i {input_2index_2values} -x 1,2 -a 3,4 -A mean"
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.aggregate_column_data(lsargs)
	_, printed = script2test(args.split(" "))
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'agg_2index_2values.txt'))
	assert expected_result == test_result

def test_aggregate_column_tanspose():
	input_file = os.path.join(TRANS_DATA_TEST_PATH, 'cluster_genes_dis_desagg')
	args = f"-i {input_file} -x 1 -s , -a 2 --transposed".split(" ")
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.aggregate_column_data(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False 
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

	#Testing desaggregation with multiple columns
	input_file = os.path.join(REF_DATA_PATH, 'agg_data_3_columns_result.txt')
	args = f"-i {input_file} -x 2,3".split(" ") 
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.desaggregate_column_data(lsargs)

	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(DATA_TEST_PATH, 'agg_data_3_columns.txt'))
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

def test_get_columns():
	#Testing with a table with header flag, using column names to subset
	input_file = os.path.join(DATA_TEST_PATH, 'simple_table')

	reference = [["col-1", "col-3", "col-4", "col-5"],
				 ["1",		"3", 	"4", 		"5"],
				 ["6",		"8", 	"9", 		"10"],
				 ["11",		"13", 	"14", 		"15"]]
	
	args = f"-i {input_file} -H -c col-1,col-3%-%col-5".split(" ")
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.get_columns(lsargs)
	_, printed = script2test(args)
	test_result = strng2table(printed)
	assert test_result == reference

	#Testing with a table without using header flag, then indicating columns by indexes to subset the same column of the table
	args = f"-i {input_file} -c 1,3-5".split(" ")
	_, printed = script2test(args)
	test_result = strng2table(printed)
	assert test_result == reference
	

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
	input_file2 = os.path.join(DATA_TEST_PATH, 'tracker')
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
	expected_result = sort_table(CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_intersect_columns_default'), add_empty_fields=False), sort_by=0, transposed=True)
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

	out_file = os.path.join(tmp_dir, 'linked_table')
	input_file3 = os.path.join(DATA_TEST_PATH, 'dis_gene_attrs')
	expected_result_file= os.path.join(REF_DATA_PATH, 'linked_table3')
	args = f"-i {input_file1} -l {input_file3} --columns2linker 2,3,4 --drop -o {out_file}".split(" ") 
	_, printed = script2test(args)
	test_result_file = CmdTabs.load_input_data(out_file) 
	expected_result_file = CmdTabs.load_input_data(expected_result_file) 
	assert test_result_file == expected_result_file


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


def test_standard_name_replacer(tmp_dir):
	input_file1 = os.path.join(DATA_TEST_PATH, 'disease_cluster')
	input_file2 = os.path.join(DATA_TEST_PATH, 'disease_gene')
	out_file1 = os.path.join(tmp_dir, 'replaced_name')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.standard_name_replacer(lsargs)

	args = f"-i {input_file1} -I {input_file2} -o {out_file1} -c 1 -f 1 -t 2".split(" ") 
	script2test(args)
	test_result = CmdTabs.load_input_data(out_file1) 
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'replaced_name'))
	assert expected_result == test_result
	
def test_standard_name_replacer_untraslated(tmp_dir):
	input_file1 = os.path.join(DATA_TEST_PATH, 'disease_cluster')
	input_file2 = os.path.join(DATA_TEST_PATH, 'disease_gene')
	out_file1 = os.path.join(tmp_dir, 'replaced_name_untranslated')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.standard_name_replacer(lsargs)

	args = f"-i {input_file1} -I {input_file2} -o {out_file1} -c 1 -f 1 -t 2 -u".split(" ") 
	script2test(args)
	test_result = CmdTabs.load_input_data(out_file1) 
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'replaced_name_untranslated'))
	assert expected_result == test_result

def test_standard_name_replacer_transposed(tmp_dir):
	input_file1 = os.path.join(TRANS_DATA_TEST_PATH, 'disease_cluster')
	input_file2 = os.path.join(DATA_TEST_PATH, 'disease_gene')
	out_file1 = os.path.join(tmp_dir, 'transposed_replaced_name')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.standard_name_replacer(lsargs)

	args = f"-i {input_file1} -I {input_file2} -o {out_file1} -c 1 -f 1 -t 2 --transposed".split(" ") 
	script2test(args)
	CmdTabs.transposed = False
	test_result = CmdTabs.load_input_data(out_file1) 
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_replaced_name'))
	assert expected_result == test_result


def test_excel_to_tabular(tmp_dir):
	input_file1 = os.path.join(DATA_TEST_PATH, 'cluster_genes.xlsx')
	out_file1 = os.path.join(tmp_dir, 'cluster_genes_from_excel.txt')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.excel_to_tabular(lsargs)

	args = f"-i {input_file1} -c 2,3,4 -s 1 -o {out_file1}".split(" ") 
	script2test(args)
	test_result = CmdTabs.load_input_data(out_file1) 
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'cluster_genes_from_excel.txt'))
	assert expected_result == test_result

def test_excel_to_tabular_transposed(tmp_dir):
	input_file1 = os.path.join(TRANS_DATA_TEST_PATH, 'cluster_genes.xlsx')
	out_file1 = os.path.join(tmp_dir, 'transposed_cluster_genes_from_excel.txt')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.excel_to_tabular(lsargs)
	args = f"-i {input_file1} -c 2,3,4 -s 1 -o {out_file1} --transposed".split(" ") 
	script2test(args)
	test_result = CmdTabs.load_input_data(out_file1) 
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_cluster_genes_from_excel.txt'))
	assert expected_result == test_result


def test_column_filter():
	input_file = os.path.join(DATA_TEST_PATH, 'disease*')
	argsls = [[f"-t {input_file} -c 1,2 -f 1 -k MONDO:0008995 -s c -m c", "column_matching_hard"],
			  [f"-t {input_file} -c 1,2 -f 1 -k MONDO -s c -m i", "column_matching_soft"],
			  [f"-t {input_file} -c 1,2 -f 1 -k MONDO:0008995&MONDO:0017999 -s c -m c", "column_matching_hard_various_keys"],
			  [f"-t {input_file} -c 1,2 -f 1,2 -k MONDO:0008995&MONDO:0017999%53_ref -s c -m c", "column_matching_hard_various_keys_and_every_columns"],
			  [f"-t {input_file} -c 1,2 -f 1,2 -k MONDO:0008995&MONDO:0017999%53_ref -s c -m c -H", "column_matching_hard_various_keys_and_every_columns_header"],
			  [f"-t {input_file} -c 1,2 -f 1,2 -k MONDO:0008995&MONDO:0017999%53_ref -s s -m c","column_matching_hard_various_keys_and_some_columns"],
			  [f"-t {input_file} -c 1,2 -f 1,2 -k MONDO%ref -s s -m i", "column_matching_soft_and_some_columns"],
			  [f"-t {input_file} -c 1,2 -f 1,2 -k MONDO%ref -s c -m i", "column_matching_soft_and_every_columns"],
			  [f"-t {input_file} -c 1 -f 1 -k MONDO -s c -m i", "column_matching_soft_1_column"],
			  [f"-t {input_file} -c 1 -f 1 -k MONDO -s c -m i -u", "column_matching_soft_1_column_uniq"],
			  [f"-t {input_file} -c 1 -f 1 -k 17 -s c -m i -r", "column_matching_soft_1_column_reverse"]]
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.column_filter(lsargs)

	for str_script, out_name in argsls:
		args = str_script.split(" ")
		_, printed = script2test(args)
		test_result = sort_table(strng2table(printed), sort_by=0)
		if len(test_result[0]) > 1:
			test_result = sort_table(test_result, sort_by=1)
		expected_result = sort_table(CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, out_name)), sort_by=0)
		if len(expected_result[0]) > 1:
			expected_result = sort_table(expected_result, sort_by=1)
		assert expected_result == test_result

def test_column_filter_transposed():
	input_file = os.path.join(TRANS_DATA_TEST_PATH, 'disease*')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.column_filter(lsargs)
	args = f"-t {input_file} -c 1,2 -f 1 -k MONDO:0008995 -s c -m c --transposed".split(" ") 
	_, printed = script2test(args)
	test_result = strng2table(printed)
	CmdTabs.transposed = False
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'transposed_column_matching_hard'))
	assert expected_result == test_result


def test_records_count():
	input_file = os.path.join(DATA_TEST_PATH, 'ids2count')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.records_count(lsargs)
	args = f"-i {input_file} -x 2".split(" ") 
	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'ids2count'))
	assert expected_result == test_result


def test_filter_by_list(tmp_dir):
	input_table = os.path.join(DATA_TEST_PATH, 'ids2count')
	filterlist = os.path.join(DATA_TEST_PATH, 'filterlist')
	out_file = os.path.join(tmp_dir, 'filter_ids2count')
	args = f"-f {input_table} -c 2 -t {filterlist} --prefix filter_ -o {tmp_dir} --metrics".split(" ")
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.filter_by_list(lsargs)
	_, printed = script2test(args)
	test_result = CmdTabs.load_input_data(out_file)
	expected_result = [['000039', 'HP:0002140'],
		['000665', 'HP:0002140'],
		['000707', 'HP:0001082'],
		['000909', 'HP:0002315'],
		['000911', 'HP:0002140'],
		['000942', 'HP:0001082'],
		['000943', 'HP:0001082'],
		['001861', 'HP:0001082'],
		['002072', 'HP:0001082']]
	assert expected_result == test_result

def test_filter_by_list_partial_match(tmp_dir):
	input_table = os.path.join(DATA_TEST_PATH, 'ids2count')
	filterlist = os.path.join(DATA_TEST_PATH, 'filterlist_partial')
	out_file = os.path.join(tmp_dir, 'filter_ids2count')
	args = f"-f {input_table} -c 2 -t {filterlist} --prefix filter_ -o {tmp_dir} --metrics --not_exact_match".split(" ")
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.filter_by_list(lsargs)
	_, printed = script2test(args)
	test_result = CmdTabs.load_input_data(out_file)
	expected_result = [['000039', 'HP:0002140'],
		['000665', 'HP:0002140'],
		['000707', 'HP:0001082'],
		['000909', 'HP:0002315'],
		['000911', 'HP:0002140'],
		['000942', 'HP:0001082'],
		['000943', 'HP:0001082'],
		['001861', 'HP:0001082'],
		['002072', 'HP:0001082']]
	assert expected_result == test_result

def test_filter_by_list_blacklist_case(tmp_dir):
	input_table = os.path.join(DATA_TEST_PATH, 'ids2count_short')
	filterlist = os.path.join(DATA_TEST_PATH, 'blacklist')
	out_file = os.path.join(tmp_dir, 'filter_ids2count_short')
	args = f"-f {input_table} -c 2 -t {filterlist} --prefix filter_ -o {tmp_dir} --metrics --blacklist".split(" ")
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.filter_by_list(lsargs)
	_, printed = script2test(args)
	test_result = CmdTabs.load_input_data(out_file)
	expected_result = [['000707', 'HP:0001082'],
						['000909', 'HP:0002315']]
	assert expected_result == test_result

def test_filter_by_list_blacklist_case_partial_match(tmp_dir):
	input_table = os.path.join(DATA_TEST_PATH, 'ids2count_short')
	filterlist = os.path.join(DATA_TEST_PATH, 'blacklist_partial')
	out_file = os.path.join(tmp_dir, 'filter_ids2count_short')
	args = f"-f {input_table} -c 2 -t {filterlist} --prefix filter_ -o {tmp_dir} --metrics --blacklist --not_exact_match".split(" ")
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.filter_by_list(lsargs)
	_, printed = script2test(args)
	test_result = CmdTabs.load_input_data(out_file)
	expected_result = [['000707', 'HP:0001082'],
						['000909', 'HP:0002315']]
	assert expected_result == test_result

def test_records_count():
	input_file = os.path.join(DATA_TEST_PATH, 'ids2count')
	@capture_stdout
	def script2test(lsargs):
		return py_cmdtabs.records_count(lsargs)
	args = f"-i {input_file} -x 2".split(" ") 
	_, printed = script2test(args)
	test_result = strng2table(printed)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'ids2count'))
	assert expected_result == test_result


def test_subset_table(tmp_dir):
	input_file = os.path.join(DATA_TEST_PATH, 'hp_long_list.txt')
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'subset_table'))
	out_file = os.path.join(tmp_dir, 'subset_table')
	args = f"-i {input_file} -s 10 -l 10 -o {out_file}".split(" ")
	
	py_cmdtabs.subset_table(args)
	returned = CmdTabs.load_input_data(out_file)
	assert expected_result == returned

	# Testing with the --chunk_size option
	chunk_size = 2
	input_file = os.path.join(DATA_TEST_PATH, 'mondo_genes')
	out_folder = os.path.join(tmp_dir, 'subset_table_chunks')	
	args = f"-i {input_file} -k {chunk_size} -o {out_folder}".split(" ")
	py_cmdtabs.subset_table(args)
	
	expected_results = CmdTabs.load_input_data(input_file)
	for idx, file in enumerate(sorted(os.listdir(out_folder))):

		returned = CmdTabs.load_input_data(os.path.join(out_folder, file))
		assert returned == expected_results[chunk_size*idx:chunk_size*(idx+1)]

	# Testing with the --number_of_files option
	n_files = 3
	out_folder2 = os.path.join(tmp_dir, 'subset_table_chunks2')	
	args = f"-i {input_file} -n {n_files} -o {out_folder2}".split(" ")
	py_cmdtabs.subset_table(args)
	
	for idx, file in enumerate(sorted(os.listdir(out_folder2))):
		returned = CmdTabs.load_input_data(os.path.join(out_folder2, file))
		expected = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, "subset_table_fold", file))
		assert returned == expected	

def test_transpose_table(tmp_dir):
	input_file = os.path.join(DATA_TEST_PATH, 'mondo_genes')
	out_file = os.path.join(tmp_dir, 'mondo_genes_transposed')
	args = f"-i {input_file} -o {out_file}".split(" ")
	py_cmdtabs.transpose_table(args)
	
	returned = CmdTabs.load_input_data(out_file)
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'mondo_genes_transposed'))
	assert expected_result == returned

def test_transpose_table_compressed_file(tmp_dir):
	expected_result = CmdTabs.load_input_data(os.path.join(REF_DATA_PATH, 'mondo_genes_transposed'))

	###### TESTING WITH COMPRESSED INPUT AND UNCOMPRESSED OUTPUT
	input_file = os.path.join(DATA_TEST_PATH, 'mondo_genes.gz')
	out_file = os.path.join(tmp_dir, 'mondo_genes_transposed')
	args = f"-i {input_file} -o {out_file} --compressed_in".split(" ")
	py_cmdtabs.transpose_table(args)

	CmdTabs.compressed_input = False
	returned = CmdTabs.load_input_data(out_file)
	assert expected_result == returned


	###### TESTING WITH UNCOMPRESSED INPUT AND COMPRESSED OUTPUT
	input_file = os.path.join(DATA_TEST_PATH, 'mondo_genes')
	out_file = os.path.join(tmp_dir, 'mondo_genes_transposed.gz')
	args = f"-i {input_file} -o {out_file} --compressed_out".split(" ")
	py_cmdtabs.transpose_table(args)

	CmdTabs.compressed_input = True
	returned = CmdTabs.load_input_data(out_file)
	assert expected_result == returned
	CmdTabs.compressed_input = False
	CmdTabs.compressed_output = False


	###### TESTING WITH COMPRESSED INPUT AND COMPRESSED OUTPUT
	input_file = os.path.join(DATA_TEST_PATH, 'mondo_genes.gz')
	out_file = os.path.join(tmp_dir, 'mondo_genes_transposed.gz')
	args = f"-i {input_file} -o {out_file} --compressed_in --compressed_out".split(" ")
	py_cmdtabs.transpose_table(args)
	
	returned = CmdTabs.load_input_data(out_file)
	assert expected_result == returned
	CmdTabs.compressed_input = False
	CmdTabs.compressed_output = False