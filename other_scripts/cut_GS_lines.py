#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script takes the extracted protein families from the extract_protein_families.py and divides them into
# two folders of membrane and globular associated Proteins

import os
import sys

input = "Pfam 31.0/globular_fix/"
output = "Pfam 31.0/globular_cut/"

try:
    os.makedirs(output)
except:
    print "Folder " + output + " already exist!"

print input

# check if the file is already done, in case of interrupt
already_done = []
for dirpath1, dir1, files1 in os.walk(top=output):
    for file1 in files1:
        already_done.append(file1)

for dirpath, dir, files in os.walk(top=input):
    for file in files:
        if file in already_done:
            print "skipping: " + file
        else:
            print file
            stockholm_count = 0
            with open(input + file, 'r') as pfam_family:
                target = open(output + file, 'w')
                target.write("# STOCKHOLM 1.0\n")
                for line in pfam_family:
                    if "#=GS " not in line:
                        if "# STOCKHOLM 1.0" in line:
                            doNothing = 0
                        else:
                            target.write(line)
            target.close()

