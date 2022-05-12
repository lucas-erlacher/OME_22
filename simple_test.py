from optimizer import Optimizer

if __name__ == "__main__":
    class_reqs = [("1A", [("Math", 10), ("Biology", 5), ("Swiss-German", 15)]),
                  ("1B", [("Math", 20), ("Design Of Digital Circuits", 10)]),
                  ("1C", [("Biology", 5), ("Swiss-German", 30)])]
    prefered_subjects = {
        "Mr. W": ["Math", "Swiss-German"],
        "Mrs. R": ["Biology", "Design Of Digital Circuits"], 
        "Mr. E": ["Swiss-German", "Math"]  
    }
    params = [400, 400, 0.5, 0.5]
    opt = Optimizer(params)
    opt.run(class_reqs, prefered_subjects)