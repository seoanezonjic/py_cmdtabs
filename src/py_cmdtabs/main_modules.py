
import glob, sys, os
from warnings import warn
from py_cmdtabs.cmdtabs import CmdTabs

## CLASS ATTRIBUTES CONFIGURATION

def set_class_attributes(options):
    opts = vars(options)
    CmdTabs.compressed_input = opts["compressed_in"] if opts.get("compressed_in") else False
    CmdTabs.compressed_output = opts["compressed_out"] if opts.get("compressed_out") else False
    CmdTabs.transposed = opts["transposed"] if opts.get("transposed") else False

################################################
## MAIN MODULES
################################################

# ADDED TO CMDTABS FUNCTION AND DEPRECATED
# ------------------------------------------------------------
def main_tag_table(options): # Added to main_cmdtabs
    warn('This is deprecated. Use: cmdtabs --tags tables/tracker -i path_to/tag_file')

    tags = CmdTabs.load_and_parse_tags(options.tags, options.sep)
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    taged_table = CmdTabs.tag_file(input_table, tags, options.header)
    CmdTabs.write_output_data(taged_table, None, options.sep)

def main_transform_to_latex(options): # Added to main cmdtabs
    warn('This is deprecated. Use: cmdtabs --latex -i input_table --whole')

    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file, sep=options.separator)
    table_name = os.path.basename(options.input_file).split('.')[0] if options.input_file != '-' else 'tableX'
    latex_table = CmdTabs.transform_to_latex(input_table, options.header, options.whole, table_name)
    CmdTabs.write_output_data(latex_table, options.output_file, sep="")

def main_transpose_table(options): # Added to main cmdtabs
    warn('This is deprecated. Use: cmdtabs --transposed input_table')

    set_class_attributes(options)
    transposed_table = CmdTabs.transpose(CmdTabs.load_input_data(options.input_file))
    CmdTabs.write_output_data(transposed_table, options.output_file)

def main_standard_name_replacer(options): # Added to main cmdtabs
    warn('This is deprecated. Use: cmdtabs -I dictionary_index -c 1 --from 1 --to 2 -u -i input_table')

    input_index = CmdTabs.load_input_data(options.index_file)
    translation_index = CmdTabs.index_array(input_index, options.frm, options.to)

    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file, options.input_separator)
    tabular_output_translated, _ = CmdTabs.name_replaces(input_table, options.input_separator, options.columns, translation_index, options.remove_untranslated)
    CmdTabs.write_output_data(tabular_output_translated, options.output_file, options.input_separator)

def main_aggregate_column_data(options): # Added to main cmdtabs
    warn('This is deprecated. Use: cmdtabs --aggregate -i input_table --agg_ref_col_index 1,2 --agg_col 3,4')

    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    agg_data = CmdTabs.aggregate_column(input_table, options.col_index, options.col_aggregate, options.sep, options.agg_mode)
    CmdTabs.write_output_data(agg_data)

def main_desaggregate_column_data(options): # Added to main cmdtabs
    warn('This is deprecated. Use: cmdtabs --desaggregate -i input_table --desagg_col 3,4 --desagg_sep ","')

    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    desagg_data = CmdTabs.desaggregate_column(input_table, options.col_index, options.sep)
    CmdTabs.write_output_data(desagg_data)

def main_records_count(options): # Added to main cmdtabs
    warn('This is deprecated. Use: cmdtabs -i input_table --count-cols 2')

    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    counts = CmdTabs.records_count(input_table, options.col_index)
    CmdTabs.write_output_data(counts)

def main_excel_to_tabular(options): # Added to main_cmdtabs
    warn('This is deprecated. Use: cmdtabs -i input_table --file_type excel --excel_cols 1,2,3 --excel_sheet_number 1')

    set_class_attributes(options)
    sheet = CmdTabs.get_table_from_excel(options.input_file, options.sheet_number)
    storage = CmdTabs.extract_columns(sheet, options.columns2extract)
    storage = CmdTabs.extract_rows(storage, options.rows2extract)
    CmdTabs.write_output_data(storage, options.output_file)

def main_create_metric_table(options):
    warn('This is deprecated. Use: cmdtabs -i input_table --sample_attributes sample_attr-comma-separated')

    set_class_attributes(options)
    metric_file = CmdTabs.load_input_data(options.metric_file)
    samples_tag = options.attributes.pop(0)
    metric_names, indexed_metrics = CmdTabs.index_metrics(metric_file, options.attributes)
    table_output, corrupt_recs = CmdTabs.create_table(indexed_metrics, samples_tag, options.attributes, metric_names)
    CmdTabs.write_output_data(table_output, options.output_file)

    if options.corrupted != None and len(corrupt_recs) > 0: CmdTabs.write_output_data(corrupt_recs, options.corrupted)

def main_subset_table(options):
    warn('This is deprecated. Use:')
    warn('  cmdtabs -i input_table --offset 3,4 -H')
    warn('  cmdtabs -i input_table --split_out --sp_chunk_size 4 -o FOLDER/FILE_NAME')
    warn('  cmdtabs -i input_table --split_out --sp_file_number 2 -o FOLDER/FILE_NAME')

    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    if options.chunk_size == 0 and options.number_of_files == 0: # subset the table from start_line to chunk_lines
      subset_table = CmdTabs.subset_table(input_table, options.start_line, options.chunk_lines, options.header)
      CmdTabs.write_output_data(subset_table, options.output_file)
    else:
      os.makedirs(options.output_file, exist_ok=True)
      file_name = os.path.basename(options.input_file).split('.')[0]
      header = [input_table[0]] if options.header else []
      if options.number_of_files > 0: # split the table in N files with the same number of lines
        CmdTabs.split_by_nFiles(input_table, options.number_of_files, options.output_file, file_name, header = header)
      elif options.chunk_size > 0: # split the table in chunks of K lines in different files
        CmdTabs.split_by_chunk(input_table, options.chunk_size, options.output_file, file_name, header = header)

def main_get_columns(options):
    warn('This is deprecated. Use:')
    warn('  cmdtabs -i input_table --extract_cols 1,3-5')
    warn('  cmdtabs -i input_table -H --extract_cols col-1,col-3%-%col-5')

    set_class_attributes(options)
    input_data = CmdTabs.load_input_data(options.input_file, options.sep)
    columns = CmdTabs.parse_column_indices(options.columns2extract.split(","), has_header=options.header, table=input_data)
    output_table = CmdTabs.filter_columns(input_data, columns)
    CmdTabs.write_output_data(output_table, options.output_file, options.sep)

def main_column_filter(options):
    warn('This is deprecated. Use:')
    warn('  cmdtabs -i input_table --extract_cols 1,2 --ext_col_match 1 --ext_keywords KEYWORD --ext_search_mode c --ext_match_mode c')
    table_file = options.input_file
    if table_file == None: table_file = options.table_file # legacy option kept by compatibility
    if table_file == None: sys.exit('Tabulated file not specified') 
    set_class_attributes(options)
    file_names = glob.glob(table_file)
    input_files = CmdTabs.load_several_files(file_names, options.separator)
    # TODO: Add to cmdtabs script iterate several files add header for the following method
    filtered_table = CmdTabs.merge_and_filter_tables(input_files, vars(options))
    CmdTabs.write_output_data(filtered_table)

def main_filter_by_list(options):
    warn('This is deprecated. Use: cmdtabs -i input_table --ext_col_match 1 --ext_keyword_file table_with_keywords --ext_stats --ext_reverse')

    terms2befiltered = CmdTabs.load_input_data(options.terms2befiltered)
    terms2befiltered = list(map(list, zip(*terms2befiltered )))[0]

    set_class_attributes(options)
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
            if options.blacklist:
              table = CmdTabs.filter_by_blacklist(table, terms2befiltered, column, options.not_exact_match)
            else:
              table = CmdTabs.filter_by_whitelist(table, terms2befiltered, column, options.not_exact_match)
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

def main_table_linker(options):
    warn('This is deprecated. Use: cmdtabs_merge --tables input_table1,input_table2 --columns2add 1,2')

    set_class_attributes(options)
    input_linker = CmdTabs.load_input_data(options.linker_file, sep=options.sep)
    indexed_linker = CmdTabs.index_array(input_linker, options.id_linker, options.columns2linker, options.header)
    if CmdTabs.transposed:
      input_table = CmdTabs.load_input_data(options.input_file, options.sep)
    else:
      input_table = CmdTabs.load_input_data(options.input_file, options.sep, 2)
    linked_table = CmdTabs.link_table(indexed_linker, input_table, options.drop_line, options.sep, options.header)
    CmdTabs.write_output_data(linked_table, options.output_file, sep=options.sep)

def main_merge_tabular(options):
    warn("This is deprecated. Use: cmdtabs_merge --tables input_table1,input_table2,input_table3 --columns2add '1,2,3;1,2' --union --fill_character 'NA'")
    
    set_class_attributes(options)
    files = CmdTabs.load_files(options.files, fill_character = options.fill_character)
    merged = CmdTabs.merge_files(files, fill_character=options.fill_character)
    CmdTabs.write_output_data(merged)

def main_intersect_columns(options):
    warn('This is deprecated. Use: cmdtabs_merge -a table_a -b table_b -A 1 -B 1 -s "\\t" --keep ab --full ')


    set_class_attributes(options)

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
      result = CmdTabs.get_subset(common, a_only, b_only, full_a_rec, full_b_rec, keep_subset=options.keep, full=options.full)
      CmdTabs.write_output_data(result, None, options.sep)

########################################################
## Unifiying script CMDTABS
########################################################

def main_cmdtabs(opts):
  output_sep = "\t"
  CmdTabs.compressed_input = opts.compressed_in
  if opts.file_type == 'excel': #[excel2table]
    sheet = CmdTabs.get_table_from_excel(opts.input_file, opts.excSheet_number)
    table = CmdTabs.extract_columns(sheet, opts.excColumns2extract)
    table = CmdTabs.extract_rows(table, opts.excRows2extract)
  else:
    table = CmdTabs.load_input_data(opts.input_file, sep=opts.separator)

  if len(opts.offset) > 0: table = CmdTabs.subset_table(table, int(opts.offset[0]) - 1, int(opts.offset[1]), opts.header) # [subset] subset file
  
  if len(opts.extract_cols) > 0 or opts.ext_keyword_file != None: # [get_columns] [column_filter]
    n_rows  = len(table)
    cols = CmdTabs.parse_column_indices(opts.extract_cols, has_header = opts.header, table=table) #[get_columns]
    if opts.ext_keyword_file != None:# [filter_by_list]
      keywords = [ row[0] for row in CmdTabs.load_input_data(opts.ext_keyword_file) ] # Flatten nested list to simple list
    else:
      keywords = opts.ext_keywords
    table = CmdTabs.filter_columns(table, cols, opts.ext_col_match, keywords, opts.ext_search_mode, opts.ext_match_mode, opts.ext_reverse) #[column_filter]
    if opts.ext_stats: print(round(100*(len(table)/n_rows),2)) # [filter_by_list]

  if opts.transposed: table = CmdTabs.transpose(table) # TRANSFORMATION [transpose_table]
  # STATS
  if opts.count_cols != None: table = CmdTabs.records_count(table, opts.count_cols) # [records_count]
  # TRANSFORMATIONS
  if len(opts.sample_attributes) > 0: #[create_metric_table]
    samples_tag = opts.sample_attributes.pop(0)
    metric_names, indexed_metrics = CmdTabs.index_metrics(table, opts.sample_attributes)
    table, corrupt_recs = CmdTabs.create_table(indexed_metrics, samples_tag, opts.sample_attributes, metric_names)
    if opts.corrupted != None and len(corrupt_recs) > 0: CmdTabs.write_output_data(corrupt_recs, opts.corrupted)

  if opts.aggregate: table = CmdTabs.aggregate_column(table, opts.agg_col_index, opts.col_aggregate, opts.agg_sep, opts.agg_mode) # [aggregate_table]

  if opts.desaggregate: table = CmdTabs.desaggregate_column(table, opts.desagg_col, opts.desagg_sep) # [desaggregate_table]

  if len(opts.tags) > 0: # [tag_table]
    tags = CmdTabs.load_and_parse_tags(opts.tags, opts.separator) # Warining the following 2 lines must not be within set_class_attributes
    table = CmdTabs.tag_file(table, tags, opts.header)
  
  if opts.index_file != None: # [standard_name_replacer]
    input_index = CmdTabs.load_input_data(opts.index_file)
    translation_index = CmdTabs.index_array(input_index, opts.frm, opts.to)
    table, _ = CmdTabs.name_replaces(table, opts.separator, opts.columns, translation_index, opts.remove_untranslated)
  
  if opts.uniq: table = CmdTabs.get_uniq(table)

  if opts.to_latex: # [transform_to_latex]
    table_name = os.path.basename(opts.input_file).split('.')[0] if opts.input_file != '-' else 'tableX'
    table = CmdTabs.transform_to_latex(table, opts.header, opts.whole, table_name)
    output_sep = ""
  
  ## OUTPUT
  CmdTabs.compressed_output = opts.compressed_out
  if opts.split_out: # [subset]
    os.makedirs(opts.output_file, exist_ok=True)
    file_name = os.path.basename(opts.input_file).split('.')[0]
    header = [table[0]] if opts.header else []
    if opts.sp_chunk_size > 0: # [subset] split by chunk size
      CmdTabs.split_by_chunk(table, opts.sp_chunk_size, opts.output_file, file_name, header = header)
    elif opts.sp_file_number > 0: # [subset] split by file number
      CmdTabs.split_by_nFiles(table, opts.sp_file_number, opts.output_file, file_name, header = header)
  else:
    CmdTabs.write_output_data(table, opts.output_file, sep=output_sep)
  

########################################################
## cmdtabs script for table merging
########################################################

def main_cmdtabs_merge(opts):
  output_sep = "\t"
  CmdTabs.compressed_input = opts.compressed_in
  table = None  
  if opts.a_file != None and opts.b_file != None:
    input_data_a = CmdTabs.load_input_data(opts.a_file, sep=opts.separator, fill_character=opts.fill_character)
    input_data_b = CmdTabs.load_input_data(opts.b_file, sep=opts.separator, fill_character=opts.fill_character)
    a_records, full_a_rec = CmdTabs.load_records(input_data_a, opts.a_cols, opts.full)
    b_records, full_b_rec = CmdTabs.load_records(input_data_b, opts.b_cols, opts.full)
    common, a_only, b_only = CmdTabs.get_groups(a_records, b_records)
    if opts.count:
      print("a: " + str(len(a_only)))
      print("b: " + str(len(b_only)))
      print("c: " + str(len(common)))
      exit()
    else:
      table = CmdTabs.get_subset(common, a_only, b_only, full_a_rec, full_b_rec, keep_subset=opts.keep, full=opts.full)
  elif opts.tables != None :
    main_table = opts.tables.pop(0)
    table = CmdTabs.load_input_data(main_table, sep=opts.separator) # [table_linker]
    columns2add = [[cols.pop(0), cols] for cols in opts.columns2add]
    CmdTabs.merge_tables2mainTab(table, opts.tables, columns2add, sep = opts.separator, 
                              fill_character= opts.fill_character, header = opts.header, union=opts.union) # [table_linker]
  CmdTabs.compressed_output = opts.compressed_out
  CmdTabs.write_output_data(table, opts.output_file, sep=output_sep)
  