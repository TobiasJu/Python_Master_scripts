#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
plt.switch_backend('agg')


# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pdb", help="PDB directory with PDB files, with subfolder structure: "
                                        "subfolders are like 00, 0g, 0m, 01, 1a, 1..")
parser.add_argument("-e", "--energy", help="input energy profile directory (will iterate over all files)")
parser.add_argument("-f", "--energy_file", help="input energy profile file (run just for this file)")
parser.add_argument("-o", "--out", help="output energy profile directory, for EPs with contacts")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and adds aa contact profiles to them"
    parser.print_help()
    sys.exit(0)

if args.out:
    output_folder = args.out + "/"
else:
    output_folder = "ep_with_contacts" + "/"
try:
    os.makedirs(output_folder)
except:
    print output_folder, " already exists!"
# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not value == 0:
        if not key in dict:
            dict[key] = (value)
        else:
            # there should never be the else case
            #dict[key].append((value))
            print "ERROR!!!! else: ", key

def plot_scatter(x ,y ,z , name):
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(figsize=(5, 5))
    ax = fig.gca(projection='3d')
    np_x = np.array(x)
    np_y = np.array(y)
    np_z = np.array(z)
    ax.scatter(np_x, np_y, np_z, label='Amino Acids')
    ax.legend()
    plt.savefig(name + '_scatter.pdf')

def check_if_file_already_computed(energy_file):
    if (os.path.isfile(output_folder + energy_file)):
        print "already computed", energy_file
        return True
    else:
        return False

def check_if_pdb_file_exists(pdb_file):
    if not (os.path.isfile(pdb_file)):
        print "there is no file: ", pdb_file
        missing_list.append(pdb_file)
        return False
    else:
        return True

def get_pdb_file(energy_file):
    pre_pdb_id = "pdb" + energy_file.split(".")[0]
    pdb_id = pre_pdb_id.split("-")[0]
    if len(pre_pdb_id.split("-")) == 2:
        specific_chain = pre_pdb_id.split("-")[1]
    else:
        specific_chain = "all"
    out_name = energy_file.split(".")[0]
    pdb_folder = pdb_id[4:6]
    if args.pdb:
        pdb_path = os.getcwd() + "/" + args.pdb
    else:
        print "trying default path: "
        pdb_path = "/mnt/h/Master/pdb/"
    pdb_file1 = pdb_path + pdb_folder.lower() + "/" + pdb_id.lower() + ".ent"
    print energy_file
    print pdb_file
    return pdb_file1, specific_chain, out_name

def calc_energy_file(pdb_file, specific_chain, out_name):
    line_count = 0
    xlist = []
    ylist = []
    zlist = []
    poslist = []
    pre_aa_count = ""
    if specific_chain != "all":
        # just the specific Chain
        with open(pdb_file, 'r') as pdb_file_handle:
            for line in pdb_file_handle:
                if line.startswith('ATOM'):
                    # see for more info: http://deposit.rcsb.org/adit/docs/pdb_atom_format.html
                    chain = line[21].replace(" ", "")
                    if chain != specific_chain:
                        # skip this chain
                        continue
                    atom = line[0:5]
                    pos = line[6:10].replace(" ", "")
                    a_type = line[12:15].replace(" ", "")
                    aa = line[17:20].replace(" ", "")
                    aa_count = line[22:26].replace(" ", "")
                    alternate_ca = line[26:27].replace(" ", "")
                    oc_x = line[30:37].replace(" ", "")
                    oc_y = line[38:45].replace(" ", "")
                    oc_z = line[46:53].replace(" ", "")
                    if a_type == "CA" and pre_aa_count != aa_count:
                        # print pre_aa_count, aa_count
                        if pre_aa_count != aa_count:
                            xlist.append(float(oc_x))
                            ylist.append(float(oc_y))
                            zlist.append(float(oc_z))
                            poslist.append(aa_count + chain)
                        pre_aa_count = aa_count
                elif line.startswith('ENDMDL'):
                    break
    else:
        # all chains
        with open(pdb_file, 'r') as pdb_file_handle:
            for line in pdb_file_handle:
                if line.startswith('ATOM'):
                    chain = line[21].replace(" ", "")
                    atom = line[0:5]
                    absolut_pos = line[6:10].replace(" ", "")
                    a_type = line[12:15].replace(" ", "")
                    aa = line[17:20].replace(" ", "")
                    aa_count = line[22:26].replace(" ", "")
                    alternate_ca = line[26:27].replace(" ", "")
                    oc_x = line[30:37].replace(" ", "")
                    oc_y = line[38:45].replace(" ", "")
                    oc_z = line[46:53].replace(" ", "")

                    if a_type == "CA" and pre_aa_count != aa_count:
                        # print pre_aa_count, aa_count
                        if pre_aa_count != aa_count:
                            xlist.append(float(oc_x))
                            ylist.append(float(oc_y))
                            zlist.append(float(oc_z))
                            poslist.append(aa_count + chain)
                        pre_aa_count = aa_count
                elif line.startswith('ENDMDL'):
                    break

    contact_dict = {}
    # check distances to other atoms in the specific chain
    for x1, y1, z1, pos1 in itertools.izip(xlist, ylist, zlist, poslist):
        contact_list = []
        chain1 = re.split(r'(\d+)', pos1)[2]
        # print pos1
        for x2, y2, z2, pos2 in itertools.izip(xlist, ylist, zlist, poslist):
            chain2 = re.split(r'(\d+)', pos2)[2]
            if chain1 != chain2:
                continue
            dist = np.sqrt(np.square(x1 - x2) + np.square(y1 - y2) + np.square(y1 - y2))
            if dist < 8:
                # if x1-4 < x2 < x1+4 and y1-4 < y2 < y1+4 and z1-4 < z2 < z1+4:
                # print x1, x2, y1, y2, z1, z2, dist
                contact_list.append("1")
            else:
                contact_list.append("0")
        insert_into_data_structure(pos1, contact_list, contact_dict)

    if counter % 10000 == 0:
        print energy_file
        # break
    if energy_file.endswith(".ep2"):
        target = open(output_folder + out_name + ".ep2", 'w')
        # print "writing to: " + output_folder + "/" + out_name + ".ep2"


        with open(dirpath + energy_file, 'r') as energy_file_handle:
            for line in energy_file_handle:
                # print line
                line_array = line.split("\t")
                target.write(line.rstrip())
                if not "REMK" in line_array:
                    if line_count == 0:
                        name = line_array[1]
                        target.write("\n")
                    elif line_count == 1:
                        aa_type = line_array[1]
                        target.write("\n")
                    elif line_count == 2:
                        header = line_array
                        target.write("\n")
                    else:
                        aa_number = line_array[2]
                        energy_chain = line_array[1]
                        try:
                            export_string = " ".join(contact_dict[aa_number + energy_chain])
                        except (ValueError, IndexError, KeyError):
                            export_string = "-"
                        target.write("\t" + export_string + "\n")
                line_count += 1
        target.close()

# ---------------------------------------- main script ------------------------------------------ #

counter = 0
missing_list = []
print "starting..."
if args.energy:
    print "Whole dir"
    for dirpath, dir, files in os.walk(top=args.energy):
        for energy_file in files:
            if check_if_file_already_computed(energy_file):
                continue
            pdb_file, specific_chain, out_name = get_pdb_file(energy_file)
            if not check_if_pdb_file_exists(pdb_file):
                continue
            calc_energy_file(pdb_file, specific_chain, out_name)
        counter += 1

elif args.energy_file:
    print "just one file"
    energy_file = args.energy_file
    pdb_file, specific_chain, out_name = get_pdb_file(energy_file)
    calc_energy_file(pdb_file, specific_chain, out_name)


print "FINISH!"
print "Found ", len(missing_list), " missing pdb files"
print missing_list





