
# CSC-791-Project: A Multi-objective Semi-supervised Explanation System


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
[![GitHub Workflow](https://github.com/setu1421/CSC-791/actions/workflows/python-app.yml/badge.svg)](https://github.com/setu1421/CSC-791-Project/actions/workflows/python-app.yml)
[![DOI](https://zenodo.org/badge/589857531.svg)](https://doi.org/10.5281/zenodo.7831672)
[![GitHub issues](https://img.shields.io/github/issues-raw/setu1421/CSC-791)](https://github.com/setu1421/CSC-791-Project/issues)

## Setup

Prerequisites:
* [Python](https://www.python.org/downloads/) >= 3.9
* [pip](https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/) >= 22.2.9

### How to Run:

 - Install the requirements: `pip install -r requirements.txt`
 - Change directory to `src`
 - Run  `python main.py`  to generate tables for the  `auto2.csv`  file
 - Run `python main.py --help`  to view possible configuration values

```
USAGE: python3 main.py [OPTIONS] [-g ACTIONS]

OPTIONS:
  -b  --bins        initial number of bins           = 16
  -c  --cliff       cliff's delta threshold          = .147
  -d  --D           different is over sd*d           = .35
  -F  --Far         distance to distant              = .95
  -h  --help        show help                        = false
  -H  --Halves      search space for clustering      = 512
  -I  --IMin        size of smallest cluster         = .5
  -M  --Max         numbers                          = 512
  -p  --P           dist coefficient                 = 2
  -R  --Rest        how many of rest to sample       = 3
  -r  --reuse       child splits reuse a parent pole = true
  -x  --Bootstrap   number of samples to bootstrap   = 512    
  -o  --Conf        confidence interval              = 0.05
  -f  --file        file to generate table of        = etc/data/SSN.csv
  -n  --Niter       number of iterations to run      = 20
  -w  --budget      budget of sampling               = 20
  -r  --best        choose the best row of sway      = false    
  ```

### Notes:

 1. Source codes are present in [src](https://github.com/setu1421/CSC-791-Project/tree/main/src) folder.
 2. Datasets are present in [etc/data](https://github.com/setu1421/CSC-791-Project/tree/main/etc/data) folder
 3. Outputs for each dataset and different budgets are present in [etc/out](https://github.com/setu1421/CSC-791-Project/tree/main/etc/out) folder

## Output:
The output of running `sway1` and `sway2` method for `auto2.csv` file:

```
---------------Start of Run: 20 , Budget: 10  -------------

         CityMPG+    HighwayMPG+    Weight-    Class-    Avg evals
-----  ----------  -------------  ---------  --------  -----------
all            21             28       3040      17.7            0
sway1       28.05           33.5    2303.25     9.315            4
xpln1        28.9           33.1     2317.5     9.885            4
sway2        27.8          33.55    2358.25      9.93            0
xpln2       28.45          33.25     2399.5    11.115            0
top            31             37       2055       8.6           93

                CityMPG+    HighwayMPG+    Weight-    Class-
--------------  ----------  -------------  ---------  --------
all to all      =           =              =          =
all to sway1    ≠           ≠              ≠          ≠
all to sway2    ≠           ≠              ≠          ≠
sway1 to sway2  ≠           ≠              ≠          ≠
sway1 to xpln1  ≠           ≠              ≠          ≠
sway2 to xpln2  ≠           ≠              ≠          ≠
sway1 to top    ≠           ≠              ≠          ≠
---------------End of Run: 20 , Budget: 10  -------------
```

## License:
This project is licensed under the terms of the MIT license. Please check [LICENSE](https://github.com/setu1421/CSC-791-Project/blob/main/LICENSE) for more details. 
## Roadmap:
  - [List of Roadmap and their corresponding open issues](https://github.com/setu1421/CSC-791-Project/issues)
## Authors:
 - Setu Kumar Basak (sbasak4@ncsu.edu)
## How to Contribute:
 Please check [here](https://github.com/setu1421/CSC-791-Project/blob/main/CONTRIBUTING.md). 
