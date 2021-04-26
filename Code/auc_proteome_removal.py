#!/hosts/linuxhome/scarab/eva2/Programs/miniconda3/bin/python
#python 3

import sys
import pandas as pd
from scipy.spatial import distance
from sklearn.metrics import roc_auc_score
#remove proteomes one by one and see how auc improves

#sequentially remove proteomes
#measure distances between interacting sets
#calculate new auc values

#og profiles
pro_file = sys.argv[1]
#leca_ogs
leca_file = sys.argv[2]
#positive set
positive_file = sys.argv[3]
#negative set
negative_file = sys.argv[4]
#output file
out_file = sys.argv[5]

#leca profiles
#need to get the header
profile = pd.read_csv(pro_file, sep = "\t", index_col = 0)
profile.index = profile.index.map(str)

leca = pd.read_csv(leca_file, header = None).astype(str)
profile_leca = profile[profile.index.isin(leca[0])]

pos_setr = pd.read_csv(positive_file, sep = "\t")
pos_set = pos_setr[["OG_A", "OG_B"]]
pos_set = pos_set.astype(str)
pos_set_leca = pos_set[pos_set[["OG_A", "OG_B"]].isin(list(leca[0])).all(axis=1)]
pos_set_leca.head()

####get pseudo negative interaction set
neg_setr = pd.read_csv(negative_file, sep = "\t", header = None)
neg_set = neg_setr[[2,3]]
neg_set.columns = [["OG_A", "OG_B"]]
neg_set = neg_set.astype(str)
neg_set_leca = neg_set[neg_set[["OG_A", "OG_B"]].isin(list(leca[0])).all(axis=1)]

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

#when only auc is needed
def get_auc(profile, keep_list, pos_set, neg_set):
    profile_dropped = profile[keep_list] #
    profile_dropped.index.name = "OG"
    pos_df = get_distance_df(pos_set, profile_dropped, 1) #score near 0 is good
    neg_df = get_distance_df(neg_set, profile_dropped, 0) #score near 1 is good
    #cosine can become NaN if profile/vector only contains 0's
    #Can be caused by genomes removed
    #This was not a problem before because the set is defined in HSAP
    #HSAP that is always present, so 1, and vector will always contian a 1
    dist_df = pd.DataFrame(pos_df.append(neg_df))
    #auc calculate with distances (roc scores: 0 bad and 1 good, and for distances 0 is good and 1 bad)
    #because of this the auc is inverted and must be converted with 1 - auc
    auc = 1 - roc_auc_score(dist_df.loc[:,"set"],dist_df.loc[:,"cosine"].astype(float))
    return auc

base_set =profile_leca.columns

auc_base = get_auc(profile_leca, base_set, pos_set_leca, neg_set_leca)
print("base", auc_base)

with open(out_file, "w") as out_file:
    #out_file.write("\t".join(["base", str(auc_base),"\n"]))

    for species in profile_leca.columns:
        minus_species = [x for x in profile_leca.columns if x != species]
        auc = get_auc(profile_leca, minus_species, pos_set_leca, neg_set_leca)
        print(species, auc)
        out_file.write("\t".join([species, str(auc), "\n"]))
