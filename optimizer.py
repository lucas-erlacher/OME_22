import math

class Optimizer:
    def __init__(self, params):
        self.num_gens = params[0]
        self.num_ents = params[1]
        self.muatation_rate = params[2]
        self.elitism_degree = params[3]

    def run(self, reqs):
        curr_gen_ents = self.__generate_initial_ents(reqs)
        for i in range(self.num_gens):
            old_gen_ents = curr_gen_ents
            curr_gen_ents = self.__mutate(curr_gen_ents)
            curr_gen_ents = self.__cross_over(curr_gen_ents)
            # elitism 
            num_old_gen = math.floor(self.num_ents * self.elitism_degree)
            num_curr_gen = self.num_ents - num_old_gen
            sorted_old_gen = old_gen_ents.sort(key=lambda x: self.__fitness(x))
            sorted_curr_gen = curr_gen_ents.sort(key=lambda x: self.__fitness(x))
            curr_gen_ents = sorted_old_gen[0:num_old_gen] + sorted_curr_gen[0:num_curr_gen]
        print(curr_gen_ents)

    def __generate_initial_ents(reqs):
        pass

    def __mutate(ents):
        pass    

    def __cross_over(ents):
        pass  

    def __fitness(ent):
        pass