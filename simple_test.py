from optimizer import Optimizer

if __name__ == "__main__":
    class_reqs = [
        ("1A", [("Math", 10), ("Biology", 5), ("Swiss-German", 15)]),
        ("1B", [("Math", 20), ("Design Of Digital Circuits", 10)]),
        ("1C", [("Biology", 5), ("Swiss-German", 30)]),
        ("2A", [("Math", 5), ("Biology", 30)]), 
        ("2B", [("Design Of Digital Circuits", 15), ("Chemistry", 15)]), 
        ("2C", [("Physics", 5), ("Chemistry", 25)]),
        ("3A", [("Math", 10), ("Biology", 5), ("Swiss-German", 15)]),
        ("3B", [("Math", 20), ("Design Of Digital Circuits", 10)]),
        ("3C", [("Biology", 5), ("Swiss-German", 30)]),
        ("4A", [("Math", 5), ("Biology", 30)]), 
        ("4B", [("Design Of Digital Circuits", 15), ("Chemistry", 15)]), 
        ("4C", [("Physics", 5), ("Chemistry", 25)]),
        ("5A", [("Math", 10), ("Biology", 5), ("Swiss-German", 15)]),
        ("5B", [("Math", 20), ("Design Of Digital Circuits", 10)]),
        ("5C", [("Biology", 5), ("Swiss-German", 30)]),
        ("6A", [("Math", 5), ("Biology", 30)]), 
        ("6B", [("Design Of Digital Circuits", 15), ("Chemistry", 15)]), 
        ("6C", [("Physics", 5), ("Chemistry", 25)]),
        ("7A", [("Math", 10), ("Biology", 5), ("Swiss-German", 15)]),
        ("7B", [("Math", 20), ("Design Of Digital Circuits", 10)]),
        ("7C", [("Biology", 5), ("Swiss-German", 30)]),
        ("8A", [("Math", 5), ("Biology", 30)]), 
        ("8B", [("Design Of Digital Circuits", 15), ("Chemistry", 15)]), 
        ("8C", [("Physics", 5), ("Chemistry", 25)])
    ]
    prefered_subjects = {
        "Mr. A": ["Math", "Swiss-German"],
        "Mr. B": ["Biology", "Design Of Digital Circuits"], 
        "Mr. C": ["Swiss-German", "Math"],
        "Mr. D": ["Physics", "Design Of Digital Circuits"],
        "Mr. E": ["Biology", "Chemistry"], 
        "Mr. F": ["Chemistry", "Math"],
        "Mr. G": ["Math", "Swiss-German"],
        "Mr. H": ["Biology", "Design Of Digital Circuits"], 
        "Mr. I": ["Swiss-German", "Math"],
        "Mr. J": ["Physics", "Design Of Digital Circuits"],
        "Mr. K": ["Biology", "Chemistry"], 
        "Mr. L": ["Chemistry", "Math"], 
        "Mr. M": ["Math", "Swiss-German"],
        "Mr. N": ["Biology", "Design Of Digital Circuits"], 
        "Mr. O": ["Swiss-German", "Math"],
        "Mr. P": ["Physics", "Design Of Digital Circuits"],
        "Mr. Q": ["Biology", "Chemistry"], 
        "Mr. R": ["Chemistry", "Math"], 
        "Mr. S": ["Math", "Swiss-German"],
        "Mr. T": ["Biology", "Design Of Digital Circuits"], 
        "Mr. U": ["Swiss-German", "Math"],
        "Mr. V": ["Physics", "Design Of Digital Circuits"],
        "Mr. W": ["Biology", "Chemistry"], 
        "Mr. X": ["Chemistry", "Math"],  
    }
    params = [1000, 100, 0.75, 0.5]
    opt = Optimizer(params)
    opt.run(class_reqs, prefered_subjects)