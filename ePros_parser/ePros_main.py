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
parser.add_argument("-o", "--output", help="output directory for mapped files")
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
        ep_list[randint(0, (len(ep_list) - 1))] = amino_acids[random_triple_letter]
        ep_seq = ''.join(ep_list)
        score_list.append(pairwise2.align.globalxx(pfam_seq, ep_seq, score_only=1))
    print score_list
    x_mean = numpy.mean(score_list)
    return x_mean


def calc_seq_identity(alignment):
    pos = 0
    max_score = 0
    min_legth = 0
    counter = 0
    # take the first alignment with the highest score and min length possible
    for a in alignment:
        al1, al2, score, begin, end = a
        length = end - begin
        if score >= max_score and length < min_legth:
            max_score = score
            min_legth = length
            pos = counter
        counter += 1
    print alignment[pos][0], "\n", alignment[pos][1]
    matches = sum(aa1 == aa2 for aa1, aa2 in zip(alignment[pos][0], alignment[pos][1]))
    # gap_counter = sum(aa1 == "-" and aa2 == "-" for aa1, aa2 in zip(alignment[pos][0], alignment[pos][1]))
    seq_identity = 100.0 * matches / (len(alignment[pos][0]))
    return seq_identity, pos


def map_ep_to_pfam(alignment, max_pos, energy_object, pfam_seq, pfam_acc):
    print "mapping"
    destination = dest_folder + pfam_acc + "_" + energy_object._epros_file__name + ".txt"
    print "writing to: ", destination
    #print "pfam: ", pfam_seq
    #print alignment[max_pos][0]
    #print "next"
    #print alignment[max_pos][1]
    # print(format_alignment(*alignment[max_pos]))
    res = str(''.join(energy_entry._epros_file__res))
    # print res
    ss = str(''.join(energy_entry._epros_file__ss))
    # print ss
    pos_counter = 0
    pos_array = []
    for aa in alignment[max_pos][1]:
        #print aa
        if aa == energy_entry._epros_file__res[pos_counter]:
            pos_array.append(pos_counter)
            pos_counter += 1
            # print aa
    # print pos_array
    # print energy_entry._epros_file__energy
    energy_seq = energy_entry._epros_file__energy
    if os.path.isfile(destination):
        print "APPEND!"
        with open(destination, "a") as target:
            target.write("\n")
            target.write(">ID:\t" + pfam_seq.id + "\n")
            target.write(">SEQ:\t" + alignment[max_pos][0] + "\n")
            target.write(">QUAN:\t" + "to do..." + "\n")
            target.write("SSE:\t" + str(''.join(energy_entry._epros_file__ss)) + "\n")
            target.write(">EVAL:\t" + str(' '.join(energy_entry._epros_file__energy)) + "\n")
    else:
        print "CREATING NEW FILE!"
        with open(destination, 'w') as target:
            target.write("\n")
            target.write(">ID:\t" + pfam_seq.id + "\n")
            target.write(">SEQ:\t" + alignment[max_pos][0] + "\n")
            target.write(">QUAN:\t" + "to do..." + "\n")
            target.write("SSE:\t" + str(''.join(energy_entry._epros_file__ss)) + "\n")
            target.write(">EVAL:\t" + str(' '.join(energy_entry._epros_file__energy)) + "\n")



    # output should look like this
    '''
    >ID:    FA9_HUMAN/97-127:1IXA-A/51-81
    >SEQ:   ----------CESN-----PCLNGGSCK-
    >QUAN:  2341.....214324112-
    >SSE:   cccc*****cccEEEEccc
    >EVAL:  -12.32 -12.1 -2.12 -0.12 -7.51...
    '''

# ---------------------------------------- main script ------------------------------------------------- #

# calc_seq_identity("DYLLPDI", "DYLLPDINHAIDII")
# sys.exit(0)

print "starting..."
start_time = time.time()
energy_dir = args.energy
pfam_dir = args.directory
pdbmap = args.pdbmap
pdbmap_dict = {}
if not args.output:
    dest_folder = "mapped/"
else:
    dest_folder = args.output
try:
    os.makedirs(dest_folder)
except:
    print "Folder " + dest_folder + " already exist!"

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

        # open wanted energy files and create Energy Objects
        pdb_id_list = pdbmap_dict[pfam_accesion]
        # no double entries
        pdb_id_list_set = list(set(pdb_id_list)) 
        for pdb_id in pdb_id_list_set:
            file = os.path.join(energy_dir + pdb_id + ".ep2")
            if os.path.isfile(file):
                print "creating energy object " + pdb_id + " for pfam: " + pfam_accesion
                energy_list.append(epros_file.create_energyprofile(file))

        # align each pfam sequence
        for pfam_record in pfam_alignment:
            # with each energy sequence
            for energy_entry in energy_list:
                print "alignment", energy_entry._epros_file__name, "with", pfam_accesion, "id", pfam_record.id
                epros_res = str(''.join(energy_entry._epros_file__res))
                pfam_energy_alignment = pairwise2.align.globalxx(pfam_record.seq, epros_res)
                x_row = 0
                for a in pfam_energy_alignment:
                    if a[2] > x_row:
                        x_row = a[2]
                print "X_ROW: ", x_row
                x_opt = pairwise2.align.globalxx(pfam_record.seq, pfam_record.seq, score_only=1)
                print "X_OPT: ", x_opt
                x_mean = align_with_permute_ep_seq(pfam_record.seq, epros_res)
                print "X_MEAN: ", x_mean
                x_real = -1 * numpy.log10((x_row - x_mean) / (x_opt - x_mean))
                print "X_REAL: ", x_real
                seq_identity, max_pos = calc_seq_identity(pfam_energy_alignment)
                print "SEQ_IDENTITY: ", seq_identity
                x_pred = -1.006 * numpy.log(seq_identity) + 4.7189  # seq identity in % or as 0.xx???
                print "X_PRED: ", x_pred
                x_z = (x_real - x_pred) / 0.03858
                print "X_Z: ", x_z
                if x_z >= 1.60:
                    map_ep_to_pfam(pfam_energy_alignment, max_pos, energy_entry, pfam_record, pfam_accesion)

print str(time.time() - start_time)
print "Done"
