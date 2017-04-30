#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script takes the extracted protein families from the extract_protein_families.py and divides them into
# two folders of membrane and globular associated Proteins

import os
import sys

input = "Pfam 31.0/membrane/"
output = "Pfam 31.0/membrane_fix/"

try:
    os.makedirs(output)
except:
    print "Folder membrane/ or glob/ already exist!"

print input

for dirpath, dir, files in os.walk(top=input):
    for file in files:
        print file
        stockholm_count = 0
        with open(input + file, 'r') as pfam_family:
            target = open(output + file, 'w')
            target.write("# STOCKHOLM 1.0\n")
            for line in pfam_family:
                if "# STOCKHOLM 1.0" in line and stockholm_count == 0:
                    stockholm_count += 1
                    target.write(line)
                elif "# STOCKHOLM 1.0" in line and stockholm_count == 1:
                    machnix = 0
                else:
                    target.write(line)

        target.close()
