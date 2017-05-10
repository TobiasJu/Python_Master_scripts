#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script takes a folder of PFAM family sequences and extracts the sequences which have cleared structures in the pdb

import argparse
import sys
import os
from Bio import AlignIO

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory of the Pfam family files")
parser.add_argument("-i", "--idmap", help="mapped ids location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of PFAM family sequences and extracts the sequences which have cleared " \
          "structures in the pdb"
    parser.print_help()
    sys.exit(0)

if not args.idmap or not args.directory:
    print "missing input!"
    print "please provide the needed input"
    parser.print_help()
    sys.exit(0)

input_dir = args.directory
id_map = args.idmap
hit_count = 0
ids = []
output_dir = "Pfam 31.0/globular_filtered_seq/"
print "output dir: " + output_dir

try:
    os.makedirs(output_dir)
except:
    print "Folder " + output_dir + " already exist!"
    sys.exit(0)

# load all pfam ids from the id_map file into a list
with open(id_map, 'r') as id_map_file:
    for line in id_map_file:
        line_array = line.split(";\t")
        id = line_array[0].strip()
        ids.append(id)

# walk through the given directory and check if id is in the file, then move it accordingly
for dirpath, dir, files in os.walk(top=input_dir):
    for file in files:
        print file
        line_count = 0
        print "writing to: " + output_dir + file
        target = open(output_dir + file, 'w')
        target.write("# STOCKHOLM 1.0\n")
        with open(dirpath + file, 'r') as pfam_family:
            for line in pfam_family:
                if "#=" in line:
                    target.write(line)
                else:
                    line_array = line.split("/")
                    id = line_array[0]
                    if id in ids:
                        print line
                        target.write(line)
                        hit_count += 1
                line_count += 1
        target.write("//")
        target.close()
print "found " + str(hit_count) + " Sequences"

