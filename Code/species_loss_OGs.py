#!/hosts/linuxhome/scarab/eva2/Programs/miniconda3/bin/python
#python3
############################################################
## Go through Dollo trees and get the OG loss per species
## to later compare with illogical loss of interactions
############################################################
import sys
from ete3 import Tree
import pandas as pd
import random

dollo_file = sys.argv[1]
leca_file = sys.argv[2]
out_file = sys.argv[3]

#leca OGS
leca_dict = {}
leca_file = open(leca_file, "r")
for lines in leca_file:
    line = lines.rstrip()
    leca_dict[line] = 0

print("leca_dict done", len(leca_dict))
#dollo trees for OGs to dictionary per og
tree_dict = {}
dollo_tree = open(dollo_file, "r")
dollo_tree.readline()
for lines in dollo_tree:
    line = lines.rstrip().split("\t")
    OG = line[0]
    tree = line[1]
    if OG in leca_dict:
        tree_dict[OG] = tree
print("tree dict done", len(tree_dict))

for og in leca_dict:
    if og not in tree_dict:
        print("OG is: ", og)
#leaves = [x.name for x in Tree(tree_dict[random.choice(list(tree_dict.keys()))], format = 1).iter_leaves()]
#print(leaves)
species_loss_d = {}

for OG, tree in tree_dict.items():
    tree_structure = Tree(tree, format = 1)
    #lineage and clade loss --> independent loss
    #leaves = []
    for leaf in tree_structure.iter_leaves():
        #leaves += [leaf.name]
        species = leaf.name
        if species not in species_loss_d: #make dictionary
            species_loss_d[species] = {"species_loss": 0, "clade_loss": 0, "leca_present": 0}
        if (leaf.event == 'loss'): #every leaf with loss is a single loss and not ancestral, and thus species speciifc
            species_loss_d[species]["species_loss"] += 1
        elif (leaf.event == 'ancestral_loss'): #ancestral loss (not weird --> 0)
            species_loss_d[species]["clade_loss"] += 1
        else: #OG present in species
            species_loss_d[species]["leca_present"] += 1


species_loss_df = pd.DataFrame.from_dict(species_loss_d, orient='index') #,orient='index'
species_loss_df.index.name = "species"
print(species_loss_df)
species_loss_df.to_csv(out_file)
