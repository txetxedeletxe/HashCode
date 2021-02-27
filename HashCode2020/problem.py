#!/usr/bin/env python
"""This module contains functions for manipulating problem instances and solutions to those instances. It only contains tools
that have to do with the problem description, and does not include any implementation of an algorithm to solve the problem."""
import sys
from argparse import ArgumentParser

import types

import numpy as np

## PROBLEM INSTANCES
def read_instance(stream=sys.stdin):
    """Read an instance from 'stream' (stdin by default) in the problem specified format. Returns a
    namespace object $inst$ containing the data of the instance:
    
        inst.n_books (int): number of different books in total

        inst.n_lib (int):   number of libraries

        inst.n_days (int):  budget of days to scan books

        inst.book_scores (np.array(ndim=1,dtype=np.int32)): 
            value of each book.
            inst.book_scores[i] (with i < inst.n_books) is the value of the i-th book

        inst.lib_book_counts (np.array(ndim=1,dtype=np.int32)): 
            number of books in each library. 
            inst.lib_book_counts[i] (with i < inst.n_lib) is the number of books in the i-th library.

        inst.lib_signups (np.array(ndim=1,dtype=np.int32)):   
            number of days to signup in each library.
            inst.lib_signups[i] (with i < inst.n_lib) is the number of days of delay to signup in the i-th library.
                                        
        inst.lib_ships (np.array(ndim=1,dtype=np.int32)): 
            number of books that can be shipped every day.
            inst.lib_ships[i] (with i < inst.n_lib) is the number of books that the i-th library can ship each day.
                                    
        inst.lib_books (np.array(ndim=2,dtype=np.int32)):   
            what books are available in what libraries.
            k = inst.lib_books[i][j] (with i < n_lib and j < inst.lib_book_counts[i]) is the index k (with k < inst.n_books)
            of a book that is available in the i-th library, the books are sorted in descending order.
                                            
        inst.book_frequencies (np.array(ndim=1,dtype=np.int32)):
            In how many libraries does each book appear.
            inst.book_frequencies[i] (with i < inst.n_books) is the number of libraries in which the i-th book is available. 
        """
    
    # Read first header (number of books, number of libs, budget of days)
    line = stream.readline()
    n_books, n_lib, n_days = line.rstrip().split()
    n_books, n_lib, n_days = int(n_books), int(n_lib), int(n_days)

    # Read the scores of the books
    line = stream.readline()
    book_scores = np.array([int(sc) for sc in line.rstrip().split()], dtype=np.int32)

    # Init the book frequencies to 0
    book_frequencies = np.zeros(n_books, dtype=np.float32)

    lib_book_counts = []
    lib_signups = []
    lib_shipss = []

    lib_books = []

    for _ in range(n_lib):
        # Read initial header of library
        line = stream.readline()
        lib_book_count, lib_signup, lib_ships = line.rstrip().split()
        lib_book_count, lib_signup, lib_ships = int(lib_book_count), int(lib_signup), int(lib_ships)

        lib_book_counts.append(lib_book_count)
        lib_signups.append(lib_signup)
        lib_shipss.append(lib_ships)

        # Read book offer of library
        line = stream.readline()
        lib_book = [int(book) for book in line.rstrip().split()]
        lib_book.sort(key=lambda x: book_scores[x], reverse=True)
        lib_book = np.array(lib_book, dtype=np.int32)
        lib_books.append(lib_book)

        book_frequencies[lib_book] += 1

    # Wrap list in numpy arrays
    lib_book_counts = np.array(lib_book_counts, dtype=np.int32)
    lib_signups = np.array(lib_signups, dtype=np.int32)
    lib_shipss = np.array(lib_shipss, dtype=np.int32)

    # Pack data in a namespace object
    inst = types.SimpleNamespace()

    inst.n_books = n_books
    inst.n_lib = n_lib
    inst.n_days = n_days
    inst.book_scores = book_scores
    inst.lib_book_counts = lib_book_counts
    inst.lib_signups = lib_signups
    inst.lib_ships = lib_shipss

    inst.lib_books = lib_books
    inst.book_frequencies = book_frequencies

    return inst


## SOLUTIONS
def read_solution(stream=sys.stdin):
    """Read a solution from 'stream' (stdin by default) in the problem specified format. Returns a
    2-tuple "(sign_up_order, book_order)" containing a representation of a solution:
    
        sign_up_order (list[int]): 
            order in which to sign up to the libraries.
            sign_up_order[i] is the index of the library to sign up the i-th
            
        book_order (list[list[int]]):
            order in which to scan the books of each library (empty if not signed-up).
            book_order[i][j] is the index of the book to scan the j-th in the library that was subscribed the i-th """

    line = stream.readline()
    sub_count = int(line.rstrip())

    sign_up_order = []
    book_order = []
    for _ in range(sub_count):
        line = stream.readline()
        library_id, _ = line.rstrip().split()
        library_id = int(library_id)

        line = stream.readline()
        books = list(map(int, line.rstrip().split()))

        sign_up_order.append(library_id)
        book_order.append(books)

    return sign_up_order, book_order


def write_solution(sol, stream=sys.stdout):
    """A solution 'sol' is a 2-tuple (sign_up_order, book_order)
    This function writes the solution to the 'stream' (stdout by default) in the specified format:
    
        sign_up_order (list[int]): 
            order in which to sign up to the libraries.
            sign_up_order[i] is the index of the library to sign up the i-th
            
        book_order (list[list[int]]):
            order in which to scan the books of each library (empty if not signed-up).
            book_order[i][j] is the index of the book to scan the j-th in the library that was subscribed the i-th
    """

    sol_it = tuple(filter(lambda x: bool(x[1]),zip(*sol)))

    stream.write(f"{len(sol_it)}\n") # write header

    # For each signup, write description of scanned books
    for sign_up, books in sol_it:
        stream.write(f"{sign_up} {len(books)}\n")
        stream.write(" ".join(map(str,books)))
        stream.write("\n")
    

def eval_sol(inst, sol):
    """Given an instance of the problem 'inst' and a solution 'sol' in the internal representation, and 'sol' not
    violating any constraints and with no repetitions, return the objective value of the solution."""
    return sum((np.sum(inst.book_scores[books]) for books in sol[1]))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("instance", help="Path of an instance-file of the problem")
    parser.add_argument("solution", help="Path of a solution-file for the given instance")

    args = parser.parse_args()

    inst = read_instance(open(args.instance))
    sol = read_solution(open(args.solution))

    print(eval_sol(inst, sol))




