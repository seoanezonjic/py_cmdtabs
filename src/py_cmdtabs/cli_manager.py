import argparse
import sys
import os
import glob

from py_cmdtabs.cmdtabs import CmdTabs

## TYPES
def based_0(string): return int(string) - 1
def list_based_0(string): return CmdTabs.parse_column_indices(",", string)
def list_str(values): return values.split(',')

## Common options
def add_common_options(parser):
    parser.add_argument("-i", "--input_file", dest="input_file",
      help="Path to input file")
    parser.add_argument("-x", "--column_index", dest="col_index",
      help="Column index (1 based) to use as reference", type=based_0)
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
      help="Indicate if files have header")
    parser.add_argument("--transposed", default=False, action="store_true", help="To perform the operations in rows and not columns")

##############################################

def aggregate_column_data(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("-s", "--separator", dest="sep", default=",",
      help="Character separator when collapse data")
    parser.add_argument("-a", "--column_aggregate", dest="col_aggregate",
      help="Column index (1 based) to extract data and join for each id in column index", type=based_0)
    
    opts =  parser.parse_args(args)
    main_aggregate_column_data(opts)

def main_aggregate_column_data(options):
    CmdTabs.transposed = options.transposed
    input_table = CmdTabs.load_input_data(options.input_file)
    agg_data = CmdTabs.aggregate_column(input_table, options.col_index, options.col_aggregate, options.sep)
    CmdTabs.write_output_data(agg_data)

def column_filter(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Get records from table an extract desired columns.')
    add_common_options(parser)
    parser.add_argument("-t", "--table_file", dest="table_file",
      help="Input tabulated file")
    parser.add_argument("-c", "--column", dest="cols_to_show", type=list_based_0,
      help="Column/s to show (1 based). Format: x,y,z..")
    parser.add_argument("-f", "--col_filter", dest="col_filter", type=list_based_0,
      help="Select columns where search keywords. Format: x,y,z..")
    parser.add_argument("-p", "--separator", dest="separator", default="\t",
      help="Column character separator")
    parser.add_argument("-k", "--keywords", dest="keywords",
      help="Keywords for select rows. Format: key1_col1&key2_col1%%key1_col2&key2_col2")
    parser.add_argument("-s", "--search", dest="search_mode", default='c', choices=['c', 's'],
      help="c for match in every columns set, s some match in some column. Default c")
    parser.add_argument("-m", "--match_mode", dest="match_mode", default='i', choices=['i', 'c'],
      help="i string must include the keyword, c for fullmatch. Default i")
    parser.add_argument("-r", "--reverse", dest="reverse", default=False, action='store_true',
      help="Select not matching")
    parser.add_argument("-u", "--uniq", dest="uniq", default=False, action='store_true',
      help="Delete redundant items")
        
    opts = parser.parse_args(args)
    main_column_filter(opts)

def main_column_filter(options):
    if options.table_file == None: sys.exit('Tabulated file not specified') 
    CmdTabs.transposed = options.transposed
    file_names = glob.glob(options.table_file)
    input_files = CmdTabs.load_several_files(file_names, options.separator)
    filtered_table = CmdTabs.merge_and_filter_tables(input_files, vars(options))
    CmdTabs.write_output_data(filtered_table)

def create_metric_table(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("metric_file", metavar='M',
      help="File with tabulated metrics")
    parser.add_argument("attributes", metavar='A',
      help="String with comma separated attributes")
    parser.add_argument("output_file", metavar='O',
      help="Output file path")
    parser.add_argument("-c", "--corrupted", dest="corrupted",
      help="File where corrupted metrics are stored")
    
    opts = parser.parse_args(args)
    main_create_metric_table(opts)

def main_create_metric_table(options):
    CmdTabs.transposed = options.transposed
    metric_file = CmdTabs.load_input_data(options.metric_file)
    attributes = options.attributes.split(',')
    samples_tag = attributes.pop(0)
    metric_names, indexed_metrics = CmdTabs.index_metrics(metric_file, attributes)
    table_output, corrupted_records = CmdTabs.create_table(indexed_metrics, samples_tag, attributes, metric_names)
    CmdTabs.write_output_data(table_output, options.output_file)

    if options.corrupted != None and len(corrupted_records) > 0:
        CmdTabs.write_output_data(corrupted_records, options.corrupted)

def desaggregate_column_data(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("-s", "--sep_char", dest="sep", default=',',
      help="Character separator when collapse data")

    opts = parser.parse_args(args)
    main_desaggregate_column_data(opts)

def main_desaggregate_column_data(options):
    CmdTabs.transposed = options.transposed
    input_table = CmdTabs.load_input_data(options.input_file)
    desagg_data = CmdTabs.desaggregate_column(input_table, options.col_index, options.sep)
    CmdTabs.write_output_data(desagg_data)

def excel_to_tabular(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Replace substring in a tabular file with the strings listed in a dictionary file')
    add_common_options(parser)
    parser.add_argument("-o", "--output_file", dest="output_file",
      help="Path to output file")
    parser.add_argument("-c", "--columns2extract", dest="columns2extract", default=[0], type=list_based_0,
      help="Column position to extract (1 based). Default 1")
    parser.add_argument("-s", "--sheet_number", dest="sheet_number", default=0, type=based_0,
      help="Sheet number to work with. Default 1")

    opts = parser.parse_args(args)
    main_excel_to_tabular(opts)

def main_excel_to_tabular(options):
    CmdTabs.transposed = options.transposed
    sheet = CmdTabs.get_table_from_excel(options.input_file, options.sheet_number)
    storage = CmdTabs.extract_columns(sheet, options.columns2extract)
    CmdTabs.write_output_data(storage, options.output_file)

def filter_by_list(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    add_common_options(parser)
    parser.add_argument("-f", "--files2befiltered", default= None, type = lambda x: x.split(","), required=True, help="The root to the files that has to be filtered, separated by commas")
    parser.add_argument("-c", "--columns2befiltered", default = None, type = lambda	x: [list(map(lambda y: int(y) -1,r.split(","))) for r in x.split(";")],help="The columns (based 1) that need to be filtered for each file, separated by semicolons, with each set of columns separated by commas")
    parser.add_argument("-t", "--terms2befiltered", default= None, required=True, help="The PATH to the list of terms to be filtered")
    parser.add_argument("--prefix", dest= "prefix", default= "filtered_", help="To select which prefix to add in new filterd files")
    parser.add_argument("-o", "--output_path", default=".", help="The name of the output path")
    parser.add_argument("--metrics", default=False, action="store_true", help= "Getting a table with the proportion of lines removed for each file")
    opts = parser.parse_args(args)
    main_filter_by_list(opts)

def main_filter_by_list(options):
    terms2befiltered = CmdTabs.load_input_data(options.terms2befiltered)
    terms2befiltered = list(map(list, zip(*terms2befiltered )))[0]

    CmdTabs.transposed = options.transposed
    files2befiltered = options.files2befiltered
    columns2befiltered = options.columns2befiltered
    files_columns2befiltered = list(zip(files2befiltered,columns2befiltered))
    loaded_files = CmdTabs.load_several_files(options.files2befiltered)

    output_path = options.output_path

    file_filteredfile = {}
    for file_columns in files_columns2befiltered:
        file = file_columns[0]
        columns = file_columns[1]
        table = loaded_files[file]
        for column in columns:
            table = CmdTabs.filter_by_whitelist(table, terms2befiltered, column)
        file_filteredfile[file] = table


    for file_path, filtered_table in file_filteredfile.items():
        file_name = os.path.basename(file_path)
        CmdTabs.write_output_data(filtered_table, output_path=os.path.join(output_path, options.prefix + file_name))

    if options.metrics:
        for file2befiltered in options.files2befiltered:
            filtered_file = file_filteredfile.get(file2befiltered)
            if filtered_file is None:
                print(f"{file2befiltered}\tNot Filtered")
            else:
                ratio_lines_removed = round(100*(len(file_filteredfile[file2befiltered])/len(loaded_files[file2befiltered])),2)
                print(f"{file2befiltered}\t{ratio_lines_removed}")

def intersect_columns(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("-a", "--a_file", dest="a_file",
      help="Path to input file")
    parser.add_argument("-b", "--b_file", dest="b_file",
      help="Path to input file")
    parser.add_argument("-A", "--a_cols", dest="a_cols", default=[0], type=list_based_0,
      help="Index of columns in base 1 to compare")
    parser.add_argument("-B", "--b_cols", dest="b_cols", default=[0], type=list_based_0,
      help="Index of columns in base 1 to compare")
    parser.add_argument("-s", "--separator", dest="sep", default="\t",
      help="Column character separator")
    parser.add_argument("-c", "--count", dest="count", default=False, action='store_true',
      help="Only compute number of matches")
    parser.add_argument("--full", dest="full", default=False, action='store_true',
      help="Give full record")
    parser.add_argument("-k", "--keep", dest="keep", default='c', choices=['a', 'b', 'c' 'ab'],
      help="Keep records. c for common, 'a' for specific of file a, 'b' for specific of file b and 'ab' for specific of file a AND b")
    
    opts = parser.parse_args(args)
    main_intersect_columns(opts)

def main_intersect_columns(options):
    CmdTabs.transposed = options.transposed

    input_data_a = CmdTabs.load_input_data(options.a_file, options.sep)
    input_data_b = CmdTabs.load_input_data(options.b_file, options.sep)

    a_records, full_a_rec = CmdTabs.load_records(input_data_a, options.a_cols, options.full)
    b_records, full_b_rec = CmdTabs.load_records(input_data_b, options.b_cols, options.full)

    common, a_only, b_only = CmdTabs.get_groups(a_records, b_records)

    if options.count:
      print("a: " + str(len(a_only)))
      print("b: " + str(len(b_only)))
      print("c: " + str(len(common)))
    else:
      # As the groups are list with nested list with only one element: [['str1'], ['str2']..] the full mode need to access to 0 element to be use as key in full_X_rec
      if options.keep == 'c':
        result = common
        if options.full: result = [full_a_rec[r[0]] + full_b_rec[r[0]] for r in common]
      elif options.keep == 'a':
        result = a_only
        if options.full: result = [full_a_rec[r[0]] for r in a_only]
      elif options.keep == 'b':
        result = b_only
        if options.full: result = [full_b_rec[r[0]] for r in b_only]
      elif options.keep == 'ab':
        if options[:full]:
          a_only = [full_a_rec[r[0]] for r in a_only]
          b_only = [full_b_rec[r[0]] for r in b_only]
        result = a_only + b_only
      CmdTabs.write_output_data(result, None, options.sep)

def merge_tabular(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Merge several tabulated files in one single file.')
    add_common_options(parser)
    parser.add_argument("files", metavar='F', nargs='+',
      help="Paths to tabulated files")
    
    opts = parser.parse_args(args)
    main_merge_tabular(opts)

def main_merge_tabular(options):
    CmdTabs.transposed = options.transposed
    files = CmdTabs.load_files(options.files)
    merged = CmdTabs.merge_files(files)
    CmdTabs.write_output_data(merged)

def records_count(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Counting how many times a record is repeated in a column.')
    add_common_options(parser)
    opts = parser.parse_args(args)
    main_records_count(opts)

def main_records_count(options):
    input_table = CmdTabs.load_input_data(options.input_file)
    counts = CmdTabs.records_count(input_table, options.col_index)
    CmdTabs.write_output_data(counts)

def standard_name_replacer(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Replace substring in a tabular file with the strings listed in a dictionary file')
    add_common_options(parser)
    parser.add_argument("-o", "--output_file", dest="output_file",
      help="Path to output file")
    parser.add_argument("-I", "--index_file", dest="index_file",
      help="Path to index file")
    parser.add_argument("-f", "--from", dest="frm", default=0, type=based_0,
      help="Column in index file to take reference value. Default 1. Numeration is 1 based")
    parser.add_argument("-t", "--to", dest="to", default=1, type=based_0,
      help="Column in index file to take the value that will be used in substitution. Default 2. Numeration is 1 based")
    parser.add_argument("-s", "--input_separator", dest="input_separator", default="\t",
      help="Character separator")
    parser.add_argument("-c", "--columns", dest="columns", default=[1], type=list_based_0,
      help="Index of columns in base 1 to compare")
    parser.add_argument("-u", "--remove_untranslated", dest="remove_untranslated", default=False, action='store_true',
      help="Activate this flag for outputting the untranslated entries")
    
    opts = parser.parse_args(args)
    main_standard_name_replacer(opts)

def main_standard_name_replacer(options):
    input_index = CmdTabs.load_input_data(options.index_file)
    translation_index = CmdTabs.index_array(input_index, options.frm, options.to)

    CmdTabs.transposed = options.transposed
    input_table = CmdTabs.load_input_data(options.input_file, options.input_separator)
    tabular_output_translated, _ = CmdTabs.name_replaces(input_table, options.input_separator, options.columns, translation_index, options.remove_untranslated)
    CmdTabs.write_output_data(tabular_output_translated, options.output_file, options.input_separator)

def table_linker(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Merge tabular files.')
    add_common_options(parser)
    parser.add_argument("-o", "--output_file", dest="output_file",
      help="Path to output file")
    parser.add_argument("-l", "--linker_file", dest="linker_file",
      help="Path to file linker")
    parser.add_argument("--drop", dest="drop_line", default=False, action='store_true',
      help="Write the lines whose identifiers have been matched")
    parser.add_argument("-s", "--separator", dest="sep", default="\t",
      help="Character separator when collapse data")
    
    opts = parser.parse_args(args)
    main_table_linker(opts)	

def main_table_linker(options):
    CmdTabs.transposed = options.transposed
    input_linker = CmdTabs.load_input_data(options.linker_file)
    indexed_linker = CmdTabs.index_array(input_linker)
    if CmdTabs.transposed:
      input_table = CmdTabs.load_input_data(options.input_file, "\t")
    else:
      input_table = CmdTabs.load_input_data(options.input_file, "\t", 2)
    linked_table = CmdTabs.link_table(indexed_linker, input_table, options.drop_line, options.sep)
    CmdTabs.write_output_data(linked_table, options.output_file)

def tag_table(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("-t", "--tags", dest="tags",
      help="Strings or files (only first line will be used) sepparated by commas", type=list_str)
    parser.add_argument("-s", "--sep_char", dest="sep", default="\t",
      help="Column character separator")

    opts = parser.parse_args(args)
    main_tag_table(opts)

def main_tag_table(options):
    tags = CmdTabs.load_and_parse_tags(options.tags, options.sep)
    CmdTabs.transposed = options.transposed
    input_table = CmdTabs.load_input_data(options.input_file)
    taged_table = CmdTabs.tag_file(input_table, tags, options.header)
    CmdTabs.write_output_data(taged_table, None, options.sep)
