#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import numpy
import collections

# PLEASE NOTICE, this script takes at least 8GB of RAM! If you calculate mean/std/min/max for all 346366 energy files

# argparse for information
parser = argparse.ArgumentParser()
# parser.add_argument("-d", "--directory", help="input directory of the Pfam family files")
parser.add_argument("-e", "--energy", help="input energy profile directory")
# parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and analyzes them"
    parser.print_help()
    sys.exit(0)


# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))

# ---------------------------------------- main script ------------------------------------------ #

counter = 0
energy_dict = {}

print "starting..."

for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        line_count = 0
        counter += 1
        if counter % 10000 == 0:
            print energy_file
            #break
        if energy_file.endswith(".ep2"):
            with open(dirpath + energy_file, 'r') as energy_file_handle:  # with open(energy_dir + file, 'r') as energy_file:
                for line in energy_file_handle:
                    line_array = line.split("\t")
                    if not "REMK" in line_array:
                        if line_count == 0:
                            name = line_array[1]
                        elif line_count == 1:
                            aa_type = line_array[1]
                        elif line_count == 2:
                            header = line_array
                        else:
                            # just extract the A Chain
                            # if line_array[1] == "B":
                            #    break
                            insert_into_data_structure(line_array[3].rstrip(), line_array[5].rstrip(), energy_dict)

                    line_count += 1

print "creating dicts..."
mean_dict = {}
std_dict = {}
min_dict = {}
max_dict = {}
for key in energy_dict:
    energy_list = energy_dict[key]
    energy_list = [float(x) for x in energy_list]
    #print len(energy_list)
    insert_into_data_structure(key, numpy.mean(energy_list), mean_dict)
    insert_into_data_structure(key, numpy.std(energy_list), std_dict)
    insert_into_data_structure(key, numpy.amin(energy_list), min_dict)
    insert_into_data_structure(key, numpy.amax(energy_list), max_dict)

mean_dict = collections.OrderedDict(sorted(mean_dict.items()))
std_dict = collections.OrderedDict(sorted(std_dict.items()))
min_dict = collections.OrderedDict(sorted(min_dict.items()))
max_dict = collections.OrderedDict(sorted(max_dict.items()))

print mean_dict
print "std dev: "
print std_dict
print "min: "
print min_dict
print "max: "
print max_dict

print "done"
