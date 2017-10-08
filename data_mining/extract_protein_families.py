#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


# this script extracts all Proteinfamilies from the given pfam Pfam-A.full.ncbi file (222GB)
# and creates a file for each family in the split/ folder
#=GF AC   PF10417.8

line_count = 0
directory = "split/"

try:
    os.stat(directory)
except:
    os.mkdir(directory)

with open('Pfam-A.full.ncbi', 'r') as all_families_file:
    for line in all_families_file:
        if "#=GF AC   " in line:
            id_line = line.split("#=GF AC   ")
            id = id_line[1].strip()
            print id
            try:
                target.close()
            except:
                print "First run"
            target = open("split/" + id + ".txt", 'w')
            line_count += 1
        try:
            target.write(line)
        except:
            print "no target to write to"
print line_count

