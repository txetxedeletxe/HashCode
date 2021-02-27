import sys

import itertools as itools

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
        c = np.array(map(lambda x: name2id[x], rl[1:]))
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

## Instance processing
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

def process_instance(instance):
    processed_instance = dict()

    processed_instance["streets_in"] = streets_in(instance)

    return processed_instance


## Evaluate solution
def score(instance, solution):
    sim_duration, n_nodes , bonus = instance[0]
    streets, cars= instance[-2:]

    car_position = [(0,0)]*len(cars)

    for day in range(sim_duration):
        for car_i in range(len(cars)):
            car = cars[car_i]
            car_pos= car_position[car_i]
            
            # Has finished route
            if car_pos[1] == len(car): continue

            current_street_i = car[car_pos[1]]
            current_street = streets[current_street_i]

            # Is at the end of the road
            end_of_road = car_pos[1] == 0 or (day - car_pos[0] >= 0)




if __name__ == "__main__":
    ri = read_instance()
    print(ri)