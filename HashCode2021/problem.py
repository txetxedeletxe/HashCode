import sys

import itertools as itools
import heapq

import numpy as np

## READ and WRITE instance and solutions
def read_instance(stream=sys.stdin):
    # Top level problem constants
    sim_duration, n_nodes, n_edges, n_cars, bonus = map(int,stream.readline().split())
    problem = (sim_duration, n_nodes, bonus)

    # Streets
    streets_start = []
    streets_end = []
    streets_time = []

    name2id = {}
    id2name = []
    for edge_i in range(n_edges):
        s,e,sn,time = stream.readline().split()
        
        s,e,time = map(int,(s,e,time))
        
        name2id[sn] = edge_i
        id2name.append(sn)

        streets_start.append(s)
        streets_end.append(e)
        streets_time.append(time)

    streets = tuple(map(np.array,(streets_start, streets_end, streets_time)))
    meta = id2name

    cars = []
    for _ in range(n_cars):
        rl = stream.readline().split()
        c = np.array(tuple(map(lambda x: name2id[x], rl[1:])))
        cars.append(c)

    return problem, streets, cars, meta

def write_solution(instance, solution, stream=sys.stdout):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    # Unpack solution
    sol_ids, sol_scheds = solution

    stream.write(str(len(sol_ids)))
    stream.write("\n")
    
    for sol_id, sol_sched in zip(sol_ids, sol_scheds):
        stream.write(str(sol_id))
        stream.write("\n")

        street_ids, street_scheds = sol_sched

        stream.write(str(len(street_ids)))
        stream.write("\n")

        for street_id, street_sched in zip(street_ids, street_scheds):
            stream.write(id2name[street_id])
            stream.write(" ")
            stream.write(str(street_sched))
            stream.write("\n")

# Instance processing
## Preprocessing
### No dependencies
def streets_in(instance):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    st_in = list(map(lambda x: list(),range(n_nodes)))
    for s_i, s_end in enumerate(streets_end):
        st_in[s_end].append(s_i)

    return list(map(np.array,st_in))

def cars_in_street(instance):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    cis = list(map(lambda x: list(),streets_start))
    for i, car in enumerate(cars):
        for s in car:
            cis[s].append(i)

    return list(map(np.array,cis))

def car_times(instance):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    return list(map(lambda x: streets_time[x],cars))

### Self dependencies
def car_count_street(instance,p_instance):
    cis = p_instance["cars_in_street"]
    return np.array(tuple(map(len,cis)))

def cum_car_times(instance,p_instance):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    ct = p_instance["car_times"]

    return list(map(lambda x: np.cumsum(x),ct))        

### Instance preprocessing frontend
def process_instance(instance):
    processed_instance = dict()

    processed_instance["streets_in"] = streets_in(instance)
    processed_instance["cars_in_street"] = cars_in_street(instance)
    processed_instance["car_times"] = car_times(instance)

    processed_instance["car_count_street"] = car_count_street(instance,processed_instance)
    processed_instance["cum_car_times"] = cum_car_times(instance,processed_instance)

    return processed_instance

## In the loop processing
def traffics(instance,p_instance,street):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    cis = p_instance["cars_in_street"][street]
    cct = p_instance["cum_car_times"][cis]
    

    traf = np.zeros((len(streets_start),sim_duration))
    for tt, car in zip(cct,cars):
        for ts,te,s in zip(tt[:-1],tt[1:],car[1:]):
            ts, te = ts - tt[0], min(te - tt[0], sim_duration-1)
            traf[s,ts] += 1
            traf[s,te] -= 1

    return np.cumsum(traf,axis=1)

## Evaluate solution
def score(instance, solution):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    

if __name__ == "__main__":
    ri = read_instance()
    print(ri)