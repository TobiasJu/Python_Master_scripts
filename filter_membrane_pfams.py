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
parser.add_argument("-d", "--directory", help="input directory")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "This script takes the extracted protein families from the extract_protein_families.py and divides them " \
          "into two folders of membrane and globular associated Proteins"
    parser.print_help()
    sys.exit(0)

input = args.directory
membran_dest = 'membrane/'
glob_dest = 'globular/'

try:
  os.makedirs(membran_dest)
  os.makedirs(glob_dest)
except:
  print "Folder membrane/ or glob/ already exist!"

membrane_ids = []

with open('membrane_pfam.tsv', 'r') as all_membrane_proteins:
    for line in all_membrane_proteins:
        line_array = line.split("\t")
        id = line_array[0]
        #print id
        membrane_ids.append(id)

# print membrane_ids
membrane_counter = 1
# walk through the given directory and check if id is in the file, then move it accordingly
for dirpath, dir, files in os.walk(top=input):
    for file in files:
        line_count = 0
        with open(input + file, 'r') as pfam_family:
            for line in pfam_family:
                if "#=GF AC" in line:
                    array = line.split("#=GF AC   ")
                    pfam_id_with_version = array[-1]
                    pfam_id_with_version_array = pfam_id_with_version.split(".")
                    pfam_id = pfam_id_with_version_array[0]
                    #print pfam_id
                    if pfam_id in membrane_ids:
                        print pfam_id
                        membrane_counter += 1
                        shutil.move(input + file, membran_dest)
                    else:
                        shutil.move(input + file, glob_dest)
                line_count += 1
                if line_count >= 5:
                    break

print "found" + str(membrane_counter) + "Families"
