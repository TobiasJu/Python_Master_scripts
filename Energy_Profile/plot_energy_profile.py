#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import Bio.SeqUtils
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
import re


##plot 2 energy profiles in one plot to compare them

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-e1", "--energy_profile_1", help="input energy profile number 1")
parser.add_argument("-e2", "--energy_profile_2", help="input energy profile number 2")
parser.add_argument("-m", "--marker", help="SNP position number")
parser.add_argument("-a", "--aminoacid", help="new Aminoacid SNP if any")

args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and analyzes them"
    parser.print_help()
    sys.exit(0)


def plotting(energy_file1, energy_file2, snp_pos, snp_aa):
    energy_list1 = []
    energy_list2 = []
    pos_list = []
    energy_avg_1 = 0
    energy_avg_2 = 0
    line_count = 0
    contacts = ""
    with open(energy_file1) as inf:
        for line in inf:
            if "ENGY" in line:
                spl = line.split('\t')
                energy_list1.append(float(spl[5]))
                pos_list.append(int(spl[2]))
            line_count += 1
    if pos_list[0] > snp_pos or pos_list[-1] < snp_pos:
        print "ERROR SNP is NOT in 3D Strukture"
        print "Strukture range: ", pos_list[0], pos_list[-1]
        sys.exit()
    with open(energy_file2) as inf:
        for line in inf:
            if "ENGY" in line:
                spl = line.split('\t')
                energy_list2.append(float(spl[5]))
                if int(spl[2]) == snp_pos:
                    contacts = spl[-1].replace(" ", "")
                    current_aa = spl[3]
                    if Bio.SeqUtils.IUPACData.protein_letters_3to1[snp_aa] != current_aa:
                        print "ERROR: WRONG SNP! in energy profile: ", energy_file2
                        print "FOUND: ", current_aa, "expected: ", snp_aa
                        sys.exit()

    highlight = int(snp_pos) - pos_list[0]
    labels = []
    energy_profile_list_1 = []
    energy_profile_list_2 = []
    energy_diff = []
    maxval = max(k for k in energy_list1)

    for energy1, energy2, pos in zip(energy_list1, energy_list2, pos_list):
        labels.append(pos)
        energy_profile_list_1.append(energy1)
        energy_profile_list_2.append(energy2)
        energy_avg_1 += energy1
        energy_avg_2 += energy2
        energy_diff.append(energy1 - energy2)

    y_p = np.array(energy_profile_list_2)
    y_h = np.array(energy_profile_list_1)
    y_d = np.array(energy_diff)
    x_h = np.array(labels)
    diff = str((energy_avg_1 / line_count) - (energy_avg_2 / line_count))[0:6]

    plt.rcParams["figure.figsize"] = (45, 10)
    plt.axis([pos_list[0], pos_list[-1], -40, 15])
    energy_file_name1 = energy_file1.split("/")[-1]
    energy_file_name2 = energy_file2.split("/")[-1]
    plt.plot(x_h, y_p, 'r-', label=energy_file_name2)
    plt.plot(x_h, y_h, 'b-', label=energy_file_name1)
    plt.plot(x_h, y_d, 'g-', label="diff " + diff)
    # plt.plot(x_h[12], y_p[0], 'g*')
    plt.axvspan(x_h[highlight - 1], x_h[highlight + 1], color='orange', alpha=0.5)

    for contact, pos in zip(contacts, pos_list):
        if contact == "1":
            # print pos
            try:
                plt.axvspan(x_h[pos], x_h[pos], color='grey', alpha=0.5)
            except IndexError:
                print "OUT OF RANGE contact: "

    print energy_avg_1/line_count, energy_avg_2/line_count, diff
    outfile = "comp_plot45_" + str(energy_file_name1) + "_" + str(energy_file_name2)
    plt.xlabel("ResNo")
    plt.ylabel("Energy value")
    plt.title("Energy compairson")
    plt.legend()
    plt.savefig(outfile + ".pdf")
    plt.savefig(outfile + ".png")
    plt.close()

# ------------------------------------------------- main script ------------------------------------------------------ #


snp_pre = args.energy_profile_2.split("/")[-1].split(".ep2")[0].split("p.")[-1]
print snp_pre

snp_pos = int(re.findall('\d+', snp_pre)[0])
snp_aa = snp_pre[-3::1]

print "plotting: ", args.energy_profile_1, args.energy_profile_2, "pos:", snp_pos, "aa: ", snp_aa
plotting(args.energy_profile_1, args.energy_profile_2, snp_pos, snp_aa)

