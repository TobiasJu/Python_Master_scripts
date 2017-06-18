#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import subprocess
import os
import matplotlib
matplotlib.use('Agg')
import numpy as np
from scipy.stats import kendalltau
import seaborn as sns
sns.set(style="ticks")
import math

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory of the Pfam family files")
# parser.add_argument("-e", "--energy", help="input energy profile directory")
# parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and analyzes them"
    parser.print_help()
    sys.exit(0)

currentFile = __file__  # May be 'my_script', or './my_script' or
                        # '/home/user/test/my_script.py' depending on exactly how
                        # the script was run/loaded.
realPath = os.path.realpath(currentFile)  # /home/user/test/my_script.py
dirPath = os.path.dirname(realPath)  # /home/user/test
dirName = os.path.basename(dirPath) # test

call = 'java -jar ' + dirPath + '/ramachan.jar' + ' -i ' + "/mnt/d/1brr.pdb"
print call

process = subprocess.Popen([call],shell=True, stdout=subprocess.PIPE)
out, err = process.communicate()
split_out = out.splitlines()
split_out.pop(0)

pos_list = []
psi_list = []
phi_list = []

for line in split_out:
    line_array = line.split(";")
    print line
    pos_list.append(int(line_array[0]))
    psi_list.append(float(line_array[1]))
    phi_list.append(float(line_array[2]))

psi_list_numpy = np.array(psi_list)
phi_list_numpy = np.array(phi_list)

#print psi_list
#print phi_list

print psi_list[0], ":", phi_list[0]
print psi_list[1], ":", phi_list[1]
print psi_list[2], ":", phi_list[2]

sns_plot = sns.jointplot(psi_list_numpy, phi_list_numpy, kind="hex", color="#4CB391")  # stat_func=kendalltau
#sns_plot.ylim(-180, 180)
sns_plot.savefig("ramachan.pdf")

