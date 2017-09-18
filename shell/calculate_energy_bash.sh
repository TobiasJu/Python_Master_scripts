#!/usr/bin/env bash
# bash script for calculationg energy profile for whole folder:

# first create energy profiles for pdb file
for f in *.pdb ; do java -jar ../../Python_Master_scripts/Java/SimpleECalc.jar "$f"; done

# add connections to ep2 files
for f in *.ep2 ; do ../../Python_Master_scripts/Energy_Profile/add_aa_connections_for_one_file.py -f "$f"; done

# plot energy profiles from SNPs vs original
for f in *.cnn ; do ../../Python_Master_scripts/Energy_Profile/plot_energy_profile.py -e1 NP_000526.2_PMS2_2.ep2.cnn -e2 "$f"; done
