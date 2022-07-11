import random
from typing import Tuple, List

from optimizer import Optimizer

Course = str
Teacher_name = str
Teacher = Tuple[Teacher_name,List[Course]]
Slot = Tuple[Course,Teacher_name]
Class_table = List[Slot]
Ent = List[Class_table]
Population = List[Ent]
Class_num = int
Slot_pos = int

if __name__ == "__main__":
    num_classes = random.randint(2,30)
    num_subjects = random.randint(6,12)
    class_reqs : List[Tuple[Class]] 
    # class_reqs = [
    #     ("1A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("1B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("1C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("2A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("2B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("2C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("3A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("3B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("3C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("4A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("4B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("4C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("5A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("5B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("5C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("6A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("6B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("6C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("7A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("7B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("7C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("8A", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("8B", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)]),
    #     ("8C", [("A", 4), ("B", 4), ("C", 4), ("D", 4), ("E", 4), ("F", 4), ("G", 4), ("H", 4)])
    # ]
    prefered_subjects = {
        "Mr. A": ["A", "B"],
        "Mr. B": ["C", "D"], 
        "Mr. C": ["E", "F"],
        "Mr. D": ["G", "H"],
        "Mr. E": ["A", "B"],
        "Mr. F": ["C", "D"], 
        "Mr. G": ["E", "F"],
        "Mr. H": ["G", "H"],
        "Mr. I": ["A", "B"],
        "Mr. J": ["C", "D"], 
        "Mr. K": ["E", "F"],
        "Mr. L": ["G", "H"],
        "Mr. M": ["A", "B"],
        "Mr. N": ["C", "D"], 
        "Mr. O": ["E", "F"],
        "Mr. P": ["G", "H"],
        "Mr. Q": ["A", "B"],
        "Mr. R": ["C", "D"], 
        "Mr. S": ["E", "F"],
        "Mr. T": ["G", "H"],
        "Mr. U": ["A", "B"],
        "Mr. V": ["C", "D"], 
        "Mr. W": ["E", "F"],
        "Mr. X": ["G", "H"],     
    }
    params = [1000, 100, 0.9, 0.75]
    opt = Optimizer(params)
    opt.run(class_reqs, prefered_subjects)
