#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


# this script extracts all Proteinfamilies from the given pfam Pfam-A.full.ncbi file (28GB)
# and creates a file for each family

########## WICHTIG splittet an ID nicht an //  muss noch gefixxt werden ########

line_count = 0
directory = "split/"

try:
    os.stat(directory)
except:
    os.mkdir(directory)

with open('Pfam-A.full.ncbi', 'r') as all_families_file:
    for line in all_families_file:
        if "#=GF ID   " in line:
            id_line = line.split("#=GF ID   ")
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
