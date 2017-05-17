#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import numpy
import collections
import json
import itertools
import matplotlib.pyplot as plt


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
            break
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

print "dumping dict to json file: energy_per_aa.txt"
json.dump(energy_dict, open("energy_per_aa.txt", 'w'))

mean_dict = collections.OrderedDict(sorted(mean_dict.items()))
std_dict = collections.OrderedDict(sorted(std_dict.items()))
min_dict = collections.OrderedDict(sorted(min_dict.items()))
max_dict = collections.OrderedDict(sorted(max_dict.items()))

print "mean: "
print mean_dict
print "std dev: "
print std_dict
print "min: "
print min_dict
print "max: "
print max_dict

print "plotting..."
print len(energy_dict.keys())

d = {'hello': 3, 'how': 4, 'yes': 10, 'you': 11, 'days': 10, 'are': 20, 'ago': 11}

plt.bar(range(len(d)), d.values(), align="center")
plt.xticks(range(len(d)), list(d.keys()))
plt.show()
sys.exit(0)


d = {"A": ['4026', '4024', '1940', '2912', '2916'], "B": ['3139', '2464'], 3: ['212'], 4: ['231', '312']}
x= []
y= []
for k, v in d.iteritems():
    x.extend(list(itertools.repeat(k, len(v))))
    y.extend(v)
plt.xlim(0, 5)
plt.plot(x, y, 'ro')

plt.show()
sys.exit(0)



#all_data = [numpy.random.normal(0, std, 100) for std in range(6, 10)]
fig, ax1 = plt.subplots(figsize=(9, 4))

# plot violin plot
ax1.violinplot(energy_dict,
                   showmeans=True,
                   showmedians=False)
ax1.set_title('violin plot')

# adding horizontal grid lines
ax1.yaxis.grid(True)
ax1.set_xticks([y+1 for y in range(len(energy_dict))])
ax1.set_xlabel('xlabel')
ax1.set_ylabel('ylabel')

# add x-tick labels
#ax1.setp(xticks=[y+1 for y in range(len(energy_dict))],
#                 xticklabels=['x1', 'x2', 'x3', 'x4'])  # len(energy_dict.keys())

plt.savefig('foo.pdf')
plt.show()
print "done"
