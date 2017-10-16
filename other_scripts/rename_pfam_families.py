#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script renames Pfam Familes from their ID to their Accession number
#=GF ID   1-cysPrx_C
#=GF AC   PF10417.8

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
    print "this script renames Pfam Familes from their ID to their Accession number"
    parser.print_help()
    sys.exit(0)


def copy_rename(old_file_name, new_file_name, dst_dir):
    # src_dir = os.curdir
    # dst_dir = os.path.join(os.curdir, destination)
    # src_file = os.path.join(src_dir, old_file_name)
    #shutil.copy(old_file_name, dst_dir)
    #print old_file_name
    dst_file = old_file_name
    new_dst_file_name = os.path.join(dst_dir, new_file_name)
    #print dst_file
    #print new_dst_file_name
    os.rename(dst_file, new_dst_file_name)
    #sys.exit(0)

# ------------------------------- main script -------------------------------- #

input = args.directory
dest = os.path.join(input, "renamed/")
pfam_counter = 0

try:
  os.makedirs(dest)
except:
  print "Folder " + dest + " already exist!"

for dirpath, dir, files in os.walk(top=input):
    for file in files:
        line_count = 0
        with open(dirpath + file, 'r') as pfam_family:
            for line in pfam_family:
                line_count += 1
                if "#=GF AC" in line:
                    line_array = line.split("#=GF AC   ")
                    pfam_ac = line_array[-1].strip()
                    print pfam_ac
                    pfam_counter += 1
                    input_file = os.path.join(dirpath + file)
                    output_file = pfam_ac + ".txt"
                    copy_rename(input_file, output_file, dest)
                if line_count >= 5:
                    break

