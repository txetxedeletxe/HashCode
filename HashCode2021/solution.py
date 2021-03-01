from tqdm import tqdm

import numpy as np

from problem import *

## Top level 
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
                                    processed_instance = {}, 
                                    sched_function=lambda intersect: (np.array([]),np.array([]))):
    # Unpack instance
    problem, streets, cars, meta = instance
    sim_duration, n_nodes, bonus = problem
    streets_start, streets_end, streets_time = streets
    id2name = meta

    # Create solution
    sol_ids = []
    sol_scheds = []
    for inter in tqdm(range(n_nodes)):
        sched_streets, sched_times = sched_function(inter)
        
        if len(sched_streets) == 0:
            continue

        sched = (sched_streets,sched_times)

        sol_ids.append(inter)
        sol_scheds.append(sched)
        
    return sol_ids, sol_scheds

# Scheduler classes
## Abstract
class AbstractScheduler(object):
    def __init__(self, instance, processed_instance={}):
        self.instance = instance
        self.process_instance = processed_instance


class IntersectionScheduler(AbstractScheduler):
    def __init__(self, instance, processed_instance):
        super().__init__(instance,processed_instance)
        
        self.streets_in = processed_instance["streets_in"]

    def __call__(self,intersection):
        inter_ids, inter_sched = self.schedule_intersection(intersection)
        in_sched = inter_sched != 0
        return inter_ids[in_sched], inter_sched[in_sched]

    def schedule_intersection(self,intersection):
        return np.array([]), np.array([]) # Trivial solution, no scheduling

class OrderedIntersectionScheduler(IntersectionScheduler):
    def __init__(self, instance, processed_instance):
        super().__init__(instance,processed_instance)
        
    def schedule_intersection(self,intersection):
        streets_in = self.streets_in[intersection]        
        return self.schedule_streets(streets_in)

    def schedule_streets(self,streets_in):
        return np.array([]), np.array([]) # Trivial solution, no scheduling

class UnorderedIntersectionScheduler(IntersectionScheduler):
    def __init__(self, instance, processed_instance):
        super().__init__(instance,processed_instance)

    def schedule_intersection(self,intersection):
        streets_in = self.streets_in[intersection]        
        return streets_in, self.schedule_streets(streets_in)

    def schedule_streets(self,streets_in):
        return np.zeros_like(streets_in) # Trivial solution, no scheduling

## Decorator classes
class ZeroTrafficUnscheduler(IntersectionScheduler):
    def __init__(self,instance, processed_instance, i_sched):
        super().__init__(instance,processed_instance)

        self.car_count_street = processed_instance["car_count_street"]

        self.i_sched = i_sched
    
    def schedule_intersection(self,intersect):
        inter_ids, inter_sched = self.i_sched(intersect)
        non_zero = self.car_count_street[inter_ids] != 0
        return inter_ids[non_zero], inter_sched[non_zero]


## Concrete
class AllOneIntersectionScheduler(UnorderedIntersectionScheduler):
    def __init__(self, instance, processed_instance):
        super().__init__(instance,processed_instance)
        
    def schedule_streets(self,streets):
        return np.ones_like(streets)

class TotalCarsIntersectionScheduler(UnorderedIntersectionScheduler):
    def __init__(self, instance, processed_instance):
        super().__init__(instance,processed_instance)
        
        self.car_count = processed_instance["car_count_street"]
        
    def schedule_streets(self,streets):
        return self.car_count[streets]

class MaxTrafficScheduler(AbstractScheduler):
    def __init__(self, instance, processed_instance):
        super().__init__(instance,processed_instance)
        
        self.traffic = processed_instance["traffics"]

    def __call__(self,streets):
        return np.max(self.traffic[streets],axis=1)



if __name__ == "__main__":
    inst = read_instance()

    p_inst = process_instance(inst)

    sched = AllOneIntersectionScheduler(inst,p_inst)
    sched = ZeroTrafficUnscheduler(inst,p_inst,sched)

    sol = intersection_local_scheduling(inst, p_inst, sched)
    
    write_solution(inst,sol)