#!/hosts/linuxhome/scarab/eva2/Programs/miniconda3/bin/python
#python 3

import sys
import pandas as pd
import random
from scipy.spatial import distance
from sklearn.metrics import roc_auc_score, roc_curve, auc
import math
#remove proteomes one by one and see how auc improves
#Run in parallel 20 times to get 1000 sets

#sequentially remove proteomes
#measure distances between interacting sets
#calculate new auc values

#og profiles
pro_file = sys.argv[1]
#leca_ogs
leca_ogs = sys.argv[2]
#positive set
pos_set_file = sys.argv[3]
#negative set
neg_set_file= sys.argv[4]
#output file
out_file = sys.argv[5]

#get dictionary
profile = pd.read_csv(pro_file, sep = "\t", index_col = 0)#print("profiles: ", len(prof_d))
profile.index = profile.index.map(str)

#leca ogs
leca = pd.read_csv(leca_ogs, header = None).astype(str)
print("leca ogs: ", len(leca))
#leca profiles
profile_leca = profile[profile.index.isin(leca[0])]


#positive biogrid set
pos_setr = pd.read_csv(pos_set_file, sep = "\t")
pos_set = pos_setr[["OG_A", "OG_B"]]
pos_set = pos_set.astype(str)
pos_set_leca = pos_set[pos_set[["OG_A", "OG_B"]].isin(list(leca[0])).all(axis=1)]
print(pos_set_leca.head())
#negative set
neg_setr = pd.read_csv(neg_set_file, sep = "\t", header = None)
neg_set = neg_setr[[2,3]]
neg_set.columns = ["OG_A", "OG_B"]
neg_set = neg_set.astype(str)
neg_set_leca = neg_set[neg_set[["OG_A", "OG_B"]].isin(list(leca[0])).all(axis=1)]
print(neg_set_leca.head())

#calculate distance function
def get_distance_df(interaction_set, profile, set_type):
    dist_df = []
    dist_d = {}
    for idx in range(0, len(interaction_set)):
        OG_A = interaction_set.iloc[idx, 0]
        OG_B = interaction_set.iloc[idx, 1]
        if OG_A in profile.index and OG_B in profile.index:
            if OG_A != OG_B:
                if (OG_A, OG_B) not in dist_d:
                    if (OG_B, OG_A) not in dist_d:
                        dist_d[(OG_A,OG_B)] = True #just to keep track

                        profA = list(profile.loc[OG_A,])
                        profB = list(profile.loc[OG_B,])
                        if sum(profA) == 0:
                            profA = [x+1e-6 for x in profA]
                        if sum(profB) == 0:
                            profB = [x+1e-6 for x in profB]
                        dist = {"OG_A,OG_B":(OG_A,OG_B),
                            "cosine": distance.cosine(profA, profB),
                            "set": set_type}
                        dist_df.append(dist)
    dist_df = pd.DataFrame(dist_df)
    return dist_df


pos_df = get_distance_df(pos_set_leca, profile_leca, "positive")
print(pos_df.head())

neg_df = get_distance_df(neg_set_leca, profile_leca, "negative")
print(neg_df.head())

dist_df = pd.concat([pos_df, neg_df])
print("BASE AUC: ", 1 - roc_auc_score(dist_df.loc[:,"set"],dist_df.loc[:,"cosine"]))

keep_track = 0
with open(out_file, "w") as out_file:
    while keep_track < 50: #times make a random choice of 50 proteomes, can be run in parallel 20 times to get 1000
        random_sample = random.sample(list(profile_leca.columns), k = 50)
        prof_drop = profile_leca[random_sample] #keep the samples of 50 genomes
        #print(i, random_sample)
        pos_df = get_distance_df(pos_set_leca, prof_drop, "positive")
        neg_df = get_distance_df(neg_set_leca, prof_drop, "negative")
        dist_df = pd.concat([pos_df, neg_df])
        #get max because we are using distances
        max_r = max(dist_df["cosine"])

        fpr, tpr, _ = roc_curve(dist_df.loc[:,"set"], [max_r-x for x in dist_df.loc[:,"cosine"]], pos_label="positive")
        roc_auc = auc(fpr, tpr)        #print(auc)
        #auc can be NaN if genomes set contains no fpr?
        if roc_auc != 'nan':
            keep_track += 1
            out_file.write("\t".join([",".join(random_sample), str(fpr.tolist()), str(tpr.tolist()), str(roc_auc), "\n"]))
        if keep_track in [10, 25, 50]:
            print(keep_track, roc_auc)
print("Done: ", str(sys.argv[5]))
