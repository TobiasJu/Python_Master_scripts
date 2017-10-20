#!/usr/bin/env nextflow

// currently this script is for calculationg energyprofiles for alpha helial membran proteins from the ".fromPath(...)" folder
// you can calculate energyprofiles for globular Proteins, if you remove the "m" in line 44 (see line below)
// currently the script runs on a local machine with nextflow installed
// you can run this script with drmaa on the cloud if you uncomment the excecutor lines

params.in = "/homes/tjuhre/Master/Python_Master_scripts"
params.script_path = "/homes/tjuhre/Master/Python_Master_scripts"
params.db_path = "/ceph/sge-tmp/tjuhre/membranePDB_test"
//'/nfs/biodb/pdb/data/structures/all/pdb/*.gz'


pdb_files = Channel
		    .fromPath("$params.db_path/*.gz")
		    .filter( ~/^(?:(?!pdb1htq.ent.gz|pdb4xq2.ent|pdb4cg3.ent|pdb4ptj.ent|pdb4tyv.ent|pdb4tz5.ent|pdb4pth.ent|pdb4p3q.ent|pdb2hyn.ent|pdb2ms7.ent|pdb2kox.ent|pdb2wwv.ent|pdb2m8l.ent|pdb4cbo.ent|pdb2ku2.ent|pdb4p3r.ent|pdb2ku1.ent|pdb2kh2.ent|pdb5ivh.ent.gz|pdb5ivk.ent.gz|pdb5ijn.ent.gz|pdb5exu.ent.gz|pdb5vy4.ent.gz|pdb5vy3.ent.gz).)*$/ )

// extract the pdb files otf
process extract_pdb_gz {
	maxForks 200
	cache false
	input:
	file pdb_file from pdb_files

	output:
	file "*.ent" into extracted_pdb

	script:
	"""
	$params.script_path/data_mining/extract_all_gz.py -f ${pdb_file}
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
	java -jar $params.script_path/Java/SimpleECalc.jar m ${energy_file_name}
	"""
	//java -jar $params.script_path/Java/SimpleECalc.jar ${energy_file_name}
}

/*
notes to the jar, from Florian:

Das JAR ist einfach mittels 'java -jar SimpleECalc.jar' auf der Kommandozeile auszuführen, als Parameter geben Sie eine (odere mehrere) PDB-Dateinamen an

- desweiteren können Sie mit dem Argument 'g' explizit definieren, dass die Struktur(en) als globuläre Proteine zu betrachten sind

- mit der Option 'm' führen Sie entsprechend die Berechnung für Membran-Proteine aus. Eine MEMEMBED-Installation ist wie gesagt Voraussetzung.

- es ist nicht möglich für jede Struktur explizit den Parameter g oder m zu setzen! Eine solche Umsetzung war in der kurzen Zeit nicht möglich. In diesem Fall können Sie einfach SimpleECalc für jede einzelne Struktur mit entsprechendem Parameter im Batch laufen lassen

- ACHTUNG: wird kein Parameter angegeben, wird die Struktur (oder die Strukturen) als globulär betrachtet! 

*/


//calculate connections for each ep file
process add_connections{
	//executor 'drmaa'
	cache false
	//publishDir '/homes/tjuhre/tmp/energy_profiles_membrane', mode: 'copy'

	input:
	set file(energy_file), file(pdb_file) from calculated_energy_profile

	output:
	file "${energy_file}.cnn" into connections

	script:
	"""
	$params.script_path/Energy_Profile/add_aa_connections.py -f ${energy_file} -pf $pdb_file
	"""
}

//proper naming of the files
process rename_energy_files{
	//executor 'drmaa'

	publishDir '/homes/tjuhre/tmp/energy_profiles_membrane_test', mode: 'copy'
	input:
	file energy_file from connections

	output:
	file "*.ep2" into renamed

	script:
	"""
	$params.script_path/Energy_Profile/rename_cnn_files.py -f $energy_file
	"""
}