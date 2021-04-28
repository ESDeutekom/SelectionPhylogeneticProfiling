#!/hosts/linuxhome/scarab/eva2/Programs/miniconda3/bin/python
#python 3

import sys
import pandas as pd
import random
from scipy.spatial import distance
from sklearn.metrics import roc_auc_score, roc_curve, auc
#use random sets of ortholgous groups/profiles
#Run in parallel 20 times to get 1000 sets

#og profiles
pro_file = sys.argv[1]
#leca_ogs
leca_ogs = sys.argv[2]
#positive set
pos_set_file = sys.argv[3]
#negative set
neg_set_file = sys.argv[4]
#output file
out_file = sys.argv[5]

#leca profiles
#need to get the header
#get dictionary
profile = pd.read_csv(pro_file, sep = "\t", index_col = 0)#print("profiles: ", len(prof_d))

#leca ogs
leca = pd.read_csv(leca_ogs, header = None)#print("leca ogs: ", len(leca_d))
#leca profiles
profile_leca = profile[profile.index.isin(leca[0])]

#positive biogrid set
pos_setr = pd.read_csv(pos_set_file, sep = "\t")
pos_set = pos_setr[["OG_A", "OG_B"]]
pos_set_leca = pos_set[pos_set[["OG_A", "OG_B"]].isin(list(leca[0])).all(axis=1)]
pos_set_leca.head()
#negative set
neg_setr = pd.read_csv(neg_set_file, sep = "\t", header = None)
neg_set = neg_setr[[2,3]]
neg_set.columns = ["OG_A", "OG_B"]
neg_set_leca = neg_set[neg_set[["OG_A", "OG_B"]].isin(list(leca[0])).all(axis=1)]


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


with open(out_file, "w") as out_file:
    #out_file.write("\t".join(["all_og", str(base_auc), "\n"]))

    for i in range(0,50): #Can be run in parallel 20 times
        profile_rand_og = profile_leca.sample(frac=0.63) #take 63% of the original data/OGs

        pos_df = get_distance_df(pos_set_leca, profile_rand_og, "positive")
        neg_df = get_distance_df(neg_set_leca, profile_rand_og, "negative")
        dist_df = pd.concat([pos_df, neg_df])
        #get max because we are using distances
        max_r = max(dist_df["cosine"])

        fpr, tpr, _ = roc_curve(dist_df.loc[:,"set"], [max_r-x for x in dist_df.loc[:,"cosine"]], pos_label="positive")
        roc_auc = auc(fpr, tpr)        #print(auc)
        if i in [10,25,50]:
            print(i, roc_auc)
        out_file.write("\t".join([str(fpr.tolist()), str(tpr.tolist()), str(roc_auc), "\n"]))
