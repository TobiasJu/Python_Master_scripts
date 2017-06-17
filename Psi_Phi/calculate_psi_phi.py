#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import subprocess

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory of the Pfam family files")
parser.add_argument("-e", "--energy", help="input energy profile directory")
parser.add_argument("-p", "--pdbmap", help="pdbmap location")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy files and analyzes them"
    parser.print_help()
    sys.exit(0)

process = subprocess.Popen(['ls', '-a'], stdout=subprocess.PIPE)
out, err = process.communicate()
print(out)