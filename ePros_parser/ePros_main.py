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
import math

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

quartile = [-118.303418308, -21.3328509911, -9.26231037705, -3.33429827376, 11.5566432042]


# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_dict(key, value, dict):
    if not key in dict:
        dict[key] = [(value)]
    else:
        dict[key].append((value))


# random permute ep sequence 100 times and align it to the pfam sequence
def align_with_permute_ep_seq(pfam_seq, ep_seq):
    score_list = []
    ep_list = list(ep_seq)
    if len(ep_list) != 0:
        for step in range(100):
            random_triple_letter = random.choice(amino_acids.keys())
            ep_list[randint(0, (len(ep_list) - 1))] = amino_acids[random_triple_letter]
            ep_seq = ''.join(ep_list)
            score_list.append(pairwise2.align.globalxx(pfam_seq, ep_seq, score_only=1))
        # print score_list
        x_mean = numpy.mean(score_list)
        return x_mean
    else:
        return float('NaN')


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
    seq_identity_percentage = 100.0 * matches / (len(alignment[pos][0]))
    seq_identity = seq_identity_percentage / 100
    return seq_identity, pos


def map_ep_to_pfam(alignments, max_pos, energy_object, pfam_seq, pfam_acc, pdb_start, pdb_end):
    print "mapping"
    destination = dest_folder + pfam_acc + "_" + energy_object._epros_file__name + ".txt"
    print "writing to: ", destination
    alignment = alignments[max_pos]
    print alignment[1]
    res = str(''.join(energy_entry._epros_file__res))
    ss = str(''.join(energy_entry._epros_file__ss))
    energy = energy_entry._epros_file__energy[pdb_start:pdb_end]

    export_aa_list = []
    export_res_list = []
    export_ss_list = []
    export_energy_list = []
    export_quant_list = []
    i = 0
    sub_ss = ss[pdb_start:pdb_end]
    sub_res = res[pdb_start:pdb_end]
    for aa in alignment[1]:
        try:
            (sub_res[i])
        except:
            continue
        if aa == "-" and sub_res[i] != "-":
            export_aa_list.extend(aa)
            export_res_list.extend("-")
            export_ss_list.extend("-")
            export_energy_list.extend("-")
            export_quant_list.extend("-")
        else:
            export_aa_list.extend(aa)
            export_res_list.extend(sub_res[i])
            export_ss_list.extend(sub_ss[i])
            export_energy_list.extend(['%.2f' % energy[i]])
            if energy[i] < quartile[1]:
                export_quant_list.extend("1")
            elif quartile[1] < energy[i] < quartile[2]:
                export_quant_list.extend("2")
            elif quartile[2] < energy[i] < quartile[3]:
                export_quant_list.extend("3")
            elif energy[i] > quartile[3]:
                export_quant_list.extend("4")
            i += 1

    print ''.join(export_res_list)
    print ''.join(export_ss_list)
    print ''.join(export_quant_list)
    print ' '.join(export_energy_list)

    if os.path.isfile(destination):
        print "APPEND!"
        with open(destination, "a") as target:
            target.write("\n")
            target.write(">ID:\t" + pfam_seq.id + "\n")
            target.write(">SEQ:\t" + ''.join(export_res_list) + "\n")
            #target.write(">SEQ2:\t" + str(alignment[0]) + "\n")
            target.write(">QUAN:\t" + ''.join(export_quant_list) + "\n")
            target.write(">SSE:\t" + str(''.join(export_ss_list)) + "\n")
            target.write(">EVAL:\t" + str(' '.join(export_energy_list)) + "\n")
    else:
        print "CREATING NEW FILE!"
        with open(destination, 'w') as target:
            target.write("\n")
            target.write(">ID:\t" + pfam_seq.id + "\n")
            target.write(">SEQ:\t" + ''.join(export_res_list) + "\n")
            #target.write(">SEQ2:\t" + str(alignment[0]) + "\n")
            target.write(">QUAN:\t" + ''.join(export_quant_list) + "\n")
            target.write(">SSE:\t" + str(''.join(export_ss_list)) + "\n")
            target.write(">EVAL:\t" + str(' '.join(export_energy_list)) + "\n")

    # output should look like this
    '''
    >ID:    FA9_HUMAN/97-127:1IXA-A/51-81
    >SEQ:   CESN-----PCLNGGSCK-
    >QUAN:  2341.....214324112-
    >SSE:   cccc*****cccEEEEccc
    >EVAL:  -12.32 -12.1 -2.12 -0.12 -7.51...
    '''
    sys.exit(0)
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
        pdb_id = line_array[0]
        pdb_pos = line_array[5].strip(";\n")
        insert_into_dict(line_array[3], pdb_id + "." + pdb_pos, pdbmap_dict)

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
        for pdb_id_with_pos in pdb_id_list_set:
            pdb_id = pdb_id_with_pos.split(".")[0]
            pdb_pos = pdb_id_with_pos.split(".")[1]
            file = os.path.join(energy_dir + pdb_id + ".ep2")
            if os.path.isfile(file):
                print "creating energy object " + pdb_id + " for pfam: " + pfam_accesion
                energy_list.append(epros_file.create_energyprofile(file, pdb_pos))

        # align each pfam sequence
        for pfam_record in pfam_alignment:
            # with each energy sequence
            for energy_entry in energy_list:
                # get the right sub sequence from the pdbmap file
                pdb_start = int(energy_entry._epros_file__pdb_pos.split("-")[0]) + 1  # +1 for logic
                pdb_end = int(energy_entry._epros_file__pdb_pos.split("-")[1]) + 1
                # calculate offset, because pdb files often doesn't start with position 1
                try:
                    offset = int(energy_entry._epros_file__resno[0])
                except:
                    print "OFFSET ERROR! skipping"
                    continue
                pdb_start -= offset
                pdb_end -= offset
                print "alignment", energy_entry._epros_file__name, "with", pfam_accesion, "id", pfam_record.id
                # print energy_entry._epros_file__res[pdb_start:pdb_end]
                # print len(energy_entry._epros_file__res[pdb_start:pdb_end])

                epros_res = str(''.join(energy_entry._epros_file__res[pdb_start:pdb_end]))
                pfam_energy_alignments = pairwise2.align.globalxx(pfam_record.seq, epros_res)
                x_row = 0
                for a in pfam_energy_alignments:
                    if a[2] > x_row:
                        x_row = a[2]
                print "X_ROW: ", x_row
                x_opt = pairwise2.align.globalxx(pfam_record.seq, pfam_record.seq, score_only=1)
                print "X_OPT: ", x_opt
                if x_opt > (x_row*10):
                    print "x_opt delta to big, skipping"
                    continue
                x_mean = align_with_permute_ep_seq(pfam_record.seq, epros_res)
                if math.isnan(x_mean):
                    print "x_mean is not a number, skipping"
                    continue
                print "X_MEAN: ", x_mean
                x_real = -1 * numpy.log10((x_row - x_mean) / (x_opt - x_mean))
                print "X_REAL: ", x_real
                seq_identity, max_pos = calc_seq_identity(pfam_energy_alignments)
                print "SEQ_IDENTITY: ", seq_identity
                x_pred = -1.006 * numpy.log(seq_identity) + 4.7189  # seq identity in % or as 0.xx???
                print "X_PRED: ", x_pred
                x_z = (x_real - x_pred) / 0.03858
                print "X_Z: ", x_z
                # if x_z >= 1.60:
                if seq_identity > 0.90:
                    map_ep_to_pfam(pfam_energy_alignments, max_pos, energy_entry, pfam_record, pfam_accesion,
                                   pdb_start, pdb_end)

print str(time.time() - start_time)
print "Done"
