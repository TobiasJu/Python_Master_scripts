#!/usr/bin/env python
# -*- coding: utf-8 -*-

from epros_file import epros_file
import os
import sys
import argparse
from Bio import AlignIO
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import time
import random
from random import randint
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

amino_acids = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
               'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
               'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
               'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))

# random permute ep sequence 100 times and align it to the pfam sequence
def align_with_permute_ep_seq(pfam_seq, ep_seq):
    score_list = []
    ep_list = list(ep_seq)
    for step in range(100):
        random_triple_letter = random.choice(amino_acids.keys())
        # print amino_acids[random_triple_letter]
        ep_list[randint(0, (len(ep_list)-1))] = amino_acids[random_triple_letter]
        ep_seq = ''.join(ep_list)
        score_list.append(pairwise2.align.globalxx(pfam_seq, ep_seq, score_only=1))
    print score_list
    x_mean = numpy.mean(score_list)
    return x_mean

def calc_seq_identity(seq1, seq2):
    alignment = pairwise2.align.globalxx(seq1, seq2)
    pos = 0
    max_score = 0
    max_legth = 0
    counter = 0
    # take the first alignment with the highest score and max length possible
    for a in alignment:
        al1, al2, score, begin, end = a
        length = end - begin
        if score >= max_score and length > max_legth:
            max_score = score
            max_legth = length
            pos = counter
        counter += 1
    print max_score
    print max_legth
    print pos
    # print alignment[pos]
    print alignment[pos][0], "\n", alignment[pos][1]
    matches = sum(aa1 == aa2 for aa1, aa2 in zip(alignment[pos][0], alignment[pos][1]))
    gap_counter = sum(aa1 == "-" and aa2 == "-" for aa1, aa2 in zip(alignment[pos][0], alignment[pos][1]))
    seq_identity = 100.0 * matches / (len(alignment[pos][0])-gap_counter)
    # pct_identity = 100.0 * matches / (len(alignment[pos][0]))
    print "Identity:", seq_identity
    return seq_identity

def map_ep_to_pfam(energy_object, pfam_file):
    print "mapping"
    print energy_object
    print pfam_file
    # to do

# ------------------------------- main script -------------------------------- #

print "starting..."
start_time = time.time()
energy_dir = args.energy
pfam_dir = args.directory
pdbmap = args.pdbmap
pdbmap_dict = {}

# load all pfam ids from the pdbmap file into a dict
with open(pdbmap, 'r') as pdbmap_file:
    for line in pdbmap_file:
        line_array = line.split(";\t")
        insert_into_data_structure(line_array[3], line_array[0], pdbmap_dict)

# align Pfam sequence with EP sequence
for dirpath, dir, files in os.walk(top=args.directory):
    for file in files:
        energy_list = []
        pfam_accesion = file.split(".")[0]
        print pfam_accesion
        pfam_alignment = AlignIO.read(open(dirpath + file), "stockholm")
        print("Alignment length %i" % pfam_alignment.get_alignment_length())

        # open wanted energy files and create Energy Objects
        for pdb_id in pdbmap_dict[pfam_accesion]:
            file = os.path.join(energy_dir + pdb_id + ".ep2")
            if os.path.isfile(file):
                print "creating energy object " + pdb_id + " for pfam: " + pfam_accesion
                energy_list.append(epros_file.create_energyprofile(file))

        # align each pfam sequence
        for record in pfam_alignment:
            # print(record.id + " " + record.seq)
            # with each energy sequence
            for entry in energy_list:
                epros_ss = str(''.join(entry._epros_file__res))
                pfam_energy_alignment = pairwise2.align.globalxx(record.seq, epros_ss)
                x_row_max = 0
                x_row = (line[2] =< x_row_max for line in pfam_energy_alignment)  # pairwise2.align.globalxx(record.seq, epros_ss, score_only=1)  # score_only=1
                print "X_ROW: ", x_row
                x_opt = pairwise2.align.globalxx(record.seq, record.seq, score_only=1)
                print "X_OPT: ", x_opt
                x_mean = align_with_permute_ep_seq(record.seq, epros_ss)
                print "X_MEAN: ", x_mean
                x_real = -1 * numpy.log10((x_row - x_mean)/(x_opt - x_mean))
                print "X_REAL: ", x_real
                seq_identity = calc_seq_identity(record.seq, epros_ss)
                print "SEQ_IDENTITY: ", seq_identity
                x_pred = -1.0061 * numpy.log(seq_identity/100) + 4.7189  # seq identity in % or as 0.xx???
                print "X_PRED: ", x_pred
                x_z = (x_real - x_pred) / 0.03858
                print "X_Z: ", x_z
                if x_z >= 1.65:
                    map_ep_to_pfam(entry, file)
                print "next alignment"

print str(time.time() - start_time)
print "Done"

