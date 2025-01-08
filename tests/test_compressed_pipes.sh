#!/usr/bin/env bash
source ~soft_bio_267/initializes/init_python

input_file=./data_tests/mondo_genes.gz
expected=./data_tests/ref_output_scripts/mondo_genes_transposed
returned=./tmp/mondo_genes_transposed
mkdir -p tmp

echo "Testing compressed stdin and stdout with transpose_table binary"
cat $input_file | transpose_table -i - --compressed_in --compressed_out > $returned.gz
gunzip $returned.gz
diff $returned $expected

rm -rf ./tmp/*
