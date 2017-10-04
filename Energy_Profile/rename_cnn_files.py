#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import itertools
import numpy as np


# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--energy_dir", help="input energy profile directory, with .cnn files (will iterate over all files)")
parser.add_argument("-f", "--energy_file", help="input energy profile file, with .cnn ending")
parser.add_argument("-o", "--out", help="output directory for renamed energy profile (only for -d)")

args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy pdb***.ent.ep2.cnn files and rename them properly"
    parser.print_help()
    sys.exit(0)

# ------------------------------------------------- main script ------------------------------------------------------ #


if args.out:
    output_folder = args.out + "/"
else:
    output_folder = "renamed_eps" + "/"
try:
    print "creating... ", output_folder
    os.makedirs(output_folder)
except(OSError):
    print output_folder, " already exists!"

if args.energy_dir:
    for dirpath, dir, files in os.walk(top=args.energy_dir):
        for energy_file in files:
            print energy_file
            new_file_name = ""
            counter = 0
            line_array = []
            with open(dirpath + energy_file, 'r') as energy_file_handle:
                for line in energy_file_handle:
                    if counter == 0:
                        full_name = line.split("\t")[1]
                        name_without_pdb = full_name.split("pdb")[-1]
                        name = name_without_pdb.split(".ent")[0]
                        # print name
                        counter += 1
                        name_line = "NAME\t" + name + "\n"
                        line_array.append(name_line)
                        new_file_name = name + ".ep2"
                    else:
                        line_array.append(line)
            target = open(output_folder + new_file_name, 'w')
            for line in line_array:
                target.write(line)
            target.close()

if args.energy_file:
    print args.energy_file
    new_file_name = ""
    counter = 0
    line_array = []
    with open(args.energy_file, 'r') as energy_file_handle:
        for line in energy_file_handle:
            if counter == 0:
                full_name = line.split("\t")[1]
                name_without_pdb = full_name.split("pdb")[-1]
                name = name_without_pdb.split(".ent")[0]
                counter += 1
                name_line = "NAME\t" + name + "\n"
                line_array.append(name_line)
                new_file_name = name + ".ep2"
            else:
                line_array.append(line)
    target = open(new_file_name, 'w')
    for line in line_array:
        target.write(line)
    target.close()
