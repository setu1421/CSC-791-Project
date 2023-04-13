import pandas as pd
from explain import Explain, selects
from data import Data
from options import options
from stats import cliffsDelta, bootstrap
from tabulate import tabulate

help = """

project: multi-goal semi-supervised algorithms
(c) Setu Kumar Basak (Group 41)
  
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
  -f  --file        file to generate table of        = etc/data/auto2.csv
  -n  --Niter       number of iterations to run      = 2
  -w  --budget      budget of sampling               = 5
"""

def get_stats(data_array):
    # gets the average stats, given the data array objects
    res = {}
    # accumulate the stats
    for item in data_array:
        stats = item.stats()
        # update the stats
        for k,v in stats.items():
            res[k] = res.get(k,0) + v

    # right now, the stats are summed. change it to average
    for k,v in res.items():
        res[k] /= options["Niter"]
    return res


def saveToCSV(table, headers, budget, run):
    data_headers = ["type"] + headers + ["Avg evals"]
    data_df = pd.DataFrame(table, columns = data_headers)
    data_df["budget"] = budget
    data_df["run"] = run
    
    return data_df
    

def main():
    """
    `main` runs each algorithm for 20 iterations, on the given file dataset.

    It accumulates the results per each iteration, and compares the algorithms
    using cliffsDelta and bootstrap

    It then produces summatory stats, including a mean table (for each algorithm,
    summarize each y column and number of iterations)
    And a table comparing each algorithm to each other using cliffsDelta and bootstrap
    """

    options.parse_cli_settings(help)


    if options["help"]:
        print(help)
    else:

        results = {"all": [], "sway1": [], "xpln1": [], "sway2": [], "xpln2": [], "top": []}
        comparisons = [[["all", "all"],None], 
                       [["all", "sway1"],None],  
                       [["all", "sway2"],None], 
                       [["sway1", "sway2"],None],
                       [["sway1", "xpln1"],None],    
                       [["sway2", "xpln2"],None], 
                       [["sway1", "top"],None]]
        n_evals = {"all": 0, "sway1": 0, "xpln1": 0, "sway2": 0, "xpln2": 0, "top": 0}

        count = 0
        data=None
        final_df = pd.DataFrame()

        # do a while loop because sometimes explain can return -1
        while count < options["Niter"]:
            # read in the data
            data=Data(options["file"])
            # get the "all" and "sway" results
            best1,rest1,evals_sway1 = data.sway()
            best2,rest2,evals_sway2 = data.sway_dbscan()
            # get the "xpln1" results
            x1 = Explain(best1, rest1)
            rule1,_= x1.xpln(data,best1,rest1)
            # get the "xpln2" results
            x2 = Explain(best2, rest2)
            rule2,_= x2.xpln(data,best2,rest2)
            # if it was able to find a rule
            if rule1 != -1 and rule2 != -1:
                # get the best rows of that rule
                data1= Data(data,selects(rule1,data.rows))
                data2 = Data(data,selects(rule2,data.rows))

                results['all'].append(data)
                results['sway1'].append(best1)
                results['sway2'].append(best2)
                results['xpln1'].append(data1)
                results['xpln2'].append(data2)

                # get the "top" results by running the betters algorithm
                top2,_ = data.betters(len(best1.rows))
                top = Data(data,top2)
                results['top'].append(top)

                # accumulate the number of evals
                # for all: 0 evaluations 
                n_evals["all"] += 0
                n_evals["sway1"] += evals_sway1
                n_evals["sway2"] += evals_sway2
                # xpln uses the same number of evals since it just uses the data from
                # sway to generate rules, no extra evals needed
                n_evals["xpln1"] += evals_sway1
                n_evals["xpln2"] += evals_sway2
                n_evals["top"] += len(data.rows)

                # update comparisons
                for i in range(len(comparisons)):
                    [base, diff], result = comparisons[i]
                    # if they haven't been initialized, mark with true until we can prove false
                    if result == None:
                        comparisons[i][1] = ["=" for _ in range(len(data.cols.y))]
                    # for each column
                    for k in range(len(data.cols.y)):
                        # if not already marked as false
                        if comparisons[i][1][k] == "=":
                            # check if it is false
                            base_y, diff_y = results[base][count].cols.y[k],results[diff][count].cols.y[k]
                            equals = bootstrap(base_y.has(), diff_y.has()) and cliffsDelta(base_y.has(), diff_y.has())
                            if not equals:
                                if i == 0:
                                    # should never fail for all to all, unless sample size is large
                                    print("WARNING: all to all {} {} {}".format(i, k, "false"))
                                    print(f"all to all comparison failed for {results[base][count].cols.y[k].txt}")
                                comparisons[i][1][k] = "≠"
                count += 1

                # generate the stats table
                headers = [y.txt for y in data.cols.y]
                table = []
                # for each algorithm's results
                for k,v in results.items():
                    # set the row equal to the average stats
                    stats = get_stats(v)
                    stats_list = [k] + [stats[y] for y in headers]
                    # adds on the average number of evals
                    stats_list += [n_evals[k]/options["Niter"]]
                    
                    table.append(stats_list)
                
                print(tabulate(table, headers=headers+["Avg evals"],numalign="right"))
                print()
                current_df = saveToCSV(table, headers, 5, count)
                final_df = pd.concat([final_df, current_df], ignore_index = True)
                file_name = options["file"].strip().split("/")[-1].split(".")[0]
                final_df.to_csv("etc/out/budget/" + file_name + "_B" + str(options["budget"]) + ".csv", index = False)

        
        # generates the =/!= table
        table=[]
        # for each comparison of the algorithms
        #    append the = / !=
        for [base, diff], result in comparisons:
            table.append([f"{base} to {diff}"] + result)
        print(tabulate(table, headers=headers,numalign="right"))


main()
