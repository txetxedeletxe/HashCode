from tqdm import tqdm

import numpy as np

from problem import *

def trivial_sol(instance, processed_instance):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    # Get necessary processed values
    streets_in = processed_instance["streets_in"]

    # Create solution
    sol_ids = []
    sol_scheds = []
    for inter in tqdm(range(n_nodes)):
        end_street = streets_in[inter]
        
        sched = (end_street,np.ones_like(end_street))

        sol_ids.append(inter)
        sol_scheds.append(sched)

    return sol_ids, sol_scheds


def intersection_local_scheduling(instance, 
                                    processed_instance, 
                                    sched_function=lambda inst, p_inst, streets: np.ones_like(streets)):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    # Get necessary processed values
    streets_in = processed_instance["streets_in"]

    # Create solution
    sol_ids = []
    sol_scheds = []
    for inter in tqdm(range(n_nodes)):
        end_street = streets_in[inter]
        
        times = sched_function(instance,processed_instance,end_street)
        sched = (end_street,times)

        sol_ids.append(inter)
        sol_scheds.append(sched)

    return sol_ids, sol_scheds

if __name__ == "__main__":
    inst = read_instance()
    pro_inst = process_instance(inst)
    sol = intersection_local_scheduling(inst, pro_inst)
    write_solution(inst,sol)