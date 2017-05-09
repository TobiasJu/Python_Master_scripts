#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

pdbmap = args.pdbmap
ids = []

# sanity check
if not len(sys.argv) > 1:
    print "this script takes the pdbmap file and extracts all UniProtKB IDs in smaller list files"
    parser.print_help()
    sys.exit(0)

# load all pfam ids from the pdbmap file into a list
with open(pdbmap, 'r') as pdbmap_file:
    for line in pdbmap_file:
        line_array = line.split(";\t")
        uniprotkb_id = line_array[4]
        ids.append(uniprotkb_id)

target = open("ids.txt", 'w')
target2 = open("ids2.txt", 'w')
target3 = open("ids3.txt", 'w')
target4 = open("ids4.txt", 'w')
counter = 0
for id in ids:
    counter += 1
    if counter < 125000:
        target.write(id + "\n")
    elif 125000 < counter < 250000:
        target2.write(id + "\n")
    elif 250000 < counter < 375000:
        target3.write(id + "\n")
    else:
        target4.write(id + "\n")

target.close()
target2.close()
print "Finished"