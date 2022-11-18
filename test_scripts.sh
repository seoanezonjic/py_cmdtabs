#!/usr/bin/env bash

source ~soft_bio_267/initializes/init_ruby
export PATH=`pwd`/bin:$PATH
test_data=test/data_tests/
out=output_test_scripts 
data_to_test=data_test_scripts
mkdir $out

#aggregate_column_data --------------------------------------------------------------------------
aggregate_column_data.py -i $test_data/cluster_genes_dis_desagg -x 1 -s "," -a 2 1> $out/cluster_genes_dis_AGG
cat $test_data/cluster_genes_dis_desagg | aggregate_column_data.py -i '-' -x 1 -s "," -a 2 1> $out/cluster_genes_dis_AGG_stdin

#desaggregate_column_data --------------------------------------------------------------------------
desaggregate_column_data.py -i $test_data/cluster_genes_dis_agg -x 1 1> $out/cluster_genes_dis_DESAGG
cat $test_data/cluster_genes_dis_agg| aggregate_column_data.py -i '-' -x 2 -s "," -a 1 1> $out/cluster_genes_dis_DESAGG_stdin

#create_metric_table --------------------------------------------------------------------------
create_metric_table.py $test_data/all_metrics sample $out/metric_table -c TEST_file

#merge_tabular --------------------------------------------------------------------------
merge_tabular.py $test_data/disease_gene $test_data/disease_cluster_uniq > $out/merge_disease_cluster_gene

#tag_table --------------------------------------------------------------------------
tag_table.py -i $test_data/cluster_stats -t $test_data/tracker 1> $out/tag_table
tag_table.py -i $test_data/cluster_stats_header -H -t $test_data/tracker 1> $out/tag_table_header

# intersect_columns.py --------------------------------------------------------------------------
##default values
intersect_columns.py -a $test_data/disease_cluster -b $test_data/disease_gene -A 1 -B 1 1> $out/intersect_columns_default
##STDIN a
cat $test_data/disease_cluster | intersect_columns.py -a'-' -b $test_data/disease_gene -A 1 -B 1 1> $out/intersect_columns_default_stdin_a
##STDIN b
cat $test_data/disease_gene | intersect_columns.py -a $test_data/disease_cluster -b '-' -A 1 -B 1 1> $out/intersect_columns_default_stdin_b
##STDIN a y b
#cat $test_data/disease_cluster, $test_data/disease_gene | intersect_columns.py $test_data/disease_gene -a'-' -b '-' -A 1 -B 1 > $out/intersect_columns_default_stdin_a_b
##count = true
intersect_columns.py -a $test_data/disease_cluster -b $test_data/disease_gene -A 1 -B 1 -c 1> $out/intersect_columns_count
##keep = 'ab'
#intersect_columns.py -a $test_data/disease_cluster -b $test_data/disease_gene -A 1 -B 1 -k 'ab' > $out/intersect_columns_ab
##full = true
intersect_columns.py -a $test_data/disease_cluster -b $test_data/disease_gene -A 1 -B 1 --full  1> $out/intersect_columns_full

#table_linker --------------------------------------------------------------------------
#test standard
table_linker.py -i $test_data/disease_cluster -l $test_data/disease_gene -o $out/linked_table
#test reverse 
table_linker.py -i $test_data/disease_gene -l $test_data/disease_cluster -o $out/linked_table_2
#test remove mismatches
table_linker.py -i $test_data/disease_cluster -l $test_data/disease_gene -o $out/linked_table_matches --drop


#standard_name_replacer --------------------------------------------------------------------------
standard_name_replacer.py -i $test_data/disease_cluster -I $test_data/disease_gene -o $out/replaced_name -c 1 -f 1 -t 2 
#test keep untranslated
standard_name_replacer.py -i $test_data/disease_cluster -I $test_data/disease_gene -o $out/replaced_name_untranstaled -c 1 -f 1 -t 2 -u

#excel_to_tabular.py --------------------------------------------------------------------------
excel_to_tabular.py -i $test_data/cluster_genes.xlsx -c 2,3,4 -s 1 -o $out/cluster_genes_from_excel.txt
#column_filter.py --------------------------------------------------------------------------
#test column matching hard
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1 -k "MONDO:0008995" -s "c" -m "c" > $out/column_matching_hard
#test column matching soft
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1 -k "MONDO" -s "c" -m "i" > $out/column_matching_soft
#test column matching hard various keys 
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1 -k "MONDO:0008995&MONDO:0017999" -s "c" -m "c" > $out/column_matching_hard_various_keys
#test column matching hard various keys and every columns 
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1,2 -k "MONDO:0008995&MONDO:0017999%53_ref" -s "c" -m "c" > $out/column_matching_hard_various_keys_and_every_columns
#test column matching hard various keys and every columns to test header 
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1,2 -k "MONDO:0008995&MONDO:0017999%53_ref" -s "c" -m "c" -H > $out/column_matching_hard_various_keys_and_every_columns_header
#test column matching hard various keys and some columns
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1,2 -k "MONDO:0008995&MONDO:0017999%53_ref" -s "s" -m "c" > $out/column_matching_hard_various_keys_and_some_columns
#test column matching soft and some columns
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1,2 -k "MONDO%ref" -s "s" -m "i" > $out/column_matching_soft_and_some_columns
#test column matching soft and every columns
column_filter.py  -t "$test_data/disease*" -c 1,2 -f 1,2 -k "MONDO%ref" -s "c" -m "i" > $out/column_matching_soft_and_every_columns
#test column matching soft 1 column
column_filter.py  -t "$test_data/disease*" -c 1 -f 1 -k "MONDO" -s "c" -m "i" > $out/column_matching_soft_1_column
#test column matching soft 1 column uniq
column_filter.py  -t "$test_data/disease*" -c 1 -f 1 -k "MONDO" -s "c" -m "i" -u > $out/column_matching_soft_1_column_uniq 
#test column matching soft 1 column reverse
column_filter.py  -t "$test_data/disease*" -c 1 -f 1 -k "17" -s "c" -m "i" -r > $out/column_matching_soft_1_column_reverse
exit

for file_to_test in `ls $out`; do
	echo $file_to_test
	diff $out/$file_to_test $data_to_test/$file_to_test"_to_test"
done