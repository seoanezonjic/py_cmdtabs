#!/usr/bin/env python

import argparse

def load_file(path):
    table = []
    with open(path,"r") as f:
        for line in f:
            table.append(line.rstrip().split("\t"))
    return table

def write_file(path, table):
    with open(f"transposed_{path}", "w") as f:
        for line in table:
            f.write("\t".join(line) + "\n")




parser = argparse.ArgumentParser()
parser.add_argument("-f",dest="data",help="file to transpose")
options = parser.parse_args()

table = load_file(options.data)
transposed_table = list(map(list, zip(*table)))
write_file(options.data,transposed_table)

