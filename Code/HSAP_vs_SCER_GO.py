#python3

import os
import sys
import pandas as pd
import random
##############################################################
## Make GO background and forground set
## OG interactions in human and lost/not in yeast
## foreground is all OGs lost in SCER but present in HSAP
## background in all OGs present in SCER and HSAP
## can be run 10 times in parallel to get different back-/foreground sets
#############################################################
og_file = sys.argv[1]
leca_file = sys.argv[2]
meta_file = sys.argv[3]
int_file = sys.argv[4] #from human
out_back = sys.argv[5] #list of leca ens ids in species
out_front = sys.argv[6] #list of leca ens ids in species interactions


#leca og dict
leca_d = {}
for lines in open(leca_file, "r"):
    leca = str(lines.rstrip())
    leca_d[leca] = True

#species id to ensemble id from meta file species
id_to_ens_d = {}
for lines in open(meta_file, "r"):
    line = lines.rstrip().split("\t")
    id = line[0]
    lt = line[7]
    ens = line[9].split(".")[0]
    if lt == "1": #longest transcript
        id_to_ens_d[id] = ens

ints_d = {}
for lines in open(int_file, "r"):
    line = lines.rstrip().split("\t")
    id1 = str(line[2])
    id2 = str(line[5])
    #we want to maintain the same set we use for distance calculation
    #for fair comparison
    if id1 != id2:
        if (id1, id2) not in ints_d:
            if (id2, id2) not in ints_d:
                ints_d[(id1, id2)] = True

int_ids = set([el for t in ints_d.keys() for el in t])

#read in OGs and corresponding sequences
leca_ogs_in_SCER = {} #leca in HSAP interaction
leca_ogs = {} #all leca in HSAP and not in SCER

#for every og check if in LECA
#select random seq if more than 1 seq of species id in OG
#for sequence of species id in OG, check if in interaction or not
#background is leca og not in interaction
#foreground is leca of in interaction
for lines in open(og_file, "r"):
    line = lines.rstrip().split(": ")
    og = str(line[0])
    seqs = line[1].split(" ")
    if og in leca_d: #if leca og
        track_seq = [] #keep track of species multiple sequences
        track_seq_S = []
        for seq in seqs:
            if seq[0:4] == "HSAP": #if in species
                track_seq += [seq]
            if seq[0:4] == "SCER":
                track_seq_S += [seq]

        if track_seq: #if in human
            seqr = random.choice(track_seq) #randomly select one sequence
            if track_seq_S: #if in both human and yeast
                if seqr in int_ids:
                    leca_ogs_in_SCER[seqr] = id_to_ens_d[seqr]
            elif not track_seq_S: #if only in human
                if seqr in int_ids:
                    leca_ogs[seqr] = id_to_ens_d[seqr]

out_back = open(out_back, "w")
for key, value in leca_ogs_in_SCER.items():
    out_back.write("%s\t%s\n" % (value, key))
out_back.close()

out_front = open(out_front, "w")
for key, value in leca_ogs.items():
    out_front.write("%s\t%s\n" % (value, key))
out_front.close()
