from optimizer import Optimizer

if __name__ == "__main__":
    class_reqs = [("1A", [("Math", 1), ("Biology", 1), ("Swiss-German", 2)]),
                  ("1B", [("Math", 2), ("Design Of Digital Circuits", 1)])]
    num_slots = 20
    prefered_subjects = {
        "Mr. W": ["Math", "Swiss-German"],
        "Mrs. R": ["Biology", "Design Of Digital Circuits"], 
        "Mr. E": ["Swiss-German", "Math"]  
    }
    params = [10, 10, 0.0, 0.5]
    opt = Optimizer(params)
    opt.run(class_reqs, num_slots, prefered_subjects)