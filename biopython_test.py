#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Bio.Seq import Seq
from Bio import pairwise2
from Bio import AlignIO

#create a sequence object
my_seq = Seq('CATGTAGACTAG')

#print out some details about it
print 'seq %s is %i bases long' % (my_seq, len(my_seq))
print 'reverse complement is %s' % my_seq.reverse_complement()
print 'protein translation is %s' % my_seq.translate()


alignments = pairwise2.align.globalxx("ACCGT", "ACG")

print alignments

#with open("Pfam 31.0/7TM_transglut.txt", "r") as file:

alignment = AlignIO.read(open("Pfam 31.0/12TM_1.txt"), "stockholm")
print("Alignment length %i" % alignment.get_alignment_length())
for record in alignment :
    print(record.seq + " " + record.id)

