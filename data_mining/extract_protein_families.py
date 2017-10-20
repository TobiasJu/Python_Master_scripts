#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


# this script extracts all Proteinfamilies from the given pfam Pfam-A.full.ncbi file (222GB)
# and creates a file for each family in the split/ folder
#=GF AC   PF10417.8

count = 0
directory = "pfam_split/"

try:
    os.stat(directory)
except:
    os.mkdir(directory)

print "making directory ", directory, " in current folder"
print "looking for Pfam-A.full.ncbi in current folder"

id_line_flag = False
write_flag = False

with open('Pfam-A.full.ncbi', 'r') as all_families_file:
    for line in all_families_file:
        if "#=GF ID   " in line:
            id_line = line
            id_line_flag = True
        elif "#=GF AC   " in line:
            accession_line = line.split("#=GF AC   ")
            ac = accession_line[1].strip()
            print ac
            target = open(directory + ac + ".txt", 'w')
            write_flag = True
            count += 1
        if id_line_flag == True and write_flag == True:
            target.write("# STOCKHOLM 1.0\n")
            target.write(id_line)
            id_line_flag = False
            write_flag = True
        if "//" in line:
            target.write(line)
            target.close()
            write_flag = False
        elif write_flag == True:
            target.write(line)

print "done with", count, "Families"

