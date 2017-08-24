# bash script for calculationg energy profile for whole folder:

for f in *.pdb ; do java -jar /mnt/h/Master/Python_Master_scripts/Java/SimpleECalc.jar "$f"; done

# add connections to ep2 files
for f in *.ep2 ; do /mnt/h/Master/Python_Master_scripts/Energy_Profile/add_aa_connections_for_one_file.py -f "$f"; done

# plot energy profiles
for f in *.cnn ; do /mnt/h/Master/Python_Master_scripts/Energy_Profile/plot_energy_profile.py -e1 MSH2_3thw.ep2.cnn -e2 "$f"; done
