#!/usr/bin/env nextflow

pdb_files = Channel.fromPath('/ceph/sge-tmp/pdb/*.ent')

//calculate Energyprofiles for pdb file
process calculate_energy_profile {
	//excecutor 'drmaa'
	//clusterOptions '-pe multislot 32'

	input:
	file energy_file_name from pdb_files

	output:
	file("energy_files/${energy_file_name}.ep2") into connections

	script:
	"""
	java -jar /homes/tjuhre/Master/Python_Master_scripts/Java/SimpleECalc.jar ${energy_file_name}
	"""
}

//calculate connections for each ep file
process add_connections{
	//excecutor 'drmaa'
	publishDir '/homes/tjuhre/tmp/energy_files_out', mode: 'copy'

	input:
	file energy_file_name from connections

	output:
	file "${energy_files}" into out

	script:
	"""
	./homes/tjuhre/Master/Python_Master_scripts/Energy_Profile/add_aa_connections.py -f ${energy_file_name}
	"""
}