#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script takes a folder of PFAM families and extracts the ones with cleared structure in the PDB

import argparse
import sys
import os
import shutil

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory of the Pfam family files", required=True)
parser.add_argument("-p", "--pdbmap", help="pdbmap location", required=True)
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of PFAM families and extracts the ones with cleared structure in the PDB"
    parser.print_help()
    sys.exit(0)

input_dir = args.directory
pdbmap = args.pdbmap
pdb_ids = []
pfam_ids = []
hit_count = 0
hit_array = []
output_dir = "/Pfam 31.0/membrane_filtered"
print output_dir
#dstdir = os.path.join(output_dir, os.path.dirname(file))

try:
    os.stat(output_dir)
except:
    os.mkdir(output_dir)

with open(pdbmap, 'r') as pdbmap_file:
    for line in pdbmap_file:
        line_array = line.split(";\t")
        pdb_id = line_array[0]
        pfam_id = line_array[3]
        pfam_ids.append(pfam_id)
        pdb_ids.append(pdb_id)

print len(pfam_ids)
print len(pdb_ids)

# walk through the given directory and check if Pfam ID is in the pdbmap file (if the structure is cleared)
for dirpath, dir, files in os.walk(top=input_dir):
    for file in files:
        line_count = 0
        print "open: "
        print input_dir + file
        with open(input_dir + file, 'r') as pfam_family:
            for line in pfam_family:
                if "#=GF AC" in line:
                    array = line.split("#=GF AC   ")
                    pfam_id_with_version = array[-1]
                    pfam_id_with_version_array = pfam_id_with_version.split(".")
                    file_pfam_id = pfam_id_with_version_array[0]
                    if file_pfam_id in pfam_ids:
                        print file_pfam_id
                        hit_count += 1
                        hit_array.append(file_pfam_id)
                        shutil.copy(dir + file, output_dir)
                    else:
                        doNothing = 0
                line_count += 1
                if line_count >= 5:
                    break

print "finished!"
print hit_count
print len(hit_array)
print len(list(set(hit_array)))
