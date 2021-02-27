#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from json import dumps

import numpy as np

from problem import read_instance


def standard_metrics(l):
    r = {}
    r["count"] = len(l)
    r["total"] = float(np.sum(l))
    r["mean"] = float(np.average(l))
    r["std"] = float(np.std(l))
    r["max"] = float(np.max(l))
    r["min"] = float(np.min(l))

    return r

def pearson_r(x,y):
    mean_x, mean_y = np.average(x), np.average(y)
    std_x, std_y = np.std(x), np.std(y)

    return float(np.average((x*y + mean_x*mean_y - (x*mean_y+y*mean_x))/(std_x*std_y)))

def correlation_mat(vars):
    mat=[]
    for var1 in vars:
        m = []
        for var2 in vars:
            m.append(pearson_r(var1,var2))
        mat.append(m)
    return mat

class NamedCartesianMat:
    def __init__(self, mat, names):
        self.mat = mat
        self.names = names

    def jsonable(self):
        return dict(mat=self.mat,names=self.names)

    def __str__(self):
        format = "{}"*(len(self.names) + 1)
        
        s = []

        s.append(format.format("",*self.names))
        for name,m in zip(self.names,self.mat):
            s.append(format.format(name,*m))
            
        return "\n".join(s)

def library_score_mat(inst):
    return list(map(lambda x:list(map(lambda y: inst.book_scores[y],x)),inst.lib_books))


def compute_metrics(inst):
    metrics = {}
    # Meta
    meta = {}
    meta["book_count"] = inst.n_books
    meta["lib_count"] = inst.n_lib
    meta["day_budget"] = inst.n_days

    metrics["meta"] = meta

    # Books 
    books = {}
    books["scores"] = standard_metrics(inst.book_scores)
    books["frequencies"] = standard_metrics(inst.book_frequencies)

    books["correlation"] = NamedCartesianMat(correlation_mat((inst.book_scores,inst.book_frequencies)),("scores","frequencies"))
    books["correlation"] = books["correlation"].jsonable()

    metrics["books"] = books

    # Libraries
    libraries = {}
    libraries["book_counts"] = standard_metrics(inst.lib_book_counts)
    libraries["signups"] = standard_metrics(inst.lib_signups)
    libraries["ships"] = standard_metrics(inst.lib_ships)
    
    libraries["correlation"] = NamedCartesianMat(correlation_mat((inst.lib_book_counts,inst.lib_signups,inst.lib_ships)),
                                        ("book_counts","signups","ships"))
    libraries["correlation"] = libraries["correlation"].jsonable()

    ## Library scores
    library_scores = {}
    lsm = library_score_mat(inst)
    library_scores["sums"] = standard_metrics(list(map(lambda x: np.sum(x),lsm)))
    library_scores["average"] = standard_metrics(list(map(lambda x: np.average(x),lsm)))
    library_scores["std"] = standard_metrics(list(map(lambda x: np.std(x),lsm)))
    library_scores["max"] = standard_metrics(list(map(lambda x: np.max(x),lsm)))
    library_scores["min"] = standard_metrics(list(map(lambda x: np.min(x),lsm)))

    libraries["scores"] = library_scores

    metrics["libraries"] = libraries

    return metrics

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-if","--inputfile",dest="if_",help="Input file to read the instance from (stdin if not specified)")
    parser.add_argument("-of","--outputfile",dest="of_",help="Output file to write the metrics to (stdout if not specified)")

    args = parser.parse_args()

    if_, of_ = sys.stdin, sys.stdout
    if args.if_:    if_ = open(args.if_)
    if args.of_:    of_ = open(args.of_, "w+")

    inst = read_instance(if_)

    metrics = compute_metrics(inst)    

    of_.write(dumps(metrics,sort_keys=True, indent=4))
    of_.write("\n")

    if_.close()
    of_.close()
     


