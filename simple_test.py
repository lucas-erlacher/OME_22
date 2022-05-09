from optimizer import Optimizer

if __name__ == "__main__":
    requirements = ([("Mr Wirz", ["Math"]),("Mrs Rosenberg", ["Biology", "Design Of Digital Circuits"]),("Mr Erlacher", ["Swiss-German"])],[("1A",[("Math", 4), ("Biology", 1), ("Swiss-German", 2)]),("1B", [("Math", 3), ("Biology", 3), ("Swiss-German", 1)])])
    # READABLE VERSION: 
    # (
    #     [
    #         ("Mr Wirz", ["Math"]),
    #         ("Mrs Rosenberg", ["Biology", "Design Of Digital Circuits"]), 
    #         ("Mr Erlacher", ["Swiss-German"])
    #     ], 
    #     [
    #         (
    #             "1A",
    #             [("Math", 4), ("Biology", 1), ("Swiss-German", 2)]
    #         ),
    #         (
    #             "1B", 
    #             [("Math", 3), ("Biology", 3), ("Swiss-German", 1)]
    #         )
    #     ]
    # )
    params = [100, 100, 0.1, 0.1]
    opt = Optimizer(params)
    print(opt.run(requirements))