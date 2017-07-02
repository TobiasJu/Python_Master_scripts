#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import subprocess
import os
from os.path import isfile
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
from scipy.stats import kendalltau
# sns.set(style="ticks")
import math
import pandas as pd
import seaborn as sns

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory of the Pfam family files")
# parser.add_argument("-e", "--energy", help="input energy profile directory")
parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and analyzes them, and plots a ramachandran plot for each fam."
    parser.print_help()
    sys.exit(0)

# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_dict(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))

# ------------------------------------------ main script ------------------------------------------------------------- #

currentFile = __file__  # May be 'my_script', or './my_script' or
                        # '/home/user/test/my_script.py' depending on exactly how
                        # the script was run/loaded.
realPath = os.path.realpath(currentFile)  # /home/user/test/my_script.py
dirPath = os.path.dirname(realPath)  # /home/user/test
dirName = os.path.basename(dirPath) # test

#pdb_file = "/mnt/d/100d.pdb"


pdbmap_dict = {}
# load all pfam ids from the pdbmap file into a dict
with open(args.pdbmap, 'r') as pdbmap_file:
    for line in pdbmap_file:
        line_array = line.split(";\t")
        pdb_id = line_array[0]
        pdb_pos = line_array[5].strip(";\n")
        insert_into_dict(line_array[3], pdb_id + "." + pdb_pos, pdbmap_dict)
#zahl = 0
for pfam, pdb_ids in pdbmap_dict.iteritems():
#    zahl += 1
#    if zahl == 1:
#        continue
    pos_list = []
    psi_list = []
    phi_list = []
    print pfam
    pdb_file_list = []
    pdb_ids_set = list(set(pdb_ids))
    for line in pdb_ids_set:
        line_array = line.split(".")
        pdb_id = "pdb" + line_array[0]
        pdb_folder = pdb_id[4:6]
        #print pdb_id
        #print pdb_folder
        #sys.exit(0)
        pdb_file = "/mnt/g/Master/pdb/" + pdb_folder.lower() + "/" + pdb_id.lower() + ".ent"
        pdb_file_list.append(pdb_file)
    counter = 0

    for pdb_file in pdb_file_list:
        counter += 1
        print counter, " / " ,len(pdb_file_list)

        if isfile(pdb_file):
            call = 'java -jar ' + dirPath + '/ramachan.jar' + ' -i ' + pdb_file
            process = subprocess.Popen([call],shell=True, stdout=subprocess.PIPE)
            out, err = process.communicate()
            split_out = out.splitlines()
            split_out.pop(0)

            if len(split_out) == 0:
                continue

            for line in split_out:
                line_array = line.split(";")
                pos_list.append(int(line_array[0]))
                psi_list.append(float(line_array[1]))
                phi_list.append(float(line_array[2]))
        else:
            print pdb_file, " not found!"
        print len(psi_list)


    #convert to numpy array
    psi_list_numpy = np.array(psi_list)
    phi_list_numpy = np.array(phi_list)
    # give the axis a name
    psi = pd.Series(psi_list_numpy, name='psi')
    phi = pd.Series(phi_list_numpy, name='phi')

    # Show the joint distribution using kernel density estimation
    sns_plot = sns.jointplot(phi, psi, kind="kde", size=12, space=0, xlim=(-190, 190), ylim=(-190, 190))

    # sns_plot = (sns.jointplot(phi, psi, size=12, space=0, xlim=(-190, 190), ylim=(-190, 190)).plot_joint(sns.kdeplot, zorder=0, n_levels=6))
    # sns_plot = sns.jointplot(psi_list_numpy, phi_list_numpy, kind="hex", color="#4CB391")  # stat_func=kendalltau

    print "plotting: ", pfam
    sns_plot.savefig("Ramachandranplot_kde_new/ramachandranplot_" + pfam + ".png")
    plt.clf()


