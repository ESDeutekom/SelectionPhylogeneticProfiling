#!/hosts/linuxhome/scarab/eva2/Programs/miniconda3/bin/python
#python 3
import sys
from ete3 import Tree
import statistics as st

#################################################################
## Counting loss in dollo set by counting all losses in nodes
## For all non-leca OGs
################################################################

dollo_tree = sys.argv[1]
leca_file = sys.argv[2]
loss_out=sys.argv[3]

leca_dict = {}
leca_file = open(leca_file, "r")
for lines in leca_file:
    line = lines.rstrip()
    leca_dict[line] = 0

tree_dict = {}
dollo_tree = open(dollo_tree, "r")
dollo_tree.readline()
for lines in dollo_tree:
    line = lines.rstrip().split("\t")
    OG = line[0]
    tree = line[1]
    if OG not in leca_dict: #non leca OGS
        tree_dict[OG] = tree
print("Tree", len(tree_dict))

non_leca_dict = {}
for OG, tree in tree_dict.items():
    tree_structure = Tree(tree, format = 1)
    #lineage and clade loss --> independent loss
    lossClade = 0
    lossLineage = 0
    for node in tree_structure.traverse(strategy='preorder'):
        if not node.is_leaf(): #nodes that are leaf losses are not a clade. In this case node is the leaf
            if (node.event == "loss"): #if loss in node --> clade loss
                lossClade += 1
    for leaf in tree_structure.iter_leaves():
        if (leaf.event == 'loss'): #if loss in leaf --> lineage specific loss
            lossLineage += 1
    indep_loss = lossClade + lossLineage
    if OG in non_leca_dict:
        non_leca_dict += indep_loss
    else:
        non_leca_dict[OG] = indep_loss #add to non leca dict the amount of loss for leca og

total_indep_loss = 0
list_val = []
loss_out = open(loss_out, "w")
for key, value in non_leca_dict.items():
    loss_out.write('%s\t%.0f\n' % (key, value))
    list_val += [value]
    total_indep_loss += float(value)
loss_out.close()

print("Total independen loss: ", total_indep_loss)
print("Mean loss: ", st. mean(list_val))
print("Median loss: ", st.median(list_val))
print('Stdev: ', st.stdev(list_val))
