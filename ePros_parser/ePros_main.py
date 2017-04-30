#!/usr/bin/env python
# -*- coding: utf-8 -*-


from epros_file import epros_file
import os
import sys
import argparse

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory")
parser.add_argument("-e", "--energy", help="input energy profile directory")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "This script maps Energy Profiles to Alignment Data"
    print "Please enter a input directory"
    parser.print_help()
    sys.exit(0)

energy_dir = args.energy
energy_list = []
name = ""
type = ""
head = ""
chain = ""
resno = ""
res = ""
ss = ""
energy = ""

for dirpath, dir, files in os.walk(top=energy_dir):
    for file in files:
        line_count = 0
        with open(energy_dir + file, 'r') as energy_file:
            for line in energy_file:
                line_array =line.split("\t")
                if line_count == 0:
                    name = line_array[1]
                elif line_count == 1:
                    type = line_array[1]
                elif line_count == 3:
                    header = line_array
                else:
                    head = line_array[0]
                    chain = line_array[1]
                    resno = line_array[2]
                    res = line_array[3]
                    ss = line_array[4]
                    energy = line_array[5]
                line_count += 1
            energy_list.append(epros_file(name, type, head, chain, resno, res, ss, energy))

