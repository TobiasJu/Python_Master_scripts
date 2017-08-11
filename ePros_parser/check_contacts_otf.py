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
contact_dict ={}
continue_counter = 0
print "starting..."
for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        print energy_file
        amino_contacts = {}
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
                    if prev_chain != "" and prev_chain != chain:
                        counter = 0
                        amino_dict_with_chains[prev_chain] = amino_seq
                        amino_seq = ""
                        print "################################################################# SET COUNTER = 0"
                        print prev_chain
                    amino = line.split("\t")[3]
                    contacts = line.split("\t")[6].replace(" ", "").rstrip()
                    id = str(counter) + chain
                    id_list.append(id)
                    insert_into_data_structure(id, contacts, amino_contacts)
                    amino_seq += amino
                    # WIESO IST JEDES 2. ELEMENT LEEEER??
                    counter += 1
                    prev_chain = chain
                # one last time for adding the last chain aa to the dict
                amino_dict_with_chains[prev_chain] = amino_seq

            # iterate over data and count
            for id in id_list:
                counter = re.split(r'(\d+)', id)[1]
                chain = re.split(r'(\d+)', id)[-1]
                print counter
                print chain
                contacts = amino_contacts[id]
                #if (len(contacts) == len(amino_dict_with_chains[chain])):
                #    print "alles supi"
                #else:
                #    print "FUCKED UP"
                amino_pos_counter = 0
                for contact, amino in zip(contacts, amino_dict_with_chains[chain]):

                    if contact == "1":
                        print amino, amino_dict_with_chains[chain][amino_pos_counter]
                    amino_pos_counter += 1
                    
#                for amino in amino_dict_with_chains[chain]:
#                    print amino
                    # calculate contacts ...

#                print contacts
                sys.exit()



            print energy_file
            # print amino_list
            sys.exit()

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

