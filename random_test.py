import random
from typing import Tuple, List

from optimizer import Optimizer

Course = str
Subject = str
Class_name = str
Teacher_name = str
Teacher = Tuple[Teacher_name, List[Course]]
Slot = Tuple[Course, Teacher_name]
Class_table = List[Slot]
Ent = List[Class_table]
Population = List[Ent]
Class_num = int
Slot_pos = int


def name_of_teacher(teacher):
    return "T" + str(teacher)


def name_of_subject(subject):
    return "S" + str(subject)


def name_of_class(v_class):
    return "C" + str(v_class)


if __name__ == "__main__":
    num_classes = random.randint(2, 30)
    num_subjects = random.randint(6, 12)

    # -------------------Generate class_reqs------------------
    # maximal amount of lessons a single class can have of
    # any single subject
    max_slots_per_subject = 8
    class_reqs: List[Tuple[Class_name, List[Tuple[Subject, int]]]] = []
    for curr_class in range(num_classes):
        curr_class_name = name_of_class(curr_class)
        # reasonable amount of lessons per class(can't be more than 50)
        lessons_left = random.randint(15, 40)
        # for each subject
        reqs_of_curr_class: List[Tuple[Subject, int]] = []
        for subj in range(num_subjects):
            # following is done to ensure uniformity:
            maybe_num_lessons = random.randint(0, max_slots_per_subject)
            num_lessons = min(maybe_num_lessons, lessons_left)
            subj_name = name_of_subject(subj)
            new_req = (subj_name, num_lessons)
            lessons_left -= num_lessons
            reqs_of_curr_class.append(new_req)
        class_reqs.append((curr_class_name, reqs_of_curr_class))

    # -------------generate prefered_subjects -------------------
    # lower bound set, such that availability is ensured
    num_teachers = random.randint(num_classes, num_classes * 2)
    chance_of_preference = 0.3
    prefered_subjects = dict()
    for teacher in range(num_teachers):
        curr_pref_sub_list = []
        for subj in range(num_subjects):
            if (random.uniform(0, 1) < chance_of_preference):
                subj_name = name_of_subject(subj)
                curr_pref_sub_list.append(subj_name)
        teacher_name = name_of_teacher(teacher)
        prefered_subjects[teacher_name] = curr_pref_sub_list

    # ----------- select collective subjects --------------
    collective_subjects: List[Subject] = []
    chance_of_collectiveness = 0.2
    for subj in range(num_subjects):
        if (random.uniform(0, 1) < chance_of_collectiveness):
            collective_subjects.append(name_of_subject(subj))

    # -----------------insert params and run-------------------
    print("------ Requirement parameters -------")
    print("Number of classes: " + str(num_classes))
    print("Number of subjects: " + str(num_subjects))
    print("Number of teachers: " + str(num_teachers))
    num_gens = 100
    num_ents = 10
    print("------- Optimization parameters ----------")
    print("Number of generations: " + str(num_gens))
    print("Number of entities: " + str(num_ents))
    params = [num_gens, num_ents, collective_subjects]
    opt = Optimizer(params)
    opt.run(class_reqs, prefered_subjects)
