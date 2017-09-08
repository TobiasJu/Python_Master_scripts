#!/usr/bin/env nextflow

//pdb_files = Channel.fromPath('/homes/tjuhre/Master/pdb/*.gz')

//already_done_files = Channel
//		    .fromPath('/homes/tjuhre/tmp/energy_profiles/*.cnn')

pdb_files = Channel
		    //.fromPath('/nfs/biodb/pdb/data/structures/all/pdb/*.gz')
		    //.from( 'a', 'aa', 'abc', 'pdb184d.ent.gz', 'pdb190d.ent.gz', '/nfs/biodb/pdb/data/structures/all/pdb/pdb1a0d.ent.gz' , '/nfs/biodb/pdb/data/structures/all/pdb/pdb1htq.ent.gz','/nfs/biodb/pdb/data/structures/all/pdb/pdb185d.ent.gz')
		    .fromPath('/ceph/sge-tmp/tjuhre/pdb4/*.gz')
		    .filter( ~/^(?:(?!pdb1htq.ent.gz|pdb2hyn.ent|pdb2ms7.ent|pdb2kox.ent|pdb2wwv.ent).)*$/ )
		    //.filter( ~/\/nfs\/biodb\/pdb\/data\/structures\/all\/pdb\/pdb9/)
		    //.subscribe { println it }



process extract_pdb_gz {
	maxForks 200
	cache false
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
	//executor 'drmaa'
	cache false
	//publishDir '/homes/tjuhre/tmp/energy_profiles_no_c', mode: 'copy'
	
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
	//executor 'drmaa'
	cache false
	publishDir '/homes/tjuhre/tmp/energy_profiles_4', mode: 'copy'

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