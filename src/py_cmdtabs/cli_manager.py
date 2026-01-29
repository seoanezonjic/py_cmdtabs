import argparse, sys, os, codecs
from py_cmdtabs.main_modules import *

## TYPES
def based_0(string): return int(string) - 1
def list_based_0(string): 
    from py_cmdtabs.cmdtabs import CmdTabs
    return CmdTabs.parse_column_indices(string.split(','))
def list_str(values): return values.split(',')
def unescaped_str(arg_str): return codecs.decode(str(arg_str), 'unicode_escape') 
def nested_int_list(arg_str): return [ [int(col) - 1 for col in str_cols.split(',')] for str_cols in  arg_str.split(';')]

## Common options
def add_common_options(parser, flags_to_skip = [], help_replacer={}):
    helps_dict = {
        "--input_file": "Path to input file",
        "--transposed": "To perform the operations in rows and not columns",
        "--compressed_in": "To indicate that the input file is compressed",
        "--compressed_out": "To indicate that the output file will be compressed"
        }
    helps_dict.update(help_replacer)

    if "-i" not in flags_to_skip and "--input_file" not in flags_to_skip:
      parser.add_argument("-i", "--input_file", dest="input_file", help=helps_dict["--input_file"])
    if "--transposed" not in flags_to_skip:
      parser.add_argument("--transposed", default=False, action="store_true", help=helps_dict["--transposed"])
    if "--compressed_in" not in flags_to_skip:
      parser.add_argument("--compressed_in", default=False, action="store_true", help=helps_dict["--compressed_in"])
    if "--compressed_out" not in flags_to_skip:
      parser.add_argument("--compressed_out", default=False, action="store_true", help=helps_dict["--compressed_out"])

##############################################

def aggregate_column_data(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("-x", "--column_index", dest="col_index",
	    help="Column index (1 based) to use as reference", type=list_based_0)
    parser.add_argument("-s", "--separator", dest="sep", default=",",
      help="Character separator when collapse data")
    parser.add_argument("-a", "--column_aggregate", dest="col_aggregate",
      help="Column(s) index (1 based) to extract data and join for each id in column index (if more than one, comma separated)", type=list_based_0)
    parser.add_argument("-A", "--aggregation_mode", dest="agg_mode", default="concatenate",
      help="Mode to perform aggregation. Current available: max,min,mean,median,sum,std,var,IQR,PC25,PC75,count & concatenate. Default (concatenate) is string concatenation by defined separator. More than one aggregation mode can be used separated by commas")    
    opts =  parser.parse_args(args)
    main_aggregate_column_data(opts)

def column_filter(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Get records from table an extract desired columns.')
    add_common_options(parser)
    parser.add_argument("-t", "--table_file", dest="table_file",
      help="Input tabulated file. LGACY PARAMETER TO BE DEPRECATED. Use -i instead")
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
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
  	  help="Indicate if files have header")
        
    opts = parser.parse_args(args)
    main_column_filter(opts)

def create_metric_table(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser, flags_to_skip=["--input_file"])
    parser.add_argument("metric_file", metavar='M',
      help="File with tabulated metrics")
    parser.add_argument("attributes", metavar='A', type=list_str,
      help="String with comma separated attributes")
    parser.add_argument("output_file", metavar='O',
      help="Output file path")
    parser.add_argument("-c", "--corrupted", dest="corrupted",
      help="File where corrupted metrics are stored")
    
    opts = parser.parse_args(args)
    main_create_metric_table(opts)

def desaggregate_column_data(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("-x", "--column_index", dest="col_index",
  	  help="Column index (1 based) to use as reference", type=list_based_0)
    parser.add_argument("-s", "--sep_char", dest="sep", default=',',
      help="Character separator when collapse data")

    opts = parser.parse_args(args)
    main_desaggregate_column_data(opts)

def excel_to_tabular(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Replace substring in a tabular file with the strings listed in a dictionary file')
    add_common_options(parser, flags_to_skip=["--compressed_in"], help_replacer={"--input_file": "Input xlsx file"})
    parser.add_argument("-o", "--output_file", dest="output_file",
      help="Path to output file")
    parser.add_argument("-c", "--columns2extract", dest="columns2extract", default=[0], type=list_based_0,
      help="Column position to extract (1 based). Default 1. Use 0 to extract all columns")
    parser.add_argument("-r", "--rows2extract", dest="rows2extract", default=[], type=list_based_0,
      help="Row positions to extract (1 based). Default 0, which means all rows will be extracted")  
    parser.add_argument("-s", "--sheet_number", dest="sheet_number", default=0, type=based_0,
      help="Sheet number to work with. Default 1")

    opts = parser.parse_args(args)
    main_excel_to_tabular(opts)

def filter_by_list(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    add_common_options(parser, flags_to_skip=["--input_file"])
    parser.add_argument("-f", "--files2befiltered", default= None, type = lambda x: x.split(","), required=True, help="The root to the files that has to be filtered, separated by commas")
    parser.add_argument("-c", "--columns2befiltered", default = None, type = lambda	x: [list(map(lambda y: int(y) -1,r.split(","))) for r in x.split(";")],help="The columns (based 1) that need to be filtered for each file, separated by semicolons, with each set of columns separated by commas")
    parser.add_argument("-t", "--terms2befiltered", default= None, required=True, help="The PATH to the list of terms to be filtered")
    parser.add_argument("--prefix", dest= "prefix", default= "filtered_", help="To select which prefix to add in new filterd files")
    parser.add_argument("-o", "--output_path", default=".", help="The name of the output path")
    parser.add_argument("--metrics", default=False, action="store_true", help= "Getting a table with the proportion of lines removed for each file")
    parser.add_argument("--blacklist", default=False, action="store_true", help="To select the blacklist mode instead of whitelist. Default is False (whitelist case)")
    parser.add_argument("--not_exact_match", default=False, action="store_true", help="To select the partial match mode instead of full match mode. Default is False (exact match case)")
    opts = parser.parse_args(args)
    main_filter_by_list(opts)

def get_columns(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Extract desired columns from a table.')
    add_common_options(parser)
    parser.add_argument("-s", "--separator", dest="sep", default="\t", type=unescaped_str,
      help="Column character separator")    
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
      help="Indicate if files have header")
    parser.add_argument("-o", "--output_file", dest="output_file",
      help="Path to output file")
    parser.add_argument("-c", "--columns2extract", dest="columns2extract", default="1",
      help="Comma separated values of columns positions to extract (1 based) or column names if header is present. Default 1")
    opts = parser.parse_args(args)
    main_get_columns(opts)

def intersect_columns(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser, flags_to_skip=["--input_file"])
    parser.add_argument("-a", "--a_file", dest="a_file",
      help="Path to input file")
    parser.add_argument("-b", "--b_file", dest="b_file",
      help="Path to input file")
    parser.add_argument("-A", "--a_cols", dest="a_cols", default=[0], type=list_based_0,
      help="Index of columns in base 1 to compare")
    parser.add_argument("-B", "--b_cols", dest="b_cols", default=[0], type=list_based_0,
      help="Index of columns in base 1 to compare")
    parser.add_argument("-s", "--separator", dest="sep", default="\t", type=unescaped_str,
      help="Column character separator")
    parser.add_argument("-c", "--count", dest="count", default=False, action='store_true',
      help="Only compute number of matches")
    parser.add_argument("--full", dest="full", default=False, action='store_true',
      help="Give full record")
    parser.add_argument("-k", "--keep", dest="keep", default='c', choices=['a', 'b', 'c', 'ab'],
      help="Keep records. c for common, 'a' for specific of file a, 'b' for specific of file b and 'ab' for specific of file a AND b")
    
    opts = parser.parse_args(args)
    main_intersect_columns(opts)

def merge_tabular(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Merge several tabulated files in one single file.')
    add_common_options(parser, flags_to_skip=["--input_file"])
    parser.add_argument("-f", "--fill_character", dest="fill_character", default="-",
      help="Character to fill when a field is empty")
    parser.add_argument("files", metavar='F', nargs='+',
      help="Paths to tabulated files")
    
    opts = parser.parse_args(args)
    main_merge_tabular(opts)

def records_count(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Counting how many times a record is repeated in a column.')
    add_common_options(parser)
    parser.add_argument("-x", "--column_index", dest="col_index",
	    help="Column index (1 based) to count elements", type=list_based_0)
    opts = parser.parse_args(args)
    main_records_count(opts)

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
    parser.add_argument("-c", "--columns", dest="columns", default=[0], type=list_based_0,
      help="Index of columns in base 1 to compare")
    parser.add_argument("-u", "--remove_untranslated", dest="remove_untranslated", default=False, action='store_true',
      help="Activate this flag for outputting the untranslated entries")
    
    opts = parser.parse_args(args)
    main_standard_name_replacer(opts)

def subset_table(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=f'Usage: {os.path.basename(__file__)} [options]')
    add_common_options(parser)
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
  	                   help="Indicate if files have header")
    parser.add_argument("-s", "--start_line", dest="start_line", default= 0, type= based_0,
                        help="Set the first line of subset. 0 based index")
    parser.add_argument("-l", "--lines_to_subset", dest="chunk_lines", default= 5, type= int,
                        help="Set the number of lines to extract from --start_line")
    parser.add_argument("-o", "--output_file", dest="output_file", default=None, 
                        help="Path to output file (or the folder where the chunks will be stored if --chunk_size is set)")
    parser.add_argument("-k", "--chunk_size", dest="chunk_size", default= 0, type=int,
                        help="Use it instead of start_line and lines_to_subset if you want to split the table in chunks on K lines in different files.")
    parser.add_argument("-n", "--number_of_files", dest="number_of_files", default= 0, type=int,
                        help="Use it instead of start_line and lines_to_subset if you want to split the table in N files with the same number of lines.")          
    opts = parser.parse_args(args)
    main_subset_table(opts)

def table_linker(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Merge tabular files.')
    add_common_options(parser)
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
	    help="Indicate if input file has a header line. Header will not be printed in output")
    parser.add_argument("-o", "--output_file", dest="output_file",
      help="Path to output file")
    parser.add_argument("-l", "--linker_file", dest="linker_file",
      help="Path to file linker")
    parser.add_argument("--columns2linker", dest="columns2linker", default=[1], type=list_based_0)
    parser.add_argument("--id_linker", dest="id_linker", default=0, type=based_0)
    parser.add_argument("--drop", dest="drop_line", default=False, action='store_true',
      help="Write the lines whose identifiers have been matched")
    parser.add_argument("-s", "--separator", dest="sep", default="\t",
      help="Character separator when collapse data")
    
    opts = parser.parse_args(args)
    main_table_linker(opts)	

def tag_table(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Collapse table rows aggregatting one field in the table.')
    add_common_options(parser)
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
	    help="Indicate if input file has a header line. Header will not be printed in output")
    parser.add_argument("-t", "--tags", dest="tags",
      help="Strings or files (only first line will be used) sepparated by commas", type=list_str)
    parser.add_argument("-s", "--sep_char", dest="sep", default="\t",
      help="Column character separator")

    opts = parser.parse_args(args)
    main_tag_table(opts)

def transform_to_latex(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=f'Usage: {os.path.basename(__file__)} [options]')
    add_common_options(parser)
    parser.add_argument("-s", "--separator", dest="separator", default="\t", type=unescaped_str,
                        help="Input table column character separator")
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
                     	  help="Indicate if files have header")
    parser.add_argument("-o", "--output_file", dest="output_file", default=None, 
                        help="Path to output file")
    parser.add_argument("-w", "--whole", dest="whole", default=False, action='store_true',
                        help="Indicate if you want the whole table and tabular environment to be returned with the table transformed")
    opts = parser.parse_args(args)
    main_transform_to_latex(opts)

def transpose_table(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=f'Usage: {os.path.basename(__file__)} [options]')
    add_common_options(parser)
    parser.add_argument("-o", "--output_file", dest="output_file", default=None, 
                        help="Path to output file")
    opts = parser.parse_args(args)
    main_transpose_table(opts)

def cmdtabs(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=f'Usage: {os.path.basename(__file__)} [options]')
    add_common_options(parser)
    parser.add_argument("-c", "--columns", dest="columns", default=[0], type=list_based_0,
                        help="Index of columns in base 1 to compare")
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
                     	  help="Indicate if files have header")
    parser.add_argument("-I", "--index_file", dest="index_file", default=None,
                        help="Path to index file")
    parser.add_argument("-o", "--output_file", dest="output_file", default=None, 
                        help="Path to output file")
    parser.add_argument("-s", "--separator", dest="separator", default="\t", type=unescaped_str,
                        help="Input table column character separator")
    parser.add_argument("-t", "--tags", dest="tags", default= [],
                        help="Strings or files (only first line will be used) sepparated by commas", type=list_str)
    parser.add_argument("-u", "--remove_untranslated", dest="remove_untranslated", default=False, action='store_true',
                        help="Activate this flag for outputting the untranslated entries")
    parser.add_argument("-w", "--whole", dest="whole", default=False, action='store_true',
                        help="Indicate if you want the whole table and tabular environment to be returned with the table transformed")

    parser.add_argument("--aggregate", dest="aggregate", default=False, action='store_true',
                        help="Aggregate table columns")
    parser.add_argument("--agg_ref_col_index", dest="agg_col_index",
                  	    help="Column index (1 based) to use as reference", type=list_based_0)
    parser.add_argument("--agg_col", dest="col_aggregate",
                        help="Column(s) index (1 based) to extract data and join for each id in column index (if more than one, comma separated)", type=list_based_0)
    parser.add_argument("--agg_mode", dest="agg_mode", default="concatenate",
                        help="Mode to perform aggregation. Current available: max,min,mean,median,sum,std,var,IQR,PC25,PC75,count & concatenate. Default (concatenate) is string concatenation by defined separator. More than one aggregation mode can be used separated by commas")
    parser.add_argument("--agg_sep", dest="agg_sep", default=",",
                        help="Character separator when collapse data")
    parser.add_argument("--count-cols", dest="count_cols", default=None, type=list_based_0,
                        help="Index of columns in base 1 to count")
    parser.add_argument("--desaggregate", dest="desaggregate", default=False, action='store_true',
                        help="Desaggregate table columns")
    parser.add_argument("--desagg_col", dest="desagg_col",
  	                    help="Column index (1 based) to use as reference", type=list_based_0)
    parser.add_argument("--desagg_sep", dest="desagg_sep", default=",",
                        help="Character separator when to split string column")
    parser.add_argument("--excel_cols", dest="excColumns2extract", default=[0], type=list_based_0,
                        help="Column position to extract (1 based). Default 1. Use 0 to extract all columns")
    parser.add_argument("--excel_rows", dest="excRows2extract", default=[], type=list_based_0,
                        help="Row positions to extract (1 based). Default 0, which means all rows will be extracted")  
    parser.add_argument("--excel_sheet_number", dest="excSheet_number", default=0, type=based_0,
                        help="Sheet number to work with. Default 1")
    parser.add_argument("--file_type", dest="file_type", default='text',
                        help="Default text. Other options;excel")
    parser.add_argument("--from", dest="frm", default=0, type=based_0,
                        help="Column in index file to take reference value. Default 1. Numeration is 1 based")
    parser.add_argument("--to", dest="to", default=1, type=based_0,
                        help="Column in index file to take the value that will be used in substitution. Default 2. Numeration is 1 based")
    parser.add_argument("--latex", dest="to_latex", default=False, action='store_true',
                        help="Write table in latex code")
    parser.add_argument("--sample_attributes", dest="sample_attributes", default=[], type=list_str,
                        help="Define sample atributtes (comma separated list) to colapse a long table in a wide metric table")
    parser.add_argument("--corrupted", dest="corrupted",
                        help="File where corrupted metrics are stored")
    parser.add_argument("--offset", dest="offset", default=[], type=list_str,
                        help="To subset N rows from table. Indicate as 'start_row,number_row' where start_row es the line to begin the extraction (1 based) and number_row is the amount of lines to extract")
    parser.add_argument("--split_out", dest="split_out", default=False, action='store_true',
                        help="Split output table in several files")
    parser.add_argument("--sp_chunk_size", dest="sp_chunk_size", default= 0, type=int,
                        help="To split the ouput table in chunks on K lines in different files.")
    parser.add_argument("--sp_file_number", dest="sp_file_number", default= 0, type=int,
                        help="To split the output table in N files with the same number of lines.")
    parser.add_argument("--extract_cols", dest="extract_cols", default=[], type=list_str,
                        help="Columns to extract from table, comma separated (based 1)")
    parser.add_argument("--ext_col_match", dest="ext_col_match", type=list_based_0,
                        help="Select columns where search keywords. Format: x,y,z..")
    parser.add_argument("--ext_keywords", dest="ext_keywords",
                        help="Keywords for select rows. Format: key1_col1&key2_col1%%key1_col2&key2_col2")
    parser.add_argument("--ext_keyword_file", dest="ext_keyword_file",
                        help="File with one keyword per line. They will be used to search in all the specified columns in --ext_col_match")
    parser.add_argument("--ext_search_mode", dest="ext_search_mode", default='c', choices=['c', 's'],
                        help="c for match in every columns set, s some match in some column. Default c")
    parser.add_argument("--ext_match_mode", dest="ext_match_mode", default='i', choices=['i', 'c'],
                        help="i string must include the keyword, c for fullmatch. Default i")
    parser.add_argument("--ext_reverse", dest="ext_reverse", default=False, action='store_true',
                        help="Select not matching")
    parser.add_argument("--ext_stats", dest="ext_stats", default=False, action='store_true',
                        help="Print row extraction statistics")                        
    parser.add_argument("--uniq", dest="uniq", default=False, action='store_true',
                        help="Make rows unique")
    opts = parser.parse_args(args)
    main_cmdtabs(opts)


def cmdtabs_merge(args=None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=f'Usage: {os.path.basename(__file__)} [options]')
    add_common_options(parser)
    parser.add_argument("-H", "--header", dest="header", default=False, action='store_true',
                     	  help="Indicate if files have header")
    parser.add_argument("-o", "--output_file", dest="output_file", default=None, 
                        help="Path to output file")
    parser.add_argument("-s", "--separator", dest="separator", default="\t", type=unescaped_str,
                        help="Input table column character separator")
    parser.add_argument("-a", "--a_file", dest="a_file",
                        help="Path to input file")
    parser.add_argument("-b", "--b_file", dest="b_file",
                        help="Path to input file")
    parser.add_argument("-A", "--a_cols", dest="a_cols", default=[0], type=list_based_0,
                        help="Index of columns in base 1 to compare")
    parser.add_argument("-B", "--b_cols", dest="b_cols", default=[0], type=list_based_0,
                        help="Index of columns in base 1 to compare")
    parser.add_argument("-c", "--count", dest="count", default=False, action='store_true',
                        help="Only compute number of matches")
    parser.add_argument("--full", dest="full", default=False, action='store_true',
                        help="Give full record")
    parser.add_argument("-k", "--keep", dest="keep", default='c', choices=['a', 'b', 'c', 'ab'],
                        help="Keep records. c for common, 'a' for specific of file a, 'b' for specific of file b and 'ab' for specific of file a AND b")

    parser.add_argument("--tables", dest="tables", default=None, type=list_str,
                        help="Path to tables, comma separated. Paths could include wildcards")
    parser.add_argument("--fill_character", dest="fill_character", default="-",
                        help="Character to fill when a field is empty")
    parser.add_argument("--columns2add", dest="columns2add", default=[], type=nested_int_list,
                        help="For each file to add to the first file, column indexes 1 based comma separated. To separate each column set, use semicolon ;")
    parser.add_argument("--union", dest="union", default=False, action='store_true',
                     	  help="If a row in a file has not match in the merging table is added to it")
    opts = parser.parse_args(args)
    main_cmdtabs_merge(opts)

                      