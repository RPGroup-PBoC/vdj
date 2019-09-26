
# Probing the Sequence-Dependent Dynamics of Endogenous and Synthetic RSSs in V(D)J Recombination 

Welcome to the GitHub repository for our work on V(D)J recombination! This
repository contains the entire project history as well as curated scripts to
ensure computational reproducibility. The following sections will describe this
repository in detail. If anything remains unclear, please [open an
issue](https://github.com/RPGroup-PBoC/mwc_mutants/issues) and we'll respond as
quickly as we can. 


## Branches

This repository contains three unique branches -- `master`, `gh-pages`, and
`publication` (where you are now). The `master` branch is the primary branch of
the project and contains the entire history of our thought process including
exploratory data analysis and modeling attempts. The `gh-pages` branch contains
all files that constitute the [paper website](http://rpgroup.caltech.edu/vdj_recombination),
including all of the interactive figures. Finally, the `publication` branch
contains a curated list of all of the *processed* data files, final versions of
the figure-generating and analysis Python scripts, the Python software module
`vdj`, and the MATLAB module `tpm`. The `vdj` module is necessary to reproduce
the work in this paper and can be installed locally. 


## Installation

To reproduce this work, you must install the `vdj` python module -- a homegrown
software package written explicitly for this work. The various components are
described in `README.md` files within the `vdj` folder. To install this package
locally, the requirements can be installed via  the command line:

```
pip install -r requirements.txt
```

The `vdj` module itself can be installed locally by executing the following
command in the root directory (this directory). 

```
pip install -e ./
```

Both of these commands can be executed at once by running the `install.sh`
script in this repostiory, 

```
sh install.sh
```
in the root directory. When installed, a new folder `vdj.egg-info` will appear.
**Do not delete this folder as it is necessary to access the `vdj` software.**


## Repository Architecture

This repository is broken up into several directories and subdirectories. Please
see each directory individually for important notes. Below, we summarize the
contents of each folder. 

### `code`
This folder contains all of the *exectued* Python scripts used to reproduce the
findings in this work. These files are broken up further into several
subdirectories which separate the scripts by their function.

1. **`analysis`** \| Contains all Python scripts which perform data *analysis*
   procedures on pre-processed data (i.e., not raw image data). This includes
   scripts to perform bootstrapping of looping frequencies, generate posterior
   distributions for the cleavage probability, and parameter inference.
2. **`figures`** \| Contains all Python scripts which perform data
   *visualization* procedures. This includes the generation of all main and
   supplementary figures.
3. **`processing`** \| Contains a single script `compile_data.py` which reads
   through the pre-processed data files, stored as `.mat`, and extracts the
   important quantities.
4. **`interactives`** \| Contains all Python and JavaScript files to generate
   the interactive figures on the [paper
   website](https://rpgroup.caltech.edu/vdj_recombination).
5. **`stan`** \| Contains the inferential model used to estimate the
   paired-complex leaving rate. This is written in the [Stan probabilistic
   programming language](http://mc-stan.org) and is not directly executable. 

### `data`
This folder contains the processed data files needed to reproduce the figures in
this work. The pre-processed data for each mutant in each condition can be
downloaded as `.mat` files from the [CaltechDATA](http://data.caltech.edu)
research data repository under `DOI: 10.22002/D1.1288`. These files, as is described in 
`code/processing/README.md`, are generated by processing the raw image files
using the `tpm` MATLAB module. The raw image files are very large (~ 10 TB) and
are on cold storage. Image fils are available upon request.

### `figures`
This folder contains  `.pdf` files of all main and supplementary text figures.
The interactive figures are saved here as `.html` and are stand alone, meaning
that all data is encoded within the file. No code exists in this directory.  

### `vdj`
This is heart-and-soul of the repository. It contains a series of Python files
which define the myriad functions used in the processing, analysis, and
visualization of the data associated with this work. Please navigate to the
directory to see a description of its contents. 

### `tpm`
This contains all of the MATLAB `.m` files used to process the raw image files.
This code was used and described previously in [Lovely *et al.* PNAS 112 (14)
2015](https://www.pnas.org/content/112/14/E1715) and in the supplementary
material of [Johnson *et al.* Nucleic Acids Research 40 (16)
2012.](https://academic.oup.com/nar/article/40/16/7728/1028173).

## License
[![](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)

All creative works (writing, figures, etc) are licensed under a [Creative
Commons CC-BY 4.0 license](http://creativecommons.org/licenses/by/4.0/). All
software is distributed under the standard MIT license as follows:

```
Copyright 2019 The Authors 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
