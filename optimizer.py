# ASSUMPTIONS:
# All teachers can in theory teach all subjects
# There are at least as many teachers as there are classes

import math
import random

class Optimizer:
    def __init__(self, params):
        self.num_gens = params[0]
        self.num_ents = params[1]
        self.muatation_rate = params[2]
        self.elitism_degree = params[3]

    def run(self, reqs, num_slots, prefered_subjects):
        teachers = list(map(lambda x: x[0], prefered_subjects))
        curr_gen_ents = self.__generate_initial_ents(reqs, num_slots, teachers)
        for i in range(self.num_gens):
            old_gen_ents = curr_gen_ents
            curr_gen_ents = self.__mutate_all(curr_gen_ents, num_slots, teachers)
            curr_gen_ents = self.__cross_over_all(curr_gen_ents)
            # elitism 
            num_old_gen = math.floor(self.num_ents * self.elitism_degree)
            num_curr_gen = self.num_ents - num_old_gen
            sorted_old_gen = old_gen_ents.sort(key=lambda x: self.__fitness(x))
            sorted_curr_gen = curr_gen_ents.sort(key=lambda x: self.__fitness(x))
            curr_gen_ents = sorted_old_gen[0:num_old_gen] + sorted_curr_gen[0:num_curr_gen]
        return curr_gen_ents

    def __generate_initial_ents(self, reqs, num_slots, teachers):
        num_classes = len(reqs)
        ents = []
        for i in range(self.num_ents):
            # fill the school table with subjects
            school_timetable = []
            for j in range(num_classes):
                curr_class_reqs = reqs[j]
                expanded_reqs = self.__flatten(list(map(self.__expand, curr_class_reqs)))
                # pad class table with free slots
                if len(expanded_reqs) < num_slots:
                    expanded_reqs += "Free" * (num_slots - len(expanded_reqs))
                random.shuffle(expanded_reqs)
                school_timetable.append(expanded_reqs)
            # fill the school table with teachers
            for i in range(num_slots):
                random.shuffle(teachers)
                for j in range(num_classes):
                    school_timetable[j][i] = (school_timetable[j][i], teachers[j])
            ents.append(school_timetable)
        return ents

    def __expand(req):
        subj = req[0]
        num_repetitions = int(req[1])
        return subj * num_repetitions

    def __flatten(l):
        res = []
        for sublist in l:
            res += sublist
        return res

    def __mutate_all(self, ents, num_slots, teachers):
        mutated_ents = []
        for ent in ents:
            rand_num = random.uniform(0, 1)
            if rand_num <= self.muatation_rate:
                mutated_ents.append(self.__mutate_one(ent, num_slots, teachers))
            else:
                mutated_ents.append(ent)
        return mutated_ents

    def __mutate_one(ent, num_slots, teachers):
        num_classes = len(ent)
        row_num = random.randrange(0, num_slots - 1)
        random.shuffle(teachers)
        for j in range(num_classes):
            ent[j][row_num] = (ent[j][row_num], teachers[j])

    def __cross_over_all(self, ents):
        # enforcing even number of ents per generation simplifies this method a bit
        assert(len(ents) % 2 == 0)
        random.shuffle(ents)
        crossed_ents = []
        for i in range(len(ents)/2):
            crossed_ents.append(self.__cross_over_two([ents[i], ents[i + 1]]))

    def __cross_over_two(ents):
        pass

    def __fitness(ent):
        pass