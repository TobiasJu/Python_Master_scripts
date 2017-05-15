#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

input_dir = "Pfam 31.0/globular/"
dest = "Pfam 31.0/globular_less_than_10/"

try:
    os.makedirs(dest)
except:
    print "Folder " + dest + " already exist!"

# walk through the given directory and check if Pfam ID is in the pdbmap file (if the structure is cleared)
for dirpath, dir, files in os.walk(top=input_dir):
    for file in files:
        seq_counter = 0
        line_count = 0
        print "checking: "
        print input_dir + file
        with open(input_dir + file, 'r') as pfam_family:
            for line in pfam_family:
                if "//" in line:
                    break
                if "#" not in line:
                    seq_counter += 1
        if seq_counter < 10:
            print "moving pfam with less than 10 sequences: " + file
            shutil.move(dirpath + file, dest)
