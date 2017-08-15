#!/usr/bin/env nextflow

pdb_files = Channel.fromPath('/nfs/biodb/pdb/data/structures/all/pdb/*.gz')
//pdb_files = Channel.fromPath('/homes/tjuhre/Master/pdb/*.gz')


process extract_pdb_gz {
	maxForks 100
	
	input:
	file pdb_file from pdb_files

	output:
	file "*.ent" into extracted_pdb

	script:
	"""
	/homes/tjuhre/Master/Python_Master_scripts/extract_all_gz.py -f ${pdb_file}
	"""
}


//calculate Energyprofiles for pdb file
process calculate_energy_profile {
	executor 'drmaa'
	
	input:
	file energy_file_name from extracted_pdb

	output:
	set file("${energy_file_name}.ep2"), file("${energy_file_name}") into calculated_energy_profile

	script:
	"""
	java -jar /homes/tjuhre/Master/Python_Master_scripts/Java/SimpleECalc.jar ${energy_file_name}
	"""
}

//calculate connections for each ep file
process add_connections{
	executor 'drmaa'
	publishDir '/homes/tjuhre/tmp/energy_profiles', mode: 'copy'

	input:
	set file(energy_file), file(pdb_file) from calculated_energy_profile

	output:
	file "${energy_file}.cnn" into connections

	script:
	"""
	/homes/tjuhre/Master/Python_Master_scripts/Energy_Profile/add_aa_connections.py -f ${energy_file} -pf $pdb_file
	"""
}

/*
process rename_energy_files{
	executor 'drmaa'
	input:
	file energy_file from connection

	output:
	file "*.ep2" into connections

	script:
	"""
	
	"""
}
*/