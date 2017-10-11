#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import argparse

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pfam_directory", help="pfam directory")
parser.add_argument("-o", "--output_directory", help="output directory for emtpy pfams")

args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print ""
    parser.print_help()
    sys.exit(0)

input_dir = args.pfam_directory
dest = args.output_directory

try:
    print "Making directory", dest
    os.makedirs(dest)
except:
    print "Folder " + dest + " already exist!"

empty_counter = 0
print "iterating over pfam directory and searching for emtpy fams"
for dirpath, dir, files in os.walk(top=input_dir):
    for file in files:
        is_empty = "true"
        line_count = 0
        print "checking: "
        print input_dir + file
        with open(input_dir + file, 'r') as pfam_family:
            for line in pfam_family:
                if "//" in line:
                    break
                if "#" not in line:
                    is_empty = "false"
        if is_empty == "true":
            print "moving pfam without sequences:" + file
            shutil.move(dirpath + file, dest)
            empty_counter += 1

print "Found", empty_counter, "empty pfams"
