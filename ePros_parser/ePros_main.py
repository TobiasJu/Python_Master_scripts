#!/usr/bin/env python
# -*- coding: utf-8 -*-

from epros_file import epros_file
import os
import sys
import argparse
from Bio import AlignIO
from Bio import pairwise2
import time
from pprint import pprint

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory")
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
time_start = time.time()
print time_start
energy_dir = args.energy
energy_list = []
pdbmap = args.pdbmap
pdbmap_dict = {}


def insertIntoDataStructure(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))


# load all pfam ids from the pdbmap file into a list
with open(pdbmap, 'r') as pdbmap_file:
    for line in pdbmap_file:
        line_array = line.split(";\t")
        insertIntoDataStructure(line_array[3], line_array[0], pdbmap_dict)
        # pdbmap_dict[line_array[3]] = line_array[0]
        # pdbmap_dict["chain"] = line_array[1]
        # pdbmap_dict["name"] = line_array[2]
        # pdbmap_dict[line_array[3]] = line_array[3]
        # pdbmap_dict["UniProtKB_id"] = line_array[4]
        # pdbmap_dict["sequence_pos"] = line_array[5]

#print pdbmap_dict
counter = 0
# open all energy files and create Energy Objects
for dirpath, dir, files in os.walk(top=energy_dir):
    for file in files:
        line_count = 0
        name = ""
        type = ""
        head = []
        chain = []
        resno = []
        res = []
        ss = []
        energy = []
        with open(energy_dir + file, 'r') as energy_file:
            for line in energy_file:
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
                # else:
                #    print "found REMK line in file: " + file
                line_count += 1
            counter += 1
            if counter > 10000:
                break
            energy_list.append(epros_file(name, type, head, chain, resno, res, ss, energy))
print str(time.time() - time_start)

for entry in energy_list:
    print entry._epros_file__name
    print entry._epros_file__type
    print entry._epros_file__head
    print entry._epros_file__chain
    print entry._epros_file__resno
    print entry._epros_file__res
    print entry._epros_file__ss
    print entry._epros_file__energy
    print "done"
    sys.exit(0)

# align Pfam sequence with EP sequence
for dirpath1, dir1, files1 in os.walk(top=args.directory):
    for file1 in files1:
        print file1

pfam_alignment = AlignIO.read(open("Pfam 31.0/globular_cut/2C_adapt.txt"), "stockholm")
print("Alignment length %i" % pfam_alignment.get_alignment_length())
for record in pfam_alignment:
    print(record.seq + " " + record.id)
    for entry in energy_list:
        epros_ss = ''.join(entry._epros_file__ss)
        alignments = pairwise2.align.globalxx(record.seq, str(epros_ss))
        print alignments
        print ""
