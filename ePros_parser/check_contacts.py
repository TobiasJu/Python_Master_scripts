#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns
import collections
import timeit

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

# ---------------------------------------------- main script ---------------------------------------------------- #
start_time = timeit.default_timer()
contact_dict ={}
continue_counter = 0
print "starting..."
for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        print energy_file
        amino_contacts = {}
        amino_list = []
        with open(args.energy + "/" + energy_file, 'r') as energy_file_handle:
            counter = 0
            for line in energy_file_handle:
                if line.startswith('ENGY'):
                    amino = line.split("\t")[3]
                    contacts = line.split("\t")[6].replace(" ", "").rstrip()
                    #print "KONTAKTE: "
                    #print len(contacts)
                    insert_into_data_structure(counter, contacts, amino_contacts)
                    amino_list.append(amino)
                    counter += 1
            for a_count, contacts in amino_contacts.iteritems():
                contact_string = "".join(str(x) for x in contacts)
                a_check_couter = 0
                for contact in contact_string:
                    if contact == "1":
                        try:
                            check = amino_list[a_count]
                            check = amino_list[a_check_couter]
                        except:
                            continue_counter += 1
                            print "ERROR: out of bound exception!"
                            continue
                        #print counter, " ", a_check_couter
                        #print len(amino_list)
                        #print amino_list[a_count], " ", amino_list[a_check_couter]
                        insert_into_data_structure(amino_list[a_count], amino_list[a_check_couter], contact_dict)

                    a_check_couter += 1

print start_time
print "analysing and couting dict entries"
contact_count_dict = {}
for amino1, amino2_list in contact_dict.iteritems():
    print "counting dict: ", amino1
    print timeit.default_timer() - start_time
    a_count_dict = {i: amino2_list.count(i) for i in amino2_list}
    contact_dict[amino1] = a_count_dict

print contact_dict
print "sorting dict"
ordered_contact_dict = collections.OrderedDict(sorted(contact_dict.items()))

for key, value in ordered_contact_dict.iteritems():
    sys.stdout.write(str(key))
    sys.stdout.write(",")
    for key2, value2 in value.iteritems():
        sys.stdout.write(str(value2))
        sys.stdout.write(",")
    print ""

print "skipped ", continue_counter, " lines of EPs"

