from optimizer import Optimizer
import time

if __name__ == "__main__":
    class_reqs = [("1A", [("Math", 10), ("Biology", 5), ("Swiss-German", 15)]),
                  ("1B", [("Math", 20), ("Design Of Digital Circuits", 10)]),
                  ("1C", [("Biology", 5), ("Swiss-German", 30)])]
    prefered_subjects = {
        "Mr. W": ["Math", "Swiss-German"],
        "Mrs. R": ["Biology", "Design Of Digital Circuits"], 
        "Mr. E": ["Swiss-German", "Math"]  
    }
    params = [100, 1000, 0.4, 0.4]
    opt = Optimizer(params)
    s = time.time()
    opt.run(class_reqs, prefered_subjects)
    e = time.time()
    print(e-s)