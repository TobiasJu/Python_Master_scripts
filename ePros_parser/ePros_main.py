#!/usr/bin/env python
# -*- coding: utf-8 -*-

from epros_file import epros_file
import os
import sys
import argparse
from Bio import AlignIO
from Bio import pairwise2
import time
import random
import numpy

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input pfam directory")
parser.add_argument("-e", "--energy", help="input energy profile directory")
parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "This script maps Energy Profiles to Alignment Data"
    print "Please enter a input directory"
    parser.print_help()
    sys.exit(0)

if not args.directory:
    print "This script maps Energy Profiles to alignment data"
    print "Please enter a input directory for the Pfam data"
    parser.print_help()
    sys.exit(0)

if not args.energy:
    print "This script maps Energy Profiles to alignment data"
    print "Please enter a input directory for the engery data"
    parser.print_help()
    sys.exit(0)

print "starting..."
start_time = time.time()
energy_dir = args.energy
pfam_dir = args.directory
pdbmap = args.pdbmap
pdbmap_dict = {}

# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))


# creates a epros_file object
def create_energyprofile(energy_file):
    line_count = 0
    name = ""
    type = ""
    head = []
    chain = []
    resno = []
    res = []
    ss = []
    energy = []
    with open(energy_file, 'r') as energy_file_handle:  # with open(energy_dir + file, 'r') as energy_file:
        for line in energy_file_handle:
            line_array = line.split("\t")
            if not "REMK" in line_array:
                if line_count == 0:
                    name = line_array[1]
                elif line_count == 1:
                    type = line_array[1]
                elif line_count == 2:
                    header = line_array
                else:
                    # just extract the A Chain
                    if line_array[1] == "B":
                        break
                    head.append(line_array[0])
                    chain.append(line_array[1])
                    resno.append(line_array[2])
                    res.append(line_array[3])
                    ss.append(line_array[4])
                    energy.append(line_array[5].rstrip())
            line_count += 1
    return epros_file(name, type, head, chain, resno, res, ss, energy)

# random permute ep sequence 100 times and align it to the pfam sequence
def align_with_permute_ep_seq(pfam_seq, ep_seq):
    score_list = []
    ep_list = list(ep_seq)
    for step in range(100):
        random.shuffle(ep_list)
        ep_seq = ''.join(ep_list)
        score_list.append(pairwise2.align.globalxx(pfam_seq, ep_seq, score_only=1))
    print score_list
    x_mean = numpy.mean(score_list)
    return x_mean

# ------------------------------- main script -------------------------------- #

# load all pfam ids from the pdbmap file into a dict
with open(pdbmap, 'r') as pdbmap_file:
    for line in pdbmap_file:
        line_array = line.split(";\t")
        insert_into_data_structure(line_array[3], line_array[0], pdbmap_dict)

# align Pfam sequence with EP sequence
for dirpath1, dir1, files1 in os.walk(top=args.directory):
    for file1 in files1:
        energy_list = []
        pfam_accesion = file1.split(".")[0]
        print pfam_accesion
        pfam_alignment = AlignIO.read(open(dirpath1 + file1), "stockholm")
        print("Alignment length %i" % pfam_alignment.get_alignment_length())

        # open wanted energy files and create Energy Objects
        for pdb_id in pdbmap_dict[pfam_accesion]:
            file = os.path.join(energy_dir + pdb_id + ".ep2")
            if os.path.isfile(file):
                print "creating energy object " + pdb_id + " for pfam: " + pfam_accesion
                energy_list.append(create_energyprofile(file))

        # align each pfam sequence
        for record in pfam_alignment:
            # print(record.id + " " + record.seq)
            # with each energy sequence
            for entry in energy_list:
                epros_ss = str(''.join(entry._epros_file__res))
                x_row = pairwise2.align.globalxx(record.seq, epros_ss, score_only=1)  # score_only=1
                print "X_ROW: ", x_row
                x_opt = pairwise2.align.globalxx(record.seq, record.seq, score_only=1)
                print "X_OPT: ", x_opt
                x_mean = align_with_permute_ep_seq(record.seq, epros_ss)
                print "X_MEAN: ", x_mean
                x_real = -1 * numpy.log((x_row - x_mean)/(x_opt - x_mean))
                print "X_REAL: ", x_real

                print "next alignment"

print str(time.time() - start_time)
print "Done"

