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
import re
from pprint import pprint
import copy

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
        dict[key] = value
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

# ------------------------------------------------- main script ------------------------------------------------------ #
start_time = timeit.default_timer()
contact_count_dict = {'A': {}, 'C': {}, 'D': {}, 'E': {}, 'F': {}, 'G': {}, 'H': {}, 'I': {}, 'K': {}, 'L': {},
                      'M': {}, 'N': {}, 'P': {}, 'Q': {}, 'R': {}, 'S': {}, 'T': {}, 'U': {}, 'V': {}, 'W': {}, 'Y': {}}
sub_contact_count_dict = {'A': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'K': 0, 'L': 0,
                          'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'Y': 0}
for key, vale in contact_count_dict.iteritems():
    contact_count_dict[key] = copy.deepcopy(sub_contact_count_dict)

continue_counter = 0
print "starting..."
for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        print energy_file
        amino_contacts_dict = {}
        amino_dict_with_chains = {}
        amino_seq = ""
        id_list = []
        with open(args.energy + "/" + energy_file, 'r') as energy_file_handle:
            counter = 0
            chain = ""
            prev_chain = ""
            for line in energy_file_handle:
                if line.startswith('ENGY'):
                    chain = line.split("\t")[1]
                    if bool(re.search(r'\d', chain)):
                        continue
                    if prev_chain != "" and prev_chain != chain:
                        counter = 0
                        amino_dict_with_chains[prev_chain] = amino_seq
                        amino_seq = ""
                        #print "#################################################################- SET COUNTER = 0"
                        #print prev_chain
                    amino = line.split("\t")[3]
                    contacts = line.split("\t")[6].replace(" ", "").rstrip()
                    id = str(counter) + chain
                    id_list.append(id)
                    insert_into_data_structure(id, contacts, amino_contacts_dict)
                    amino_seq += amino
                    # WIESO IST JEDES 2. ELEMENT LEEEER??
                    counter += 1
                    prev_chain = chain
            # one last time for adding the last chain aa_seq to the dict, or the first if only one chain
            amino_dict_with_chains[prev_chain] = amino_seq

            # iterate over data and count
            for id in id_list:
                counter = int(re.split(r'(\d+)', id)[1])
                chain = re.split(r'(\d+)', id)[-1]
                contacts = amino_contacts_dict[id]
                if (len(contacts) != len(amino_seq)):
                    print "YOU FUCKED UP"
                    continue_counter += 1
                    continue
                amino_seq = amino_dict_with_chains[chain]
                amino_now = amino_seq[counter]
                contact_index = 0
                for contact, amino_in_loop in zip(contacts, amino_seq):
                    # count all contacts except self contacts
                    if contact == "1" and contact_index != counter:
                        nix = 0
                        # print amino_now, amino_in_loop
                        contact_count_dict[amino_now][amino_in_loop] += 1
                    contact_index += 1

print "print DICT: "
# pprint(contact_count_dict)

print timeit.default_timer() - start_time

for key, value in contact_count_dict.iteritems():
    print key
    print contact_count_dict[key]

for key, value in contact_count_dict.iteritems():
    for key2, value2 in contact_count_dict[key].iteritems():
        sys.stdout.write(str(value2) + ",")
    print ""



print "skipped ", continue_counter, " lines of EPs"

