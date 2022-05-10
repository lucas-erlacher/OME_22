# ASSUMPTIONS:
# All teachers can in theory teach all subjects but are better in some subjects than others (relaxation of "teacher can only teach subjects x,y and z")
# There are at least as many teachers as there are classes

import math
import random
import matplotlib.pyplot as plt

class Optimizer:
    def __init__(self, params):
        self.num_gens = params[0]
        self.num_ents = params[1]
        self.muatation_rate = params[2]
        self.elitism_degree = params[3]

    def run(self, reqs, num_slots, prefered_subjects):
        teachers = list(prefered_subjects.keys())
        curr_gen_ents = self.__generate_initial_ents(reqs, num_slots, teachers)
        top_ents = []
        worst_ents = []
        for i in range(self.num_gens):
            old_gen_ents = curr_gen_ents
            curr_gen_ents = self.__mutate_all(curr_gen_ents, num_slots, teachers)
            curr_gen_ents = self.__cross_over_all(curr_gen_ents, teachers, prefered_subjects)
            # elitism 
            num_old_gen = math.floor(self.num_ents * self.elitism_degree)
            num_curr_gen = self.num_ents - num_old_gen
            old_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            curr_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            next_gen_ents = old_gen_ents[0:num_old_gen] + curr_gen_ents[0:num_curr_gen]
            # progress report: print the fitness of the top ent of each gen to see how things are evolving
            next_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            top_ents.append(next_gen_ents[0])
            worst_ents.append(next_gen_ents[-1])
            curr_gen_ents = next_gen_ents
            # progress report 
            print("generation " + str(i + 1) + "/" + str(self.num_gens) + " done")
        # plot the evolution
        top_ents_fitnesses = list(map(lambda x: self.__fitness(x, prefered_subjects), top_ents))
        worst_ents_fitnesses = list(map(lambda x: self.__fitness(x, prefered_subjects), worst_ents))
        plt.plot(top_ents_fitnesses, "g", label="top_ent of gen")
        plt.plot(worst_ents_fitnesses, "r", label="worst_ent of gen")
        plt.legend(loc="lower right")
        plt.show()

    def __generate_initial_ents(self, reqs, num_slots, teachers):
        num_classes = len(reqs)
        ents = []
        for i in range(self.num_ents):
            # fill the school table with subjects
            school_timetable = []
            for j in range(num_classes):
                curr_class_reqs = reqs[j][1]
                expanded_reqs = self.__flatten(list(map(self.__expand, curr_class_reqs)))
                # pad class table with free slots
                if len(expanded_reqs) < num_slots:
                    expanded_reqs += ["Free"] * (num_slots - len(expanded_reqs))
                random.shuffle(expanded_reqs)
                school_timetable.append(expanded_reqs)
            # fill the school table with teachers
            for i in range(num_slots):
                random.shuffle(teachers)
                for j in range(num_classes):
                    school_timetable[j][i] = (school_timetable[j][i], teachers[j])
            ents.append(school_timetable)
        return ents
      
    def __expand(self, req):
        subj = req[0]
        num_repetitions = int(req[1])
        return [subj] * num_repetitions

    def __flatten(self, l):
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

    def __mutate_one(self, ent, num_slots, teachers):
        num_classes = len(ent)
        row_num = random.randrange(0, num_slots - 1)
        random.shuffle(teachers)
        for j in range(num_classes):
            ent[j][row_num] = (ent[j][row_num], teachers[j])
        return ent

    def __cross_over_all(self, ents, teachers, prefered_subjects):
        # enforcing even number of ents per generation simplifies this method a bit
        assert(len(ents) % 2 == 0)
        random.shuffle(ents)
        crossed_ents = []
        for i in range(int(len(ents)/2)):
            crossed_ents += self.__cross_over_two([ents[i], ents[i + 1]], teachers, prefered_subjects)
        return crossed_ents

    def __cross_over_two(self, ents, teachers, prefered_subjects):
        parent_1 = ents[0]
        parent_2 = ents[1]
        child_1 = []
        child_2 = []
        num_classes = len(parent_1)
        # construct the children
        for i in range(num_classes):
            num = random.uniform(0, 1)
            if num < 0.5: 
                child_1.append(parent_1[i])
                child_2.append(parent_2[i])
            else:
                child_1.append(parent_2[i])
                child_2.append(parent_1[i])
        child_1 = self.__fix_teacher_conflicts(child_1, teachers, prefered_subjects)
        child_2 = self.__fix_teacher_conflicts(child_2, teachers, prefered_subjects)
        return [child_1, child_2]

    def __fix_teacher_conflicts(self, ent, teachers, prefered_subjects):
        num_classes = len(ent)
        num_slots = len(ent[0])
        for i in range(num_slots):
            leftover_teachers = teachers[:]
            for j in range(num_classes):
                self.__remove_if_there(ent[j][i][1], leftover_teachers)
                for k in range(j + 1, num_classes):
                    self.__remove_if_there(ent[k][i][1], leftover_teachers)
                    if ent[j][i][1] == ent[k][i][1]:
                        subj = ent[j][i][0]
                        # try to resolve the conflic using a teacher that is prefered in this subject
                        qualified = list(filter(lambda x: subj in prefered_subjects[x], leftover_teachers))
                        if len(qualified) > 0:
                            picked_teacher = qualified[0]
                            ent[k][i] = (subj, qualified[0])
                        else:
                            if len(leftover_teachers) == 1:
                                # edge case
                                picked_teacher = leftover_teachers[0]
                            else:
                                picked_teacher = leftover_teachers[random.randrange(0, len(leftover_teachers) - 1)]
                            ent[k][i] = (subj, picked_teacher)
                        leftover_teachers.remove(picked_teacher)   
        return ent

    def __remove_if_there(self, elem, l):
      try:
        l.remove(elem)
        return l
      except (Exception):
        return l
      
    def __fitness(self, ent, prefered_subjects):
        num_classes = len(ent)
        num_slots = len(ent[0])
        score = 0
        for i in range(num_classes):
            for j in range(num_slots):
                subject = ent[i][j][0]
                teacher = ent[i][j][1]
                if subject in prefered_subjects[teacher]:
                    score += 1
        return score