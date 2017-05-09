#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

input_dir = "Pfam 31.0/globular_seq"
output_dir = "Pfam 31.0/globular_empty"

# walk through the given directory and check if Pfam ID is in the pdbmap file (if the structure is cleared)
for dirpath, dir, files in os.walk(top=input_dir):
    for file in files:
        is_empty = "true"
        line_count = 0
        print "open: "
        print input_dir + file
        with open(input_dir + file, 'r') as pfam_family:
            for line in pfam_family:
                if not "//" or not "#" in line:
                    is_empty = "false"

        if is_empty == "true":
            print "moving empty file:" + file
            shutil.move(dirpath + file, output_dir)
