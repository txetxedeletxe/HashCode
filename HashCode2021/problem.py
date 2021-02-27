import sys
def read_instance(stream=sys.stdin):
    sim_duration, n_nodes, n_edges, n_cars, bonus = map(int,stream.readline().split())
    
    #adj_list = [[]]*n_nodes
    streets = []


    name2id = {}
    id2name = []
    for edge_i in range(n_edges):
        s,e,sn,time = stream.readline().split()
        
        s,e,time = map(int,(s,e,time))
        
        name2id[sn] = edge_i
        id2name.append(sn)

        streets.append((s,e,time,edge_i))

    cars = []
    for _ in range(n_cars):
        rl = stream.readline().split()
        c = tuple(map(lambda x: name2id[x], rl[1:]))
        cars.append(c)

    return (sim_duration, n_nodes, bonus), (name2id,id2name), streets, cars

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
            end_of_road = car_pos[1] == 0 or (day - car_pos[0] >= )

def write_solution(instance, solution, stream=sys.stdout):
    stream.write(str(len(instance)))
    stream.write("\n")
    
    for inter in solution:
        stream.write(str(inter[0]))
        stream.write("\n")

        stream.write(str(len(inter[1])))
        stream.write("\n")

        for street in inter[1]:
            stream.write(instance[1][1][street[0]])
            stream.write(" ")
            stream.write(str(street[1]))
            stream.write("\n")


if __name__ == "__main__":
    ri = read_instance()
    print(ri)