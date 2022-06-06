# All teachers can in theory teach all subjects but are better in some subjects than others (relaxation of "teacher can only teach subjects x,y and z")
# There must be at least as many teachers as there are classes
# Teachers are currently being assigned to Free slots but that just means that the teacher has a Free hour (just like the class)
# num_ent must be even (simplifies crossing over method a bit)

# TODO:
# FITNESS FACTORS
#   fitness function: teachers dont like gaps (i.e. Free lessons they are assigned to)
# GENERAL
#   try more genetic algorithm things such as speciation
# PERFORMANCE
#   why the hell is the multiprocessing.Pool getting slower in each generation?
#   multiprocess more things (e.g. the mapping of fitness onto ents)
#   more optimizations (?)
#   find threshold (in terms of generation size) when to use multiprocessing (provided you fix the slowing down bug)
# EVALUATION
#   measure baseline (= that FET program) performance 

import math
import random
import matplotlib.pyplot as plt
import time
import multiprocessing
import numpy as np
import copy
from typing import Tuple, List

Course = str
Teacher_name = str
Teacher = Tuple[Teacher_name,List[Course]]
Slot = Tuple[Course,Teacher_name]
Class_table = List[Slot]
Ent = List[Class_table]
Population = List[Ent]
Class_num = int
Slot_pos = int


class Optimizer:
    def __init__(self, params):
        self.num_gens = params[0] 
        self.num_ents = params[1]
        self.mutation_rate = params[2]
        self.elitism_degree = params[3]
        self.fitness_cache = dict()
        self.num_slots = 50 
        # --------------- Debuging/profiling ------------------------
        self.use_multiprocessing = False
        self.profiling = False
        # --------------- Mutation parameters -----------------------
        self.use_crossover = False
        # I don't expect crossover to be effective alone, so better keep this on: 
        self.use_mutation = True
        # Average amount of teacher placements to be mutated per iteration
        self.avg_teacher_mutations = 60
        # Average amount of course<->class<->slot bindings to be mutated per iteration
        self.avg_course_mutations = 10
        # Chance to actually do a course mutation on an given ent
        self.course_mutation_chance = 0.4

    def run(self, reqs, prefered_subjects):
        s = time.time()
        teachers = list(prefered_subjects.keys())
        curr_gen_ents = self.__generate_initial_ents(reqs, teachers)
        top_ents_fitnesses = []
        worst_ents_fitnesses = []
        top_ever_ent = []
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for i in range(self.num_gens):
            # increase exploration after a few generations
            # To discuss: Ist das wirklich die richtige Veränderung? Hatten wir nicht z.B.
            # bei swarm-algorithms, dass die Schritte immer kleiner werden?
            # idk tbh. Vielleicht auch ganz gut so..
            if i >= 300 and self.mutation_rate < 1:
                self.mutation_rate += 0.01
            a = time.time()
            # copy needed in order for the mutation and crossing not to mess with the old generation
            x = time.time()
            old_gen_ents = copy.deepcopy(curr_gen_ents)
            y = time.time()
            if self.profiling: print("COPY CURR ENTS: " + str(y-x))
            # perform mutation and crossing over
            # ---------------Mutation----------------
            if self.use_mutation:
                x = time.time()
                curr_gen_ents = self.__mutate_all(curr_gen_ents, teachers,prefered_subjects, pool)
                y = time.time()
                if self.profiling: print("MUTATION: " + str(y-x))
            # --------------Crossover----------------
            if self.use_crossover:
                x = time.time()
                curr_gen_ents = self.__cross_over_all(curr_gen_ents, teachers, prefered_subjects, pool)
                y = time.time()
                if self.profiling: print("CROSSING OVER: " + str(y-x))
            # -------------- Elitism ----------------- 
            num_old_gen = math.floor(self.num_ents * self.elitism_degree)
            num_curr_gen = self.num_ents - num_old_gen
            x = time.time()
            # I'm not sure if the key is memoized here to save RAM?
            # TODO check if we have performance improvement if we evaluate and then sort
            old_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            y = time.time()
            if self.profiling: print("SORTING OLD ENTS: " + str(y-x))
            x = time.time()
            curr_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            y = time.time()
            if self.profiling: print("SORTING CURR ENTS: " + str(y-x))
            next_gen_ents = old_gen_ents[0:num_old_gen] + curr_gen_ents[0:num_curr_gen]
            # save the fitness of the top and worst ent of every gen
            x = time.time()
            next_gen_ents.sort(key=lambda x: self.__fitness(x, prefered_subjects), reverse=True)
            y = time.time()
            if self.profiling: print("SORTING CURR ENTS: " + str(y-x))
            top_ents_fitnesses.append(self.__fitness(next_gen_ents[0], prefered_subjects))
            worst_ents_fitnesses.append(self.__fitness(next_gen_ents[-1], prefered_subjects))
            # remeber top ever ent
            if self.__fitness(next_gen_ents[0], prefered_subjects) > self.__fitness(top_ever_ent, prefered_subjects): 
                top_ever_ent = next_gen_ents[0]
            # copy needed in order for the mutation and crossing (of the next loop iteration) not to mess with the top_ever_ent
            x = time.time()
            curr_gen_ents = copy.deepcopy(next_gen_ents)
            y = time.time()
            if self.profiling: print("COPY CURR ENTS: " + str(y-x))
            b = time.time()
            # progress report 
            print("runtime of generation " + str(i + 1) + ": " + str(b-a))
            print("current, best fitness: " + str(top_ents_fitnesses[-1]))
            if self.profiling: print()
        # plot the evolution
        freeslots = 0
        for i in range(self.num_slots):
            if top_ever_ent[-1][i][0] == "Free": freeslots = freeslots + 1
        print("Free slots in last class: " + str(freeslots))
        print("FITNESS OF TOP EVER SEEN ENT: " + str(self.__fitness(top_ever_ent, prefered_subjects)))
        plt.plot(top_ents_fitnesses, "g", label="top_ent of gen")
        plt.plot(worst_ents_fitnesses, "r", label="worst_ent of gen")
        plt.legend(loc="lower right")
        e = time.time()
        print("TOTAL RUNTIME: " + str(e - s))
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

    def __mutate_all(self, ents, teachers, prefered_subjects, pool):
        num_ents = len(ents)
        teacher_list = ([teachers] * num_ents)
        subjs_list = ([prefered_subjects] * num_ents)
        data = list(zip(ents, teacher_list,subjs_list ))
        tasks = (np.array_split(data, multiprocessing.cpu_count()))
        if self.use_multiprocessing:
            mutated_ents = self.__flatten(pool.map(self.mutate_batch, tasks))
        else:
            mutated_ents = self.__flatten(map(self.mutate_batch, tasks))
        return mutated_ents
    # Does 2 things: removes some course placements in some classes and puts these course
    # placements somewhere else, then removes some teacher placements and tries to find a
    # teacher for that slot.
    def mutate_batch(self, batch: Population):
        res: List[Ent] = []
        for input in batch:   
            ent = input[0]
            # ---------------------- dropout -----------------------------
            # randomely decide if ent is excluded from mutation
            if random.uniform(0, 1) > self.mutation_rate:
                res.append(ent)
                continue
            # --------------------- No dropout ---------------------------
            teachers: List[Teacher_name] = input[1]
            prefered_subjects = input[2]
            num_classes = len(ent)
            if random.uniform(0, 1) < self.course_mutation_chance :
                # ---------------clear some courses and fill them back in ----------------
                # We do this in 2 seperate loops to promote mutations
                # within freshly cleared slots
                # TODO maybe modularize the filling process and reuse it with initial gens
                
                # Amount of course mutations:
                n_c_mut = int(random.uniform(0, 2) * self.avg_course_mutations)
                # Fill me back in (courses to be filled into classes again)
                fmbi_c: List[Tuple[Class_num,Course]] = []
                # clearing step
                while len(fmbi_c) < n_c_mut:
                    clear_class: Class_num = random.randint(0,num_classes - 1)
                    clear_slot: Slot_pos = random.randint(0,self.num_slots - 1)
                    if(ent[clear_class][clear_slot][0] == "Free"): continue
                    else:
                        # put in fmbi, so we can add the course back in
                        fmbi_c.append((clear_class,ent[clear_class][clear_slot][0]))
                        ent[clear_class][clear_slot] = ("Free",ent[clear_class][clear_slot][1])
                        # refill step
                while len(fmbi_c) > 0 :
                    filling = fmbi_c[-1]
                    refill_class = filling[0]
                    assert(filling[1] != "Free")
                    refill_slot: Slot_pos = random.randint(0,self.num_slots - 1)
                    if(ent[refill_class][refill_slot][0] == "Free"):
                        ent[refill_class][refill_slot] =(filling[1],ent[clear_class][clear_slot][1])
                        fmbi_c.pop()
            # --------- clear some teachers and greedily fill them back in ----------
            # Amount of teacher mutations:
            n_t_mut = int(random.uniform(0, 2) * self.avg_teacher_mutations)
            # clear some teachers assigments
            fmbi_t: List[Tuple[Class_num,Slot_pos]] = []
            while (len(fmbi_t) < n_t_mut):
                clear_class: Class_num = random.randint(0,num_classes - 1)
                clear_slot: Slot_pos = random.randint(0,self.num_slots - 1)
                if ((ent[clear_class][clear_slot][0] == "Free") or (ent[clear_class][clear_slot][1] == "Refill")) : continue
                # clear teacher assignment in slot 
                ent[clear_class][clear_slot] = (ent[clear_class][clear_slot][0],"Refill")
                # remember slot
                fmbi_t.append((clear_class,clear_slot))
                # fill them back in
            while (len(fmbi_t) > 0):
                tbf = fmbi_t[-1] #to be filled
                refill_class = tbf[0]
                refill_slot = tbf[1]
                assert(ent[refill_class][refill_slot][1] == "Refill")
                # teachers, who don't teach during clear_slot
                bored_teachers = list(copy.deepcopy(teachers))
                for i in range(num_classes):
                    if ent[i][refill_slot][0] != "Free":
                        tai = ent[i][refill_slot][1] # teacher at i
                        if tai in bored_teachers:
                            bored_teachers.remove(tai)
                subj: Course = ent[refill_class][refill_slot][0]
                qualified = list(filter(lambda x: subj in prefered_subjects[x], bored_teachers))
                if len(qualified)==0:
                    # suddently everybody is qualified :)
                    qualified = bored_teachers
                ent[refill_class][refill_slot] = (ent[refill_class][refill_slot][0],random.choice(qualified))
                fmbi_t.pop()
            res.append(ent)
        return res

    def __cross_over_all(self, ents, teachers, prefered_subjects, pool):
        # enforcing even number of ents per generation simplifies this method a bit
        num_ents = len(ents)
        assert(num_ents % 2 == 0)
        random.shuffle(ents)
        pairs = []
        for i in range(int(num_ents / 2)):
            pairs.append([ents[2*i], ents[2*i + 1]])
        teacher_list = ([teachers] * (math.floor(num_ents / 2)))
        subjs_list = []
        for i in range(math.floor(num_ents / 2)):
            subjs_list.append(prefered_subjects)
        data = list(zip(pairs, teacher_list, subjs_list))
        tasks = (np.array_split(data, multiprocessing.cpu_count()))
        if self.use_multiprocessing:
            crossed_ents = self.__flatten(self.__flatten(pool.map(self.cross_over_batch, tasks)))
        else:
            crossed_ents = self.__flatten(self.__flatten(map(self.cross_over_batch, tasks)))
        return crossed_ents

    def cross_over_batch(self, batch):
        res = []
        for input in batch:
            ents = input[0]
            teachers = input[1]
            prefered_subjects = input[2]
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
            child_1_counters = self.count_free_slots(child_1)
            child_2_counters = self.count_free_slots(child_2)
            # DEBUGGING
            # print(sum(child_1_counters))
            # print(sum(child_2_counters))
            child_1 = self.__fix_teacher_conflicts(child_1, teachers, prefered_subjects)
            child_2 = self.__fix_teacher_conflicts(child_2, teachers, prefered_subjects)
            res.append([child_1, child_2])
        return res

    # for debugging purposes
    def count_free_slots(self, ent):
        counters = []
        for class_table in ent:
            counter = 0
            for slot_num in range(len(class_table)):
                if class_table[slot_num][0] == "Free":
                    counter += 1
            counters.append(counter)
        return counters


    def __fix_teacher_conflicts(self, ent, teachers, prefered_subjects):
        num_classes = len(ent)
        num_slots = 50
        for i in range(num_slots):
            # copy needed in order for leftover_teachers to be a copy of the full teachers list every time the outermost loop loops
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
        # caching
        if str(ent) in self.fitness_cache:
            return self.fitness_cache[str(ent)]
        else:
            num_classes = len(ent)
            num_slots = 50
            score = 0
            # weights of the different factors that contribute to the fitness of an ent
            prefered_subject_weight = 1
            gaps_weight = 0.2
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
            # cache the fitness value of the ent
            self.fitness_cache[str(ent)] = score
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
