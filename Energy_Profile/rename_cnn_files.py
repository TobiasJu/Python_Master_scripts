#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import itertools
import numpy as np


# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--energy_dir", help="input energy profile directory, with .cnn files (will iterate over all files)")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder of energy .cnn files and rename them properly"
    parser.print_help()
    sys.exit(0)

for dirpath, dir, files in os.walk(top=args.energy):
    for energy_file in files:
        print energy_file



