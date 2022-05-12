# NOTE:
# All teachers can in theory teach all subjects but are better in some subjects than others (relaxation of "teacher can only teach subjects x,y and z")
# There must be at least as many teachers as there are classes
# Teachers are currently being assigned to Free slots but that just means that the teacher has a Free hour (just like the class)

# TODO:
# Cache fitness vals in a dict that is indexed by the to_string of a school timetable
# 
# Might need to make the mutation decision (based on mut_rate) for every row of the school timetable = ent
#
# fitness function: teachers dont like gaps (i.e. Free lessons they are assigned to)
#
# crossing over: maybe have conflict resolution also cater to these new factors in the fitness function 
# (maybe not though because teachers doing their good subjects will be the highes weighed factor)
# 
# multithreading (z.B. bei fitness evaluierung: jeder thread evaluiert 1/num_cores der ents)

import math
import random
import matplotlib.pyplot as plt
import copy 

class Optimizer:
    def __init__(self, params):
        self.num_gens = params[0]
        self.num_ents = params[1]
        self.muatation_rate = params[2]
        self.elitism_degree = params[3]

    def run(self, reqs, prefered_subjects):
        teachers = list(prefered_subjects.keys())
        curr_gen_ents = self.__generate_initial_ents(reqs, teachers)
        top_ents_fitnesses = []
        worst_ents_fitnesses = []
        top_ever_ent = []
        for i in range(self.num_gens):
            old_gen_ents = copy.deepcopy(curr_gen_ents)
            curr_gen_ents = self.__mutate_all(curr_gen_ents, teachers)
            curr_gen_ents = self.__cross_over_all(curr_gen_ents, teachers, prefered_subjects)
            # elitism 
            num_old_gen = math.floor(self.num_ents * self.elitism_degree)
            num_curr_gen = self.num_ents - num_old_gen
            old_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            curr_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            next_gen_ents = old_gen_ents[0:num_old_gen] + curr_gen_ents[0:num_curr_gen]
            # progress report: print the fitness of the top ent of each gen to see how things are evolving
            next_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            top_ents_fitnesses.append(self.__fitness(next_gen_ents[0], prefered_subjects))
            worst_ents_fitnesses.append(self.__fitness(next_gen_ents[-1], prefered_subjects))
            # remeber top ever ent
            if self.__fitness(next_gen_ents[0], prefered_subjects) > self.__fitness(top_ever_ent, prefered_subjects): 
                top_ever_ent = next_gen_ents[0]
            # progress report 
            print("generation " + str(i + 1) + "/" + str(self.num_gens) + " done")
            curr_gen_ents = copy.deepcopy(next_gen_ents)
        # plot the evolution
        print("FITNESS OF TOP EVER SEEN ENT: " + str(self.__fitness(top_ever_ent, prefered_subjects)))
        plt.plot(top_ents_fitnesses, "g", label="top_ent of gen")
        plt.plot(worst_ents_fitnesses, "r", label="worst_ent of gen")
        plt.legend(loc="lower right")
        plt.show()

    def __generate_initial_ents(self, reqs, teachers):
        num_slots = 50
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

    def __mutate_all(self, ents, teachers):
        ents_copy = copy.deepcopy(ents)
        mutated_ents = []
        for ent in ents_copy:
            rand_num = random.uniform(0, 1)
            if rand_num <= self.muatation_rate:
                mutated_ents.append(self.__mutate_one(ent, teachers))
            else:
                mutated_ents.append(ent)
        return mutated_ents

    def __mutate_one(self, ent, teachers):
        num_slots = 50
        num_classes = len(ent)
        row_num = random.randrange(0, num_slots - 1)
        random.shuffle(teachers)
        for j in range(num_classes):
            ent[j][row_num] = (ent[j][row_num], teachers[j])
        return ent

    def __cross_over_all(self, ents, teachers, prefered_subjects):
        ents_copy = copy.deepcopy(ents)
        # enforcing even number of ents per generation simplifies this method a bit
        assert(len(ents_copy) % 2 == 0)
        random.shuffle(ents_copy)
        crossed_ents = []
        for i in range(int(len(ents_copy)/2)):
            crossed_ents += self.__cross_over_two([ents_copy[i], ents_copy[i + 1]], teachers, prefered_subjects)
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
        num_slots = 50
        for i in range(num_slots):
            leftover_teachers = teachers[:]
            for j in range(num_classes):
                self.__remove_if_there(ent[j][i][1], leftover_teachers)
                for k in range(j + 1, num_classes):
                    self.__remove_if_there(ent[k][i][1], leftover_teachers)
                    if ent[j][i][1] == ent[k][i][1]:
                        subj = ent[j][i][0]
                        # try to resolve the conflict using a teacher that is prefered in this subject
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
        if ent == []:
            return 0
        num_classes = len(ent)
        num_slots = 50
        score = 0
        # weights of the different factors that contribute to the fitness of an ent
        prefered_subject_weight = 1
        gaps_weight = 0.5
        # plus points if a teacher teaches a subject he is good at
        for i in range(num_classes):
            for j in range(num_slots):
                subject = ent[i][j][0]
                teacher = ent[i][j][1]
                if subject in prefered_subjects[teacher]:
                    score += prefered_subject_weight * 1
        # minus points for gaps (i.e. a free in between two lessons or if first lesson of the day is free)
        # compute for all gaps their length and whether they are followed by a lesson or not 
        gap_info = []
        for i in range(num_classes):
            # for each day in the timetable
            for k in range(5):
                len_counter = 0
                # for each slot in that day
                for j in range(k * 10, (k + 1) * 10):
                    if ent[i][j][0] == "Free":
                        len_counter += 1
                        # if last slot of the day is free then we need to save the gap and not rely on this being done when the next lesson filled slot comes
                        if j == ((k + 1) * 10) - 1:
                            gap_info.append((len_counter, False))
                    else:
                        # if this lesson was preceeded by a gap
                        if not (len_counter == 0):
                            gap_info.append((len_counter, True))
                            len_counter = 0
        # only penlize gaps that are followed by a lesson
        gap_info = list(filter(lambda x: x[1], gap_info))
        gap_lens = list(map(lambda x: x[0], gap_info))
        for gap_len in gap_lens:
            score -= gaps_weight * gap_len
        return score

    def __print_ent(self, ent):
        print("START OF ENT")
        for school_class in ent:
            for slot in school_class:
                print(slot, sep=",")
            print()

    def __print_sorted_fitnesses(self, ents, prefered_subjects):
        tmp_ents = ents
        tmp_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
        print(list(map(lambda x: self.__fitness(x, prefered_subjects), tmp_ents)))