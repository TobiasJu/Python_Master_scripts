#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import sys

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="input directory with files (will iterate over all files)")
parser.add_argument("-l", "--list", help="list of files to purge")


args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "this script takes a folder and purge all files in the given list"
    parser.print_help()
    sys.exit(0)

def get_purge_list(dir):
    purge_list = []
    with open(dir, 'r') as file_handle:
        for line in file_handle:
            purge_list.append(line.rstrip())
    return purge_list


def purge(dir, purge_list):
    purge_counter = 0
    for f in os.listdir(dir):
        if f in purge_list:
            print "removing: ", f
            os.remove(os.path.join(dir, f))
            purge_counter += 1
    return purge_counter


# ------------------------------------------------- main script ------------------------------------------------------ #


purge_list = get_purge_list(args.list)
purge_counter = purge(args.dir, purge_list)

print "purged ", purge_counter, " files"

