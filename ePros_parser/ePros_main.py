#!/usr/bin/env python
# -*- coding: utf-8 -*-

from epros_file import epros_file
import os
import sys
import argparse
from Bio import AlignIO
from Bio import pairwise2
import time

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
energy_list = []
pdbmap = args.pdbmap
pdbmap_dict = {}

# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))


# creates a epros_file object
def create_energyprofile(energy_file, dirpath):
    line_count = 0
    name = ""
    type = ""
    head = []
    chain = []
    resno = []
    res = []
    ss = []
    energy = []
    with open(dirpath + energy_file, 'r') as energy_file_handle:  # with open(energy_dir + file, 'r') as energy_file:
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
                    head.append(line_array[0])
                    chain.append(line_array[1])
                    resno.append(line_array[2])
                    res.append(line_array[3])
                    ss.append(line_array[4])
                    energy.append(line_array[5].rstrip())
            line_count += 1
    return epros_file(name, type, head, chain, resno, res, ss, energy)

# load all pfam ids from the pdbmap file into a list
with open(pdbmap, 'r') as pdbmap_file:
    for line in pdbmap_file:
        line_array = line.split(";\t")
        insert_into_data_structure(line_array[3], line_array[0], pdbmap_dict)

# open all energy files and create Energy Objects
for dirpath, dir, files in os.walk(top=energy_dir):
    for file in files:
        energy_list.append(create_energyprofile(file, dirpath))
print str(time.time() - start_time)

# debug
#for entry in energy_list:
#    print entry.print_all()
#    print "done"
#    sys.exit(0)

# align Pfam sequence with EP sequence
for dirpath1, dir1, files1 in os.walk(top=args.directory):
    for file1 in files1:
        print dirpath1 + file1
        pfam_alignment = AlignIO.read(open(dirpath1 + file1), "stockholm")
        print("Alignment length %i" % pfam_alignment.get_alignment_length())
        for record in pfam_alignment:
            # print(record.seq + " " + record.id)
            for entry in energy_list:
                epros_ss = ''.join(entry._epros_file__res)
                alignments = pairwise2.align.globalxx(record.seq, str(epros_ss), score_only)
                print alignments
                print "next"



