#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import math
import pprint

### Script to evaluate the .cnn files from SNPs and prints a table

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--energy", help="input energy profile directory")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder with subfolders of energy files and evaluates them"
    parser.print_help()
    sys.exit(0)


# returns a list of all files in the dir with subdirs
def list_files(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            file_list.append(os.path.join(root, name))
    return file_list


# inserts a key value pair into the dict, or adds the value if the key exists
def insert_into_data_structure(key, value, dict):
    if not key in dict:
        dict[key] = value
    else:
        dict[key].append((value))

# ------------------------------------------------- main script ------------------------------------------------------ #

snp_dict = {}

dir_file_list = list_files(args.energy)
for e_file in dir_file_list:
    if e_file.endswith(".cnn"):
        print e_file
        snp_list = []
        name = ""
        a_type = ""
        if "p." in e_file:
            # snp file
            file_name = e_file.split("/")[-1]
            last_name = re.split("\dp.", e_file)[-1]
            snp_id = re.split(".ep2", last_name)[0]
            snp_id_pre = last_name.split(".ep2")[0]
            absolute_snp_pos = int(re.findall('\d+', snp_id_pre)[0])
            # snp_list.append(file_name)
            snp_list.append(snp_id)
            if "benign" in e_file:
                snp_flag = "benign"
            elif "pathogenic" in e_file:
                snp_flag = "pathogenic"
            snp_list.append(snp_flag)

            # suche unverändertes file
            np = re.split("p.", file_name)[0]
            #print file_name
            #print np
            of = np + "_"
            print of
            original_file = ""
            for e_file2 in dir_file_list:
                if e_file2.endswith(".cnn"):
                    if of in e_file2:
                        original_file = e_file2

            o_resNo_list = []
            o_energy_list = []
            o_contact_list = []
            with open(original_file, "r") as original_energy_file_handle:
                for line in original_energy_file_handle:
                    if line.startswith('ENGY'):
                        line_array = line.split("\t")
                        chain = line_array[1]
                        if chain == "A":
                            resNo = int(line_array[2])
                            o_resNo_list.append(resNo)
                            energy_value = float(line_array[5])
                            o_energy_list.append(energy_value)
                            contacts = line_array[6].replace(" ", "")
                            o_contact_list.append(contacts)

            resNo_list = []
            energy_list = []
            contact_list = []
            with open(e_file, "r") as energy_file_handle:
                for line in energy_file_handle:
                    if line.startswith('ENGY'):
                        line_array = line.split("\t")
                        chain = line_array[1]
                        if chain == "A":
                            resNo = int(line_array[2])
                            resNo_list.append(resNo)
                            #residue = line_array[3]
                            #secStructure = line_array[4]
                            energy_value = float(line_array[5])
                            energy_list.append(energy_value)
                            contacts = line_array[6].replace(" ", "")
                            contact_list.append(contacts)
                    elif line.startswith('NAME'):
                        name = line.split("\t")[1]
                        snp_list.append(name.strip())
                    elif line.startswith('TYPE'):
                        a_type = line.split("\t")[1]
                        snp_list.append(a_type.strip())

            # search the snp pos and calculate the energy diff
            for o_energy, snp_energy, resNo in zip(o_energy_list, energy_list, resNo_list):
                if resNo == absolute_snp_pos:
                    snp_energy_diff = o_energy - snp_energy
                    print snp_energy_diff
                    snp_list.append(snp_energy_diff)
                    o_energy_square = o_energy**2
                    snp_energy_square = snp_energy**2
                    snp_energy_diff_amount = math.sqrt(o_energy_square) - math.sqrt(snp_energy_square)
                    ################## is NOT THE SAME!!!!!!
                    # snp_energy_diff_amount = math.sqrt((o_energy**2)) - math.sqrt((snp_energy**2))
                    snp_list.append(snp_energy_diff_amount)

            # iterate over contact string and save the contact positions and dont forget the offset
            contact_resNo_list = []
            for contact, resNo in zip(contact_list[absolute_snp_pos - resNo_list[0]], resNo_list):
                if contact == "1":
                    contact_resNo_list.append(resNo)

            total_energy_diff = 0
            total_contact_energy_diff = 0
            contact_energy_diff_list = []
            # iterate over the contacts and calculate energy diff for every contact
            for o_energy, snp_energy, resNo in zip(o_energy_list, energy_list, resNo_list):

                energy_diff = o_energy - snp_energy
                if energy_diff < float(0):
                    total_energy_diff += energy_diff * -1
                else:
                    total_energy_diff += energy_diff

                if resNo in contact_resNo_list:
                    contact_energy_diff = o_energy - snp_energy
                    if contact_energy_diff < float(0):
                        total_contact_energy_diff += contact_energy_diff * -1
                    else:
                        total_contact_energy_diff +=contact_energy_diff


                    #print o_energy, snp_energy, resNo, contact_energy_diff
                    contact_energy_diff_list.append(contact_energy_diff)

                    #if "-" in contact_energy_diff:
                    #    snp_list.append(contact_energy_diff)

                    #o_energy_square = o_energy**2
                    #contact_energy_square = snp_energy**2
                    #contact_energy_amount = math.sqrt(o_energy_square) - math.sqrt(contact_energy_square)
                    #snp_list.append(contact_energy_amount)
            snp_list.append(total_energy_diff)
            snp_list.append(total_contact_energy_diff)
            snp_list.append(contact_energy_diff_list)
            insert_into_data_structure(file_name, snp_list, snp_dict)

# pprint.pprint(snp_dict)

print "File;SNP;clinVar;Name;type;energy_diff;energy_diff_amount;total_diff;total_contact_diff;contact_diffs;contact_diffs_amount"
for key, value in snp_dict.iteritems():

    sys.stdout.write(key)
    sys.stdout.write(";")
    for entry in value:
        if type(entry) == float:
            number_str = str(entry).replace(".", ",")
            sys.stdout.write(number_str)
            sys.stdout.write(";")
        else:
            sys.stdout.write(str(entry))
            sys.stdout.write(";")
    print ""