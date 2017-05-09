#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this script splits the Pfam-A.clans.tsv into globular and membrane associated families

membrane_pfams = open("membrane_pfam.tsv", 'w')
globular_pfams = open("globular_pfam.tsv", 'w')

membrane_counter = 0
glob_counter = 0

with open('Pfam-A.clans.tsv', 'r') as all_families_file:
    for line in all_families_file:
        if "Membrane" in line:
            membrane_pfams.write(line)
            membrane_counter += 1
        elif "membrane" in line:
            membrane_pfams.write(line)
            membrane_counter += 1
        else:
            globular_pfams.write(line)
            glob_counter += 1

membrane_pfams.close()
globular_pfams.close()

print "Extracted: " + str(glob_counter) + " globular Pfams"
print "Extracted: " + str(membrane_counter) + " membrane associated Pfams"


