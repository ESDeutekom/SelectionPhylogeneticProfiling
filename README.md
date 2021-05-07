# SelectionPhylogeneticProfiling

<p align="center"><img src="Workflow.png" width="850" /></p>


Manuscript: "Phylogenetic profiling in eukaryotes: The effect of species, orthologous group, and interactome selection on protein interaction prediction"
Authors: E.S. Deutekom, T.J.P. van Dam, B. Snel

## Disclaimer
This serves to share code and data for reproducibility.

## Contained directories and files
Main analysis notebook: Improving_prediction_Sonic_final.ipynb
Download data at https://doi.org/10.6084/m9.figshare.14500146 as is. Add notebook to Sonicparanoid or Broccoli folder. 

### Code
Code at least needed for reproducibility, used outside of the jupyter notebook for the analyses.
Previous work was done using code from: https://github.com/ESDeutekom/ComparingOrthologies/tree/master/eukarya/scripts_nonsql

#### Software and tools in analyses
- python		3.7.6

##### Python packages
- ete3			    3.1.1
- matplotlib 		3.1.2
- numpy			    1.18.1
- pandas		    1.0.1
- scipy			    1.4.1
- seaborn       0.11.1   
- scikit-learn  0.22.2. 

### Data

All data can be reproduced using the code provided here and previous work done in https://github.com/ESDeutekom/ComparingOrthologies/

Any data can also be sent upon request.

#### Files in this analysis that can be downloaded
- BIOGRID Homo sapiens: 3.5.172.tab2.txt (https://thebiogrid.org).
- BIOGRID Saccharomyces cerevisiae S288c: 3.5.175.tab2.txt (https://thebiogrid.org).
- All pre-made files that are needed to reproduce the main results for Sonicparanoid inferred OGs in the jupyter notebook are shared with figshare (https://doi.org/10.6084/m9.figshare.14500146).
- OG files and LECA OG files: 
  - Sonicparanoid: 
    - https://github.com/ESDeutekom/ComparingOrthologies/blob/master/eukarya/annotations/Orthogroups_Sonicparanoid_sensitive.txt
    - https://github.com/ESDeutekom/ComparingOrthologies/blob/master/eukarya/annotations/leca_orthologous_group_list_Sonicparanoid_sensitive
  - Broccoli: 
    - https://github.com/ESDeutekom/ComparingOrthologies/blob/master/eukarya/annotations/Orthogroups_broccoli.txt
    - https://github.com/ESDeutekom/ComparingOrthologies/blob/master/eukarya/annotations/leca_orthologous_group_list_broccoli 
