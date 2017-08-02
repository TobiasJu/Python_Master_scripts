#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
plt.switch_backend('agg')
# from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pdb", help="PDB directory with PDB files, with subfolder structure")
# subfolders are like 00, 0g, 0m, 01, 1a, 1..
parser.add_argument("-e", "--energy", help="input energy profile directory")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and adds aa contact profiles to them"
    parser.print_help()
    sys.exit(0)

# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not value == 0:
        if not key in dict:
            dict[key] = (value)
        else:
            dict[key].append((value))

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

# ---------------------------------------- main script ------------------------------------------ #

counter = 0
print "starting..."
for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        line_count = 0
        counter += 1
        pre_pdb_id = "pdb" + energy_file.split(".")[0]
        pdb_id = pre_pdb_id.split("-")[0]
        print energy_file
        out_name = energy_file.split(".")[0]  #.split("-")[0]
        pdb_folder = pdb_id[4:6]
        pdb_file = "/mnt/g/Master/pdb/" + pdb_folder.lower() + "/" + pdb_id.lower() + ".ent"
        # print pdb_folder
        print pdb_file
        xlist = []
        ylist = []
        zlist = []
        poslist = []
        pre_aa_count = ""
        with open(pdb_file, 'r') as pdb_file_handle:
            for line in pdb_file_handle:
                if line.startswith('ATOM'):
                    # see for more info: http://deposit.rcsb.org/adit/docs/pdb_atom_format.html
                    atom = line[0:5]
                    pos = line[6:10].replace(" ", "")
                    a_type = line[12:15].replace(" ", "")

                    aa = line[17:20].replace(" ", "")
                    chain = line[21].replace(" ", "")
                    aa_count = line[23:26].replace(" ", "")
                    alternate_ca = line[26:27].replace(" ", "")
                    oc_x = line[30:37].replace(" ", "")
                    oc_y = line[38:45].replace(" ", "")
                    oc_z = line[46:53].replace(" ", "")
                    # occupacy = line[54:59].replace(" ", "")
                    #temp = line[60:65]
                    #lstring = line[72:76]
                    #lstirng = line[76:77]
                    #lstirng = line[78:79]
                    #if not alternate_ca == "":

                    if a_type == "CA" and pre_aa_count != aa_count:
                        # print pre_aa_count, aa_count
                        if pre_aa_count != aa_count:
                            xlist.append(float(oc_x))
                            ylist.append(float(oc_y))
                            zlist.append(float(oc_z))
                            poslist.append(int(aa_count))
                            # print line.rstrip()
                            #print "atom:", atom, " pos:", pos, " type:", a_type, " aa:", aa, " chain:", chain, " aa_count:", aa_count, " oc_x:", oc_x, " oc_y:", oc_y, " oc_z:", oc_z
                        pre_aa_count = aa_count
                elif line.startswith('TER'):
                    print "break!"
                    break
        #plot_scatter(x, y, z, name)
        contact_dict = {}
        #contact_counter = 0
        print len(xlist)
        #print len(poslist)

        for x, y, z, pos in itertools.izip(xlist, ylist, zlist, poslist):
            contact_list = []
            #contact_counter += 1
            for xx, yy, zz in itertools.izip(xlist, ylist, zlist):
                if x-4 < xx < x+4 and y-4 < yy < y+4 and z-4 < zz < z+4:
                    # print x, xx, y, yy, z, zz
                    contact_list.append("1")
                else:
                    contact_list.append("0")
            # print contact_list
            # print pos
            insert_into_data_structure(pos, contact_list, contact_dict)
        # print contact_dict
        if counter % 10000 == 0:
            print energy_file
            # break
        if energy_file.endswith(".ep2"):
            target = open(out_name + "_with_contacts.ep2", 'w')


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
                            aa_number = int(line_array[2])
                            # print aa_number
                            print contact_dict[aa_number]
                            #print type(" ".join(contact_dict[aa_number]))
                            #print " ".join(contact_dict[aa_number])
                            target.write("\t" + " ".join(contact_dict[aa_number]) + "\n")
                    line_count += 1
            target.close()
        counter += 1








