#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil
import urllib2
from contextlib import closing
from os.path import basename
import gzip
import tarfile

# argparse for information
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="input directory")
parser.add_argument("-r", "--remove", action="store_true", help="removes the .gz file after extracting")
args = parser.parse_args()

# sanity check
if not len(sys.argv) > 1:
    print "This script extracts all files in a given directory, including sub directories."
    print "Which directory (including sub directories) would you like to extract?"
    parser.print_help()
    sys.exit(0)

input = args.directory

# in case of a extraction error, caused by a downloading error, reload the file
def reload_file(file, dirpath):
    print "reloading file: " + file
    print 'ftp://ftp.rcsb.org/pub/pdb/data/structures/divided/' + dirpath + "/" + file
    with closing(urllib2.urlopen('ftp://ftp.rcsb.org/pub/pdb/data/structures/divided/' + dirpath + "/" + file)) as r:
        with open(dirpath + "/" + file, 'wb') as reloaded_file:
            shutil.copyfileobj(r, reloaded_file)
    with gzip.open((os.path.join(dirpath, file)), 'rb') as f:
        file_content = f.read()
        extracted_file = open((os.path.join(dirpath, os.path.splitext(file)[0])), 'w')
        extracted_file.write(file_content)
        extracted_file.close()

for dirpath, dir, files in os.walk(top=input):
    for file in files:
        if ".gz" in file:
            print "extracting: " + (os.path.join(dirpath, file))

            try:
                with gzip.open((os.path.join(dirpath, file)), 'rb') as f:
                    file_content = f.read()
                    extracted_file = open((os.path.join(dirpath, os.path.splitext(file)[0])), 'w')
                    extracted_file.write(file_content)
                    extracted_file.close()
    #            tar = tarfile.open(os.path.join(dirpath, file))
    #            tar.extractall(path=dirpath)
    #            tar.close()
            except:
                reload_file(file, dirpath)
            if args.remove:
                os.remove(os.path.join(dirpath, file))

print "Extraction finished"
