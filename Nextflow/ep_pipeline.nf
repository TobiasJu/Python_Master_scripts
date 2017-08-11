#!/usr/bin/env nextflow

//pdb_files = Channel.fromPath('/ceph/sge-tmp/pdbe/*.ent')
pdb_files = Channel.fromPath('/homes/tjuhre/tmp/pdb_test/*.ent')


//calculate Energyprofiles for pdb file
process calculate_energy_profile {
	//executor 'drmaa'
	maxForks 100
    //publishDir '/homes/tjuhre/tmp/energy_files_out', mode: 'copy'
	//errorStrategy { task.exitStatus == 'terminate' }
	
	input:
	file energy_file_name from pdb_files

	output:
	file "${energy_file_name}.ep2" into connections

	script:
	"""
	java -jar /homes/tjuhre/Master/Python_Master_scripts/Java/SimpleECalc.jar ${energy_file_name}
	"""
}

//calculate connections for each ep file
process add_connections{
	//executor 'drmaa'
	publishDir '/homes/tjuhre/tmp/energy_profiles', mode: 'copy'

	input:
	file energy_file from connections

	output:
	file "${energy_file}.cnn" into out

	script:
	"""
	/homes/tjuhre/Master/Python_Master_scripts/Energy_Profile/add_aa_connections.py -f ${energy_file}
	"""
}
