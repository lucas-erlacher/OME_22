# ASSUMPTIONS:
# All teachers can in theory teach all subjects but are better in some subjects than others (relaxation of "teacher can only teach subjects x,y and z")
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
            curr_gen_ents = self.__cross_over_all(curr_gen_ents, teachers)
            # elitism 
            num_old_gen = math.floor(self.num_ents * self.elitism_degree)
            num_curr_gen = self.num_ents - num_old_gen
            sorted_old_gen = old_gen_ents.sort(key=lambda x: self.__fitness(x))
            sorted_curr_gen = curr_gen_ents.sort(key=lambda x: self.__fitness(x))
            curr_gen_ents = sorted_old_gen[0:num_old_gen] + sorted_curr_gen[0:num_curr_gen]
            # progress report: print the fitness of the top ent of each gen to see how things are evolving
            print(curr_gen_ents.sort(key=lambda x: self.__fitness(x))[0])
        # TODO: plot the evolution of fitness of top, worst and average ent fitness of each gen (gen_number on x-axis)

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
            crossed_ents += self.__cross_over_two([ents[i], ents[i + 1]])

    def __cross_over_two(self, ents, teachers):
        parent_1 = ents[0]
        parent_2 = ents[1]
        child_1 = []
        child_2 = []
        num_classes = len(parent_1)
        # contruct the children
        for i in range(num_classes):
            num = random.uniform(0, 1)
            if num < 0.5: 
                child_1.append(parent_1[i])
                child_2.append(parent_2[i])
            else:
                child_1.append(parent_2[i])
                child_2.append(parent_1[i])
        child_1 = self.__fix_teacher_conflicts(child_1, teachers)
        child_2 = self.__fix_teacher_conflicts(child_2, teachers)
        return [child_1, child_2]

    def __fix_teacher_conflicts(ent, teachers):
        num_classes = len(ent)
        num_slots = len(ent[0])
        for i in range(num_slots):
            for j in range(num_classes):
                for k in range(j + 1, num_classes):
                    # very lazy implementation by me
                    while ent[i][j][1] == ent[i][k][1]:
                        ent[i][k][1] = teachers[random.randrange(0, len(teachers) - 1)]

    def __fitness(ent):
        pass