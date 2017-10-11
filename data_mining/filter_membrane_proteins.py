#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--pdbmap", help="pdbmap file location")
parser.add_argument("-t", "--pdbtm", help="pdbtm_all.list.txt location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script splits the pdbmap into globular and membrane associated IDs using the pdbtm_all.list.txt"
    parser.print_help()
    sys.exit(0)

# note: this script does not take care of chains
# ------------------------------------------------- main script ------------------------------------------------------ #
print "started"
pdbtm_list = []

with open(args.pdbtm, "r") as pdbtm_file_handle:
    for line in pdbtm_file_handle:
        name = line.split("_")[0].upper()
        pdbtm_list.append(name)
print "read pdbtm_all.list.txt"

membrane_ids = open("pdbmap_membrane.txt", 'w')
globular_ids = open("pdbmap_globular.txt", 'w')

membrane_counter = 0
glob_counter = 0
progress_counter = 0

print "iterating over pdbmap"
with open(args.pdbmap, 'r') as pdbmap:
    for line in pdbmap:
        stripped_line = line.rstrip().replace(";", "")
        line_array = stripped_line.split("\t")
        pdb_id = line_array[0]
        #print pdb_id
        if pdb_id in pdbtm_list:
            membrane_ids.write(line)
            membrane_counter += 1
        else:
            globular_ids.write(line)
            glob_counter += 1
        progress_counter += 1

        if progress_counter % 10000 == 0:
            print "iterated over: ", progress_counter, " lines"

membrane_ids.close()
globular_ids.close()

print "Extracted: " + str(glob_counter) + " globular IDs, written to: pdbmap_globular.txt"
print "Extracted: " + str(membrane_counter) + " membrane associated IDs, written to: pdbmap_membrane.txt"


