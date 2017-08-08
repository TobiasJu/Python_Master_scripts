#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import gzip
import glob
import os.path
import sys

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="directory with .gz files")
parser.add_argument("-o", "--output", help="directory where to extract the files")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder full of .gz files and extracts them to a given location"
    parser.print_help()
    sys.exit(0)

source_dir = args.input
output_folder = args.output

try:
    os.makedirs(output_folder)
except:
    print output_folder, " already exists!"

for src_name in glob.glob(os.path.join(source_dir, '*.gz')):
    base = os.path.basename(src_name)
    dest_name = os.path.join(output_folder, base[:-3])
    with gzip.open(src_name, 'rb') as infile:
        print "extracting: ", infile
        with open(dest_name, 'wb') as outfile:
            for line in infile:
                outfile.write(line)
