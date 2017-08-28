#!/usr/bin/env nextflow


numberchannel = Channel
			    //.from( 1,2,3,4,5,6,7,8,9,10 )
			    .from( 'a', 'aa', 'abc', 'pdb184d.ent.gz', 'pdb190d.ent.gz', '/nfs/biodb/pdb/data/structures/all/pdb/pdb1a0d.ent.gz' , '/nfs/biodb/pdb/data/structures/all/pdb/pdb1htq.ent.gz','/nfs/biodb/pdb/data/structures/all/pdb/pdb185d.ent.gz')
			    .filter( ~/^pdb1*/ )
			    .subscribe onNext: { println it }, onComplete: { println 'Done' }

// def list2 = numberchannel[0..4]

//println list2