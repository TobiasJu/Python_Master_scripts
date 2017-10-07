#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shutil import copyfile
import argparse
import sys
import os

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--pdbdir", help="input pdb directory with all pdb****.ent.gz files")
parser.add_argument("-p", "--pdbtm", help="pdbtm_all.list.txt location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "This script crawls thorug a given directory with subdirectorys and searches for all transmembran proteins"
    parser.print_help()
    sys.exit(0)

# returns a list of all files in the dir with subdirs
def list_files(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            file_list.append(os.path.join(root, name))
    return file_list

# ------------------------------------------------- main script ------------------------------------------------------ #
print "started...\n"

pdbtm_list = []
dir_file_list = list_files(args.pdbdir)

with open(args.pdbtm, "r") as pdbtm_file_handle:
    for line in pdbtm_file_handle:
        name = line.split("_")[0]
        pdbtm_list.append(name)
print "read pdbtm.\n"

for pdb_file in dir_file_list:
    name1 = pdb_file.split("/")[-1]
    print name1
    name2 = name1.split("pdb")[-1]
    print name2
    pdb_name = name2.split(".ent.gz")[0]
    print pdb_name
    if pdb_name in pdbtm_list:
        print "copying file: ", pdb_file
        copyfile(pdb_file, "/ceph/sge-tmp/tjuhre/membranePDB/"+name1 )

print "done\n"