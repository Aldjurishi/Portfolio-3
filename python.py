"""
University Mystery - Constraint Satisfaction Problem
CCS2600 Artificial Intelligence Techniques - Portfolio Exercise #3
Solved using python-constraint library
"""

from constraint import Problem, AllDifferentConstraint


def solve_university_mystery():
    problem = Problem()

    # -------------------------------------------------------------------
    # VARIABLES & DOMAINS
    # Each variable represents an attribute value's office position (1–5).
    # -------------------------------------------------------------------
    offices = [1, 2, 3, 4, 5]

    # Teaching Subjects
    problem.addVariable("cs",          offices)   # Computer Science
    problem.addVariable("maths",       offices)   # Mathematics
    problem.addVariable("history",     offices)   # History
    problem.addVariable("philosophy",  offices)   # Philosophy
    problem.addVariable("subject5",    offices)   # Fifth (unnamed) subject

    # Office Colours
    problem.addVariable("blue",   offices)
    problem.addVariable("red",    offices)
    problem.addVariable("green",  offices)
    problem.addVariable("yellow", offices)
    problem.addVariable("white",  offices)

    # Alma Mater
    problem.addVariable("oxford",    offices)
    problem.addVariable("cambridge", offices)
    problem.addVariable("mit",       offices)
    problem.addVariable("harvard",   offices)
    problem.addVariable("stanford",  offices)

    # Cars
    problem.addVariable("tesla",    offices)
    problem.addVariable("bmw",      offices)
    problem.addVariable("mercedes", offices)
    problem.addVariable("volvo",    offices)
    problem.addVariable("audi",     offices)

    # Research Focus
    problem.addVariable("ai",        offices)   # Artificial Intelligence
    problem.addVariable("climate",   offices)   # Climate Change
    problem.addVariable("quantum",   offices)   # Quantum Physics
    problem.addVariable("neuro",     offices)   # Neuroscience
    problem.addVariable("medieval",  offices)   # Medieval Literature

    # Beverages
    problem.addVariable("espresso",  offices)
    problem.addVariable("herbal",    offices)   # Herbal Tea
    problem.addVariable("greentea",  offices)   # Green Tea
    problem.addVariable("coffee",    offices)   # Black Coffee
    problem.addVariable("drink5",    offices)   # Fifth (unnamed) beverage

    # -------------------------------------------------------------------
    # GLOBAL UNIQUENESS — All-Different within each attribute category
    # -------------------------------------------------------------------
    problem.addConstraint(AllDifferentConstraint(),
        ["cs", "maths", "history", "philosophy", "subject5"])
    problem.addConstraint(AllDifferentConstraint(),
        ["blue", "red", "green", "yellow", "white"])
    problem.addConstraint(AllDifferentConstraint(),
        ["oxford", "cambridge", "mit", "harvard", "stanford"])
    problem.addConstraint(AllDifferentConstraint(),
        ["tesla", "bmw", "mercedes", "volvo", "audi"])
    problem.addConstraint(AllDifferentConstraint(),
        ["ai", "climate", "quantum", "neuro", "medieval"])
    problem.addConstraint(AllDifferentConstraint(),
        ["espresso", "herbal", "greentea", "coffee", "drink5"])

    # -------------------------------------------------------------------
    # PROBLEM-SPECIFIC CONSTRAINTS
    # -------------------------------------------------------------------
    # C1:  CS professor's office has blue decor
    problem.addConstraint(lambda a, b: a == b, ["cs", "blue"])
    # C2:  Oxford graduate drives a Tesla
    problem.addConstraint(lambda a, b: a == b, ["oxford", "tesla"])
    # C3:  AI researcher drinks espresso
    problem.addConstraint(lambda a, b: a == b, ["ai", "espresso"])
    # C4:  Professor in office #1 graduated from Cambridge
    problem.addConstraint(lambda a: a == 1, ["cambridge"])
    # C5:  BMW driver's office is adjacent to the green-decor office
    problem.addConstraint(lambda a, b: abs(a - b) == 1, ["bmw", "green"])
    # C6:  Climate Change researcher drinks herbal tea
    problem.addConstraint(lambda a, b: a == b, ["climate", "herbal"])
    # C7:  Mathematics professor has red office decor
    problem.addConstraint(lambda a, b: a == b, ["maths", "red"])
    # C8:  Mercedes driver researches Quantum Physics
    problem.addConstraint(lambda a, b: a == b, ["mercedes", "quantum"])
    # C9:  Professor in office #3 drinks green tea
    problem.addConstraint(lambda a: a == 3, ["greentea"])
    # C10: Cambridge professor's office is next to the yellow-decor office
    problem.addConstraint(lambda a, b: abs(a - b) == 1, ["cambridge", "yellow"])
    # C11: Volvo driver teaches Philosophy
    problem.addConstraint(lambda a, b: a == b, ["volvo", "philosophy"])
    # C12: Neuroscience researcher's office is adjacent to the Audi driver's office
    problem.addConstraint(lambda a, b: abs(a - b) == 1, ["neuro", "audi"])
    # C13: History professor drinks black coffee
    problem.addConstraint(lambda a, b: a == b, ["history", "coffee"])
    # C14: White-decor office professor graduated from MIT
    problem.addConstraint(lambda a, b: a == b, ["white", "mit"])
    # C15: Stanford professor's office is immediately to the RIGHT of Harvard's
    problem.addConstraint(lambda a, b: a == b + 1, ["stanford", "harvard"])

    # -------------------------------------------------------------------
    # SOLVE
    # -------------------------------------------------------------------
    solutions = problem.getSolutions()
    return solutions


def display_solution(sol):
    """Pretty-print a single solution as a table."""
    attrs = {
        "Subject":   {"cs": "Computer Science", "maths": "Mathematics",
                      "history": "History", "philosophy": "Philosophy", "subject5": "(Unnamed)"},
        "Colour":    {"blue": "Blue", "red": "Red", "green": "Green",
                      "yellow": "Yellow", "white": "White"},
        "Alma Mater":{"oxford": "Oxford", "cambridge": "Cambridge", "mit": "MIT",
                      "harvard": "Harvard", "stanford": "Stanford"},
        "Car":       {"tesla": "Tesla", "bmw": "BMW", "mercedes": "Mercedes",
                      "volvo": "Volvo", "audi": "Audi"},
        "Beverage":  {"espresso": "Espresso", "herbal": "Herbal Tea", "greentea": "Green Tea",
                      "coffee": "Black Coffee", "drink5": "(Unnamed)"},
        "Research":  {"ai": "Artificial Intelligence", "climate": "Climate Change",
                      "quantum": "Quantum Physics", "neuro": "Neuroscience",
                      "medieval": "Medieval Literature"},
    }

    grid = {i: {} for i in range(1, 6)}
    for cat, mapping in attrs.items():
        for var, label in mapping.items():
            office = sol[var]
            grid[office][cat] = label

    header = f"{'Office':<8}" + "".join(f"{cat:<22}" for cat in attrs)
    print(header)
    print("-" * len(header))
    for office in range(1, 6):
        row = f"{'#' + str(office):<8}"
        for cat in attrs:
            row += f"{grid[office].get(cat, '?'):<22}"
        print(row)


def main():
    print("=" * 70)
    print("  University Mystery CSP — CCS2600 Portfolio Exercise #3")
    print("=" * 70)

    solutions = solve_university_mystery()

    print(f"\nTotal solutions found: {len(solutions)}\n")

    if not solutions:
        print("No solution exists. Check constraints.")
        return

    # Determine what CAN be uniquely deduced regardless of solution count
    all_vars = list(solutions[0].keys())
    determined = {}
    for var in all_vars:
        vals = set(s[var] for s in solutions)
        if len(vals) == 1:
            determined[var] = vals.pop()

    print("Attributes uniquely determined by the constraints:")
    for var, val in sorted(determined.items()):
        print(f"  {var} = Office #{val}")

    # Find what is always co-located with medieval literature
    print("\nResearch Focus: What is always true about 'Medieval Literature'?")
    research_attrs = {
        "espresso": "Espresso", "herbal": "Herbal Tea", "greentea": "Green Tea",
        "coffee": "Black Coffee", "drink5": "(Unnamed drink)",
        "mercedes": "Mercedes", "tesla": "Tesla", "bmw": "BMW",
        "volvo": "Volvo", "audi": "Audi",
    }
    never_colocated = []
    for var, label in research_attrs.items():
        count = sum(1 for s in solutions if s["medieval"] == s[var])
        if count == 0:
            never_colocated.append(label)
        elif count == len(solutions):
            print(f"  ALWAYS: Medieval Literature researcher uses/has: {label}")
    if never_colocated:
        print(f"  NEVER:  Medieval Literature researcher drinks/drives: {', '.join(never_colocated)}")

    print("\n--- Sample Solution (one of the valid solutions) ---\n")
    display_solution(solutions[0])

    med_office = solutions[0]["medieval"]
    print(f"\n>>> The Medieval Literature researcher is in Office #{med_office} <<<")
    print("    (Note: The problem as stated is under-constrained — see report for analysis.)")


if __name__ == "__main__":
    main()
