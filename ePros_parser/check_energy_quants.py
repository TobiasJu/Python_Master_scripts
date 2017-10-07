#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import epros_file
import matplotlib.pyplot as plt
import numpy as np
from outliers import smirnov_grubbs as grubbs

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--energy", help="input energy profile directory")
parser.add_argument("-g", "--glob", help="globular proteins only")
parser.add_argument("-t", "--transmembrane", help="transmembrane proteins only, enter path/to/pdbtm_all.list.txt")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and prints out the quantil ranges"
    parser.print_help()
    sys.exit(0)


def plot_boxplot(energy_dict):
    print "plotting violin_box_plot"
    index = []
    data = []
    for i, (key, val) in enumerate(energy_dict.iteritems()):
        index.append(key)
        data.append(map(float, val))
    fig, (ax, ax2) = plt.subplots(ncols=2)
    ax.boxplot(data)
    ax.set_xticklabels(index)
    ax2.violinplot(data)
    ax2.set_xticks(range(1, len(index) + 1))
    ax2.set_xticklabels(index)
    plt.savefig('box_violin_plot.pdf')

# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))

# ------------------------------------------------- main script ------------------------------------------------------ #

# pdbtm_all.list.txt
pdbtm_list = []
energy_list = []
counter = 0
total_file_count = sum([len(files) for r, d, files in os.walk(top=args.energy)])
print "started for:", total_file_count, "files"

if args.transmembrane:
    with open(args.transmembrane, 'r') as pdbtm_list_handle:
        for line in pdbtm_list_handle:
            line_array = line.split("_")
            pdbtm_list.append(line_array[0])
    print pdbtm_list

for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        line_count = 0
        counter += 1
        if counter % 10000 == 0:
            print energy_file
            percentage = (float(counter) / float(total_file_count))*100
            print"{:.2f}".format(percentage), "%"
        if energy_file.endswith(".ep2"):
            if args.glob:
                name = energy_file.split(".ep2")[0]
                if name in pdbtm_list:
                    continue
            if args.transmembrane:
                name = energy_file.split(".ep2")[0]
                if name not in pdbtm_list:
                    continue
            with open(dirpath + "/" + energy_file, 'r') as energy_file_handle:  # with open(energy_dir + file, 'r') as energy_file:
                for line in energy_file_handle:
                    line_array = line.split("\t")
                    if not "REMK" in line_array:
                        if line_count == 0:
                            name = line_array[1]
                        elif line_count == 1:
                            typ = line_array[1]
                        elif line_count == 2:
                            header = line_array
                        else:
                            # just extract the A Chain
                            # if line_array[1] == "B":
                            #    break
                            energy_list.append(line_array[5].rstrip())
                    line_count += 1

energy_list = [float(x) for x in energy_list]
energy_list.sort()
# remove outliers with grubbs algorithm
energy_list = grubbs.test(energy_list, alpha=0.05)
print "Quantiles for: ", total_file_count, "files"
quant = len(energy_list)/4
print quant, "entries per quantil"
print energy_list[0]
print energy_list[quant]
print energy_list[2*quant]
print energy_list[3*quant]
print energy_list[-1]

plt.figure()
plt.boxplot(energy_list, 0, '')
plt.savefig('quantiles.pdf')

###################### OUT
'''
119460386
Quantil:  29865096
-118.303418308
-21.3328509911
-9.26231037705
-3.33429827376
11.5566432042

whithout outliers
Quantil:  29864995
-81,4800043161
-21,3326960217
-9,26223609962
-3,33428488184
11,5566432042

new Quantile for globular:
-81.2912287163
-21.5377154868
-9.50643383752
-3.44146165978
11.768577356

Quantile for membrane:

3101 files
-12.2373208162
4.49279516205
8.98564351117
13.4598691639
46.4967251975


'''

