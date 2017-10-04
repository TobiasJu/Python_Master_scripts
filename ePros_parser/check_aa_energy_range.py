#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import numpy
import collections
import json
import itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
from outliers import smirnov_grubbs as grubbs
from scipy import stats
import timeit

# argparse for information
parser = argparse.ArgumentParser()
# parser.add_argument("-d", "--directory", help="input directory of the Pfam family files")
parser.add_argument("-e", "--energy", help="input energy profile directory")
# parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "This script takes a folder of energy files, analyzes them and print min, max, avg."
    print "This script can also plot box and violin plots if you uncomment the plot sections."
    print "PLEASE NOTICE: This script takes at least 8GB of RAM! If you calculate mean/std/min/max for all 346366 energy files"
    parser.print_help()
    sys.exit(0)

# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    value = float(value)
    if not value == 0:
        if not key in dict:
            dict[key] = [(value)]
        else:
            dict[key].append((value))

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

def plot_swarmplot(data_set):
    print "plotting swarmplot"
    sns.set_style("whitegrid")
    tips = sns.load_dataset("tips")
    ax = sns.swarmplot(x="day", y="total_bill", data=data_set)
    ax = sns.boxplot(x="day", y="total_bill", data=data_set,
                     showcaps=False, boxprops={'facecolor': 'None'},
                     showfliers=False, whiskerprops={'linewidth': 0})
    plt.savefig('swarmplot.pdf')

def plot_histogramm(energy_dict):
    print "plotting histogramm"
    for key in energy_dict:
        print key
        x = []
        for value in energy_dict[key]:
            x.append(value)
        sns_plot = sns.distplot(x)
        sns_plot_all = sns.distplot(x)
        sns_plot.figure.savefig("histogramm_" + key + ".png")
        sns_plot_all.figure.savefig("histogramm_all.png")
        sns_plot.figure.clf()


# ------------------------------------------------ main script ------------------------------------------------------- #

counter = 0
energy_dict = {}
start_time = timeit.default_timer()
total_file_count = sum([len(files) for r, d, files in os.walk(top=args.energy)])

print "started for:", total_file_count, "files"
for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        line_count = 0
        counter += 1
        if counter % 10000 == 0:
            print energy_file
            percentage = counter / total_file_count
            print"{:.2f}".format(percentage), "%"
        if energy_file.endswith(".ep2"):
            with open(dirpath + energy_file, 'r') as energy_file_handle:
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
grubbs_dict = {}
for key in energy_dict:
    energy_list = energy_dict[key]
    energy_list = [float(x) for x in energy_list]

    len_before = len(energy_list)
    energy_list = grubbs.test(energy_list, alpha=0.05)  # trim with the grubbs test
    # energy_list = stats.trim_mean(energy_list, 0.01)  # Trim 1% at both ends
    # check if normal distributed
    print stats.normaltest(energy_list)
    len_after = len(energy_list)
    print len_before - len_after, " subtracted from: ", key
    energy_list.sort()
    # print energy_list[0:10]
    insert_into_data_structure(key, numpy.mean(energy_list), mean_dict)
    insert_into_data_structure(key, numpy.std(energy_list), std_dict)
    insert_into_data_structure(key, numpy.amin(energy_list), min_dict)
    insert_into_data_structure(key, numpy.amax(energy_list), max_dict)
    grubbs_dict[key] = energy_list

# print "dumping dict to json file: energy_per_aa.txt"
# json.dump(energy_dict, open("energy_per_aa.txt", 'w'))

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
# plot_boxplot(grubbs_dict)
# plot_swarmplot(grubbs_dict)
plot_histogramm(grubbs_dict)

end_time = timeit.default_timer()
print "done"
print start_time - end_time


