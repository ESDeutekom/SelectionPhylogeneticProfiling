# SelectionPhylogeneticProfiling

<p align="center"><img src="Workflow.png" width="850" /></p>


Manuscript: "Phylogenetic profiling in eukaryotes: The effect of species, orthologous group, and interactome selection on protein interaction prediction"
Authors: E.S. Deutekom, T.J.P. van Dam, B. Snel

## Disclaimer
This serves to share code and data for reproducibility.
Due to the amount of data, we cannot share all the data. Most data is readily available. Any additional (pre-made) data can be shared upon request.

## Contained directories and files
Main analsyis notebook: Improving_prediction_Sonic_final.ipynb

### Code directory
Code at least needed for reproducibility, used outside of the jupyter notebook for the analyses.

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
All pre-made files can be sent upon request. All data can be reproduced using the code provided here and previous work done in https://github.com/ESDeutekom/ComparingOrthologies/tree/master/eukarya/scripts_nonsql

#### Files in this analysis that can be downloaded
- BIOGRID Homo sapiens: 3.5.172.tab2.txt
- BIOGRID Saccharomyces cerevisiae S288c: 3.5.175.tab2.txt
- Orthogroup and leca orthogroup files: https://github.com/ESDeutekom/ComparingOrthologies/tree/master/eukarya/annotations
  - The phylogenetic profiles can also be made using the files and code in this previous repo
