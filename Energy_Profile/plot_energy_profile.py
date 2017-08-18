#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import scipy
import pylab
import matplotlib.patches as mpatches

import numpy as np
import matplotlib.pyplot as plt
import sys

import argparse


##plot 2 energy profiles in one plot to compare them

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-e1", "--energy_profile_1", help="input energy profile number 1")
parser.add_argument("-e2", "--energy_profile_2", help="input energy profile number 2")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and analyzes them"
    parser.print_help()
    sys.exit(0)


def plotting(energy_file1, energy_file2):
    #patd = {}
    #heald = {}

    energy_list1 = []
    energy_list2 = []
    pos_list = []

    with open(energy_file1) as inf:
        for line in inf:
            if "ENGY" in line:
                spl = line.split('\t')
                energy_list1.append(float(spl[5]))
                pos_list.append(int(spl[2]))
    with open(energy_file2) as inf:
        for line in inf:
            if "ENGY" in line:
                spl = line.split('\t')
                energy_list2.append(float(spl[5]))

    labels = []
    countheal = []
    countpat = []
    maxval = max(k for k in energy_list1)

#    max_count = 0

    for energy1, energy2, pos in zip(energy_list1, energy_list2, pos_list):
        labels.append(pos)
        countheal.append(energy1)
        countpat.append(energy2)
#    if max(countpat) > max_count:
#        max_count = max(countpat)
#    if max(countheal) > max_count:
#        max_count = max(countheal)
    y_p = np.array(countpat)
    y_h = np.array(countheal)
    x_h = np.array(labels)

    w = 4000
    h = 1000

    plt.rcParams["figure.figsize"] = (400, 100)
    plt.axis([pos_list[0], pos_list[-1], -60, 10])
    plt.plot(x_h, y_h, 'r-', label="Energy File 1")
    plt.plot(x_h, y_p, 'b-', label="Energy File 2")

    outfile = "comp_plot_" + str(energy_file1) + "_" + str(energy_file1)
    outfile = "comp_plot"
    plt.xlabel("ResNo")
    plt.ylabel("Energy value")
    plt.title("Energy compairson")
    plt.legend()
    plt.savefig(outfile+".png", dpi=1200)
    plt.close()


# ------------------------------------------------- main script ------------------------------------------------------ #

print "plotting: ", args.energy_profile_1, args.energy_profile_2
plotting(args.energy_profile_1, args.energy_profile_2)

