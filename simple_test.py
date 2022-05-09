from optimizer import Optimizer

if __name__ == "__main__":
    class_reqs = [("1A",[("Math", 1), ("Biology", 1), ("Swiss-German", 2)]),("1B", [("Math", 2), ("Design Of Digital Circuits", 1)])]
    num_slots = 4
    prefered_subjects = [("Mr. W", ["Math", "Swiss-German"]), ("Mrs. R", ["Biology", "Design Of Digital Circuits"])]
    params = [100, 100, 0.1, 0.1]
    opt = Optimizer(params)
    print(opt.run(class_reqs, num_slots, prefered_subjects))