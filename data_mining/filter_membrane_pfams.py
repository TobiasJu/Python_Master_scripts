#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script takes the extracted protein families from the extract_protein_families.py and divides them into
# two folders of membrane and globular associated Proteins

import shutil
import argparse
import os
import sys

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pfam_directory", help="pfam_dir pfam directory")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "This script takes the extracted protein families from the extract_protein_families.py and divides them " \
          "into two folders of membrane and globular associated Proteins, after you have generated the " \
          "pdbmap_membrane.txt file with the extract_protein_families.py"
    parser.print_help()
    sys.exit(0)

pfam_dir = args.pfam_directory
membran_dest = 'pfam_membrane/'
glob_dest = 'pfam_globular/'

try:
    print "making folders:", membran_dest, "and", glob_dest
    os.makedirs(membran_dest)
    os.makedirs(glob_dest)
except:
    print "Folder ", membran_dest, " or ", glob_dest, " already exist!"

membrane_ids = []

print "iterating over pdbmap_membrane"
with open('pdbmap_membrane.txt', 'r') as pdbmap_membrane:
    for line in pdbmap_membrane:
        stripped_line = line.rstrip().replace(";", "")
        line_array = stripped_line.split("\t")
        pfam_id_pdbmap = line_array[4]
        membrane_ids.append(pfam_id_pdbmap)
# print membrane_ids
membrane_counter = 1
# walk through the given directory and check if id is in the file, then move it accordingly

print "iterating over pfam directory"
for dirpath, dir, files in os.walk(top=pfam_dir):
    for file in files:
        pfam_id = file.split(".")[0]
        if pfam_id in membrane_ids:
            print pfam_id
            membrane_counter += 1
            shutil.move(pfam_dir + file, membran_dest)
        else:
            shutil.move(pfam_dir + file, glob_dest)

print "found", membrane_counter, "membrane Families"

