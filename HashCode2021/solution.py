from problem import *
from tqdm import tqdm
def trivial_sol(instance):
    
    streets = instance[2]
    id2name = instance[1][1]

    sol = []
    for inter in tqdm(range(instance[0][1])):
        end_street = filter(lambda x: x[1] == inter, streets)
        s = [inter,tuple(map(lambda x: (x[-1],1),end_street))]

        sol.append(s)

    return sol

if __name__ == "__main__":
    ri = read_instance()
    sol = trivial_sol(ri)
    write_solution(ri,sol)