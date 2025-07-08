from py_cmdtabs.cmdtabs import CmdTabs
import glob, sys, os

## CLASS ATTRIBUTES CONFIGURATION

def set_class_attributes(options):
    opts = vars(options)
    CmdTabs.compressed_input = opts["compressed_in"] if opts.get("compressed_in") else False
    CmdTabs.compressed_output = opts["compressed_out"] if opts.get("compressed_out") else False
    CmdTabs.transposed = opts["transposed"] if opts.get("transposed") else False

## MAIN MODULES
def main_aggregate_column_data(options):
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    agg_data = CmdTabs.aggregate_column(input_table, options.col_index, options.col_aggregate, options.sep, options.agg_mode)
    CmdTabs.write_output_data(agg_data)

def main_column_filter(options):
    table_file = options.input_file
    if table_file == None: table_file = options.table_file # legacy option kept by compatibility
    if table_file == None: sys.exit('Tabulated file not specified') 
    set_class_attributes(options)
    file_names = glob.glob(table_file)
    input_files = CmdTabs.load_several_files(file_names, options.separator)
    filtered_table = CmdTabs.merge_and_filter_tables(input_files, vars(options))
    CmdTabs.write_output_data(filtered_table)

def main_create_metric_table(options):
    set_class_attributes(options)
    metric_file = CmdTabs.load_input_data(options.metric_file)
    attributes = options.attributes.split(',')
    samples_tag = attributes.pop(0)
    metric_names, indexed_metrics = CmdTabs.index_metrics(metric_file, attributes)
    table_output, corrupted_records = CmdTabs.create_table(indexed_metrics, samples_tag, attributes, metric_names)
    CmdTabs.write_output_data(table_output, options.output_file)

    if options.corrupted != None and len(corrupted_records) > 0:
        CmdTabs.write_output_data(corrupted_records, options.corrupted)

def main_desaggregate_column_data(options):
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    desagg_data = CmdTabs.desaggregate_column(input_table, options.col_index, options.sep)
    CmdTabs.write_output_data(desagg_data)

def main_excel_to_tabular(options):
    set_class_attributes(options)
    sheet = CmdTabs.get_table_from_excel(options.input_file, options.sheet_number)
    storage = CmdTabs.extract_columns(sheet, options.columns2extract)
    CmdTabs.write_output_data(storage, options.output_file)

def main_filter_by_list(options):
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

def main_get_columns(options):
    set_class_attributes(options)
    input_data = CmdTabs.load_input_data(options.input_file, options.sep)
    columns = options.columns2extract
    if options.header: 
        cols_header_dict = dict([(col_name, str(idx+1)) for idx, col_name in enumerate(input_data[0])])
        cols_to_get = columns.split(",")
        cols_to_get_processed = []
        try:
          for col in cols_to_get:
              if "%-%" not in col:
                  cols_to_get_processed.append(cols_header_dict[col])
              else:
                  start_col, end_col = col.split("%-%")
                  start_col = cols_header_dict[start_col]
                  end_col = cols_header_dict[end_col]
                  cols_to_get_processed.append(f"{start_col}-{end_col}")
        except KeyError as e:
          raise KeyError(f"Column '{e.args[0]}' not found in header. Available columns: {', '.join(cols_header_dict.keys())}")
        columns = ",".join(cols_to_get_processed)
  
    columns = CmdTabs.parse_column_indices(",", columns)
    output_table = [[row[column] for column in columns] for row in input_data]
    CmdTabs.write_output_data(output_table, options.output_file, options.sep)

def main_intersect_columns(options):
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
        if options.full:
          a_only = [full_a_rec[r[0]] for r in a_only]
          b_only = [full_b_rec[r[0]] for r in b_only]
        result = a_only + b_only
      CmdTabs.write_output_data(result, None, options.sep)

def main_merge_tabular(options):
    set_class_attributes(options)
    files = CmdTabs.load_files(options.files)
    merged = CmdTabs.merge_files(files, options.fill_character)
    CmdTabs.write_output_data(merged)

def main_records_count(options):
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    counts = CmdTabs.records_count(input_table, options.col_index)
    CmdTabs.write_output_data(counts)

def main_standard_name_replacer(options):
    input_index = CmdTabs.load_input_data(options.index_file)
    translation_index = CmdTabs.index_array(input_index, options.frm, options.to)

    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file, options.input_separator)
    tabular_output_translated, _ = CmdTabs.name_replaces(input_table, options.input_separator, options.columns, translation_index, options.remove_untranslated)
    CmdTabs.write_output_data(tabular_output_translated, options.output_file, options.input_separator)

def main_subset_table(options):
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    if options.number_of_files > 0: # split the table in N files with the same number of lines
      file_basename = os.path.basename(options.input_file).split('.')[0]
      os.makedirs(options.output_file, exist_ok=True)
      chunk_size = len(input_table) // options.number_of_files
      if len(input_table) % options.number_of_files > 0:
          chunk_size += 1
      chunk_counter = 0
      header = [input_table[0]] if options.header else []
      init_line = 1 if options.header else 0
      for idx in range(init_line, len(input_table), chunk_size):
          CmdTabs.write_output_data(header+input_table[idx:idx+chunk_size], os.path.join(options.output_file, f"{file_basename}_chunk{chunk_counter}"))
          chunk_counter += 1

    elif options.chunk_size > 0: # split the table in chunks of K lines in different files
      file_basename = os.path.basename(options.input_file).split('.')[0]
      os.makedirs(options.output_file, exist_ok=True)
      chunk_counter = 0
      header = [input_table[0]] if options.header else []
      init_line = 1 if options.header else 0
      for idx in range(init_line, len(input_table), options.chunk_size):
          CmdTabs.write_output_data(header+input_table[idx:idx+options.chunk_size], os.path.join(options.output_file, f"{file_basename}_chunk{chunk_counter}"))
          chunk_counter += 1 

    elif options.chunk_size == 0: # subset the table from start_line to chunk_lines
      subset_table = CmdTabs.subset_table(input_table, options.start_line, options.chunk_lines, options.header)
      CmdTabs.write_output_data(subset_table, options.output_file)


def main_table_linker(options):
    set_class_attributes(options)
    input_linker = CmdTabs.load_input_data(options.linker_file)
    indexed_linker = CmdTabs.index_array(input_linker, options.id_linker, options.columns2linker, options.header)
    if CmdTabs.transposed:
      input_table = CmdTabs.load_input_data(options.input_file, "\t")
    else:
      input_table = CmdTabs.load_input_data(options.input_file, "\t", 2)
    linked_table = CmdTabs.link_table(indexed_linker, input_table, options.drop_line, options.sep, options.header)
    CmdTabs.write_output_data(linked_table, options.output_file)

def main_table_splitter(options):
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    file_basename = os.path.basename(options.input_file).split('.')[0]
    os.makedirs(options.output_folder, exist_ok=True)
    lines_to_write = []
    chunk_counter = 0
    for idx, row in enumerate(input_table):
        lines_to_write.append(row)
        if (idx+1) % options.chunk_size == 0:
          CmdTabs.write_output_data(lines_to_write, os.path.join(options.output_folder, f"{file_basename}_chunk{chunk_counter}"))
          lines_to_write = []
          chunk_counter += 1
    if len(lines_to_write) > 0:
        CmdTabs.write_output_data(lines_to_write, os.path.join(options.output_folder, f"{file_basename}_chunk{chunk_counter}"))

def main_tag_table(options):
    tags = CmdTabs.load_and_parse_tags(options.tags, options.sep)
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file)
    taged_table = CmdTabs.tag_file(input_table, tags, options.header)
    CmdTabs.write_output_data(taged_table, None, options.sep)

def main_transform_to_latex(options):
    set_class_attributes(options)
    input_table = CmdTabs.load_input_data(options.input_file, sep=options.separator)
    table_name = os.path.basename(options.input_file).split('.')[0] if options.input_file != '-' else 'tableX'
    latex_table = CmdTabs.transform_to_latex(input_table, options.header, options.whole, table_name)
    CmdTabs.write_output_data(latex_table, options.output_file, sep="")

def main_transpose_table(options):
    set_class_attributes(options)
    transposed_table = CmdTabs.transpose(CmdTabs.load_input_data(options.input_file))
    CmdTabs.write_output_data(transposed_table, options.output_file)