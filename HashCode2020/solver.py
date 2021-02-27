#!/usr/bin/env python
import sys
from argparse import ArgumentParser

import numpy as np
from tqdm import tqdm

from problem import read_instance, write_solution, eval_sol


def signup_criterion1(instance, lib):
    return np.sum(instance.book_scores[instance.lib_books[lib]])

def signup_criterion2(instance, lib):
    return np.sum(instance.book_scores[instance.lib_books[lib]] / instance.book_frequencies[instance.lib_books[lib]]) - instance.lib_signups[lib]

def signup_criterion3(instance, lib):
    return np.average(instance.book_scores[instance.lib_books[lib]] - instance.book_frequencies[instance.lib_books[lib]]) * inst.lib_ships[lib] + instance.lib_signups[lib]

def signup_criterion4(instance, lib):
    return np.sum(np.sort(instance.book_scores[instance.lib_books[lib]] / instance.book_frequencies[instance.lib_books[lib]])[:-inst.n_days*inst.lib_ships[lib]]) * inst.lib_ships[lib] + instance.lib_signups[lib] 

def signup_critC(instance, lib):
    return instance.lib_book_counts[lib] - instance.lib_signups[lib]*8 + np.average(instance.book_scores[instance.lib_books[lib]]) 

def get_signups(instance, criterion=signup_critC):

    libraries = list(range(instance.n_lib))
    libraries.sort(key=lambda x: criterion(instance,x), reverse=True)
    return libraries

def get_scans(instance, signup_order):

    scanned_set = set()
    available_lib = []
    last_signup = -1

    lib_book_index = np.zeros(instance.n_lib, dtype=np.int32)
    lib_books_chosen = [[] for _ in range(instance.n_lib)]

    for day in tqdm(range(instance.n_days)):

        # Scan the books
        for lib in available_lib:
            if lib_book_index[lib] == instance.lib_book_counts[lib]:
                continue
            for _ in range(instance.lib_ships[lib]):
                for book_i in range(lib_book_index[lib],instance.lib_book_counts[lib]): 
                    lib_book_index[lib] = book_i+1       
                    book = instance.lib_books[lib][book_i]
                    if book not in scanned_set:
                        lib_books_chosen[lib].append(book)
                        scanned_set.add(book)
                        break
                    
        #print(len(available_lib))
        #print(len(scanned_set))

        if len(available_lib) == instance.n_lib:
            continue

        next_signup_lib = signup_order[len(available_lib)]
        signup_duration = instance.lib_signups[next_signup_lib]

        if day == last_signup + signup_duration:
            available_lib.append(next_signup_lib)
            last_signup = day

    lib_books_chosen = list(map(lambda x: lib_books_chosen[x], signup_order))

    return available_lib, lib_books_chosen



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-if","--inputfile",dest="if_",help="Input file to read the instance from (stdin if not specified)")
    parser.add_argument("-of","--outputfile",dest="of_",help="Output file to write the solution to (stdout if not specified)")

    args = parser.parse_args()

    if_, of_ = sys.stdin, sys.stdout
    if args.if_:    if_ = open(args.if_)
    if args.of_:    of_ = open(args.of_, "w+")

    inst = read_instance(if_)
    sign_up = get_signups(inst)
    sol = get_scans(inst,sign_up)
    eval1 = eval_sol(inst, sol)
    write_solution(sol, of_)
    
    if_.close()
    of_.close()

