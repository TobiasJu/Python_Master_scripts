#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script fixes the missing /n in the header row of a stockholm file e.g.
# STOCKHOLM 1.0#=GF ID   1-cysPrx_C

import os
import sys

input = "Pfam 31.0/globular_filtered_seq/"
output = "Pfam 31.0/globular_fix/"

try:
    os.makedirs(output)
except:
    print "Folder membrane/ or glob/ already exist!"

print input

for dirpath, dir, files in os.walk(top=input):
    for file in files:
        print "fixing: " + file
        stockholm_count = 0
        with open(input + file, 'rU') as pfam_family:
            target = open(output + file, 'w')
            for line in pfam_family:
                if "# STOCKHOLM 1.0" in line and stockholm_count == 0:
                    stockholm_count += 1
                    line_array = line.split("#=")
                    target.write("# STOCKHOLM 1.0\n")
                    target.write("#=" + line_array[-1])
                else:
                    target.write(line)
        target.close()
