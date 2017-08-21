# bash script for calculationg energy profile for whole folder:

for f in *.pdb ; do java -jar /homes/tjuhre/Master/Python_Master_scripts/Java/SimpleECalc.jar "$f"; done

for f in *.ep2 ; do /homes/tjuhre/Master/Python_Master_scripts/Energy_Profile/add_aa_connections_for_one_file.py -f "$f"; done